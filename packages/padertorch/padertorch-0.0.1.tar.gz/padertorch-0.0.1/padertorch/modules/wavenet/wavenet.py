#  Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#      * Neither the name of the NVIDIA CORPORATION nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL NVIDIA CORPORATION BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# *****************************************************************************
import math

import torch
from cached_property import cached_property

from padertorch.base import Module
from padertorch.ops import mu_law_encode, mu_law_decode


__all__ = [
    'WaveNet',
    'Conv'
]


class Conv(torch.nn.Module):
    """
    A convolution with the option to be causal and use xavier initialization
    """

    def __init__(self, in_channels, out_channels, kernel_size=1, stride=1,
                 dilation=1, bias=True, w_init_gain='linear', is_causal=False):
        super(Conv, self).__init__()
        self.is_causal = is_causal
        self.kernel_size = kernel_size
        self.dilation = dilation

        self.conv = torch.nn.Conv1d(
            in_channels, out_channels, kernel_size=kernel_size, stride=stride,
            dilation=dilation, bias=bias
        )

        torch.nn.init.xavier_uniform_(
            self.conv.weight, gain=torch.nn.init.calculate_gain(w_init_gain))

    def forward(self, signal):
        if self.is_causal:
            padding = (int((self.kernel_size - 1) * (self.dilation)), 0)
            signal = torch.nn.functional.pad(signal, padding)
        return self.conv(signal)


class WaveNet(Module):
    def __init__(
            self, n_cond_channels, upsamp_window, upsamp_stride,
            n_in_channels=256, n_layers=16, max_dilation=128,
            n_residual_channels=64, n_skip_channels=256, n_out_channels=256,
            fading='full'
    ):
        """
        WaveNet implementation based on https://github.com/NVIDIA/nv-wavenet

        :param n_cond_channels: local conditioning: e.g. num mel bins
        :param upsamp_window: frame length
        :param upsamp_stride: frame step
        :param n_in_channels:
        :param n_layers:
        :param max_dilation:
        :param n_residual_channels:
        :param n_skip_channels:
        :param n_out_channels:
        """
        super().__init__()

        self.n_layers = n_layers
        self.max_dilation = max_dilation
        self.n_residual_channels = n_residual_channels
        self.n_out_channels = n_out_channels

        self.upsamp_stride = upsamp_stride
        self.upsamp_window = upsamp_window
        self.upsample = torch.nn.ConvTranspose1d(
            n_cond_channels, n_cond_channels, upsamp_window, upsamp_stride
        )
        self.fading = fading
        self.cond_layers = Conv(
            n_cond_channels, 2 * n_residual_channels * n_layers,
            w_init_gain='tanh'
        )
        self.dilate_layers = torch.nn.ModuleList()
        self.res_layers = torch.nn.ModuleList()
        self.skip_layers = torch.nn.ModuleList()

        self.embed = torch.nn.Embedding(n_in_channels, n_residual_channels)
        self.conv_out = Conv(
            n_skip_channels, n_out_channels, bias=False, w_init_gain='relu')
        self.conv_end = Conv(
            n_out_channels, n_out_channels, bias=False, w_init_gain='linear')

        loop_factor = math.floor(math.log2(max_dilation)) + 1
        for i in range(n_layers):
            dilation = int(2 ** (i % loop_factor))

            # Kernel size is 2 in nv-wavenet
            in_layer = Conv(
                n_residual_channels, 2 * n_residual_channels, kernel_size=2,
                dilation=dilation, w_init_gain='tanh',
                is_causal=True
            )
            self.dilate_layers.append(in_layer)

            # last one is not necessary
            if i < n_layers - 1:
                res_layer = Conv(
                    n_residual_channels, n_residual_channels,
                    w_init_gain='linear'
                )
                self.res_layers.append(res_layer)

            skip_layer = Conv(
                n_residual_channels, n_skip_channels, w_init_gain='relu')
            self.skip_layers.append(skip_layer)

    def forward(self, features, audio):
        quantized = mu_law_encode(audio).long()
        cond_input = self.get_cond_input(features)
        assert self.upsamp_stride > (cond_input.shape[-1] - quantized.shape[1]) >= 0, (quantized.shape, cond_input.shape)
        cond_input = cond_input[:, :, :quantized.size(1)]

        forward_input = self.embed(quantized)
        forward_input = forward_input.transpose(1, 2)

        cond_acts = self.cond_layers(cond_input)
        cond_acts = cond_acts.view(
            cond_acts.size(0), self.n_layers, -1, cond_acts.size(2))
        for i in range(self.n_layers):
            in_act = self.dilate_layers[i](forward_input)
            in_act = in_act + cond_acts[:, i, :, :]
            t_act = torch.tanh(in_act[:, :self.n_residual_channels, :])
            s_act = torch.sigmoid(in_act[:, self.n_residual_channels:, :])
            acts = t_act * s_act
            if i < len(self.res_layers):
                res_acts = self.res_layers[i](acts)
            forward_input = res_acts + forward_input

            if i == 0:
                output = self.skip_layers[i](acts)
            else:
                output = self.skip_layers[i](acts) + output

        output = torch.nn.functional.relu(output, True)
        output = self.conv_out(output)
        output = torch.nn.functional.relu(output, True)
        output = self.conv_end(output)

        # Remove last probabilities because they've seen all the data
        last = output[:, :, -1]
        last = last.unsqueeze(2)
        output = output[:, :, :-1]

        # Replace probability for first value with 0's because we don't know
        first = last * 0.0
        output = torch.cat((first, output), dim=2)

        return output, quantized

    def get_cond_input(self, features):
        """
        Takes in features and gets the 2*R x batch x # layers x samples tensor
        """
        cond_input = self.upsample(features)
        if self.fading is not None:
            assert self.fading in ['half', 'full']
            pad_width = self.upsamp_window - self.upsamp_stride
            if self.fading == 'half':
                front_pad = pad_width // 2
                back_pad = math.ceil(pad_width / 2)
                cond_input = cond_input[..., front_pad:-back_pad]
            elif self.fading == 'full':
                cond_input = cond_input[..., pad_width:-pad_width]
        cond_input = self.cond_layers(cond_input)
        return cond_input

    def export_weights(self):
        """
        Returns a dictionary with tensors ready for nv_wavenet wrapper
        """
        model = {}
        # We're not using a convolution to start to this does nothing
        model["embedding_prev"] = torch.zeros(
            self.n_out_channels, self.n_residual_channels).float().cuda(
            self.embed.weight.get_device()
        )

        model["embedding_curr"] = self.embed.weight.data
        model["conv_out_weight"] = self.conv_out.conv.weight.data
        model["conv_end_weight"] = self.conv_end.conv.weight.data

        dilate_weights = []
        dilate_biases = []
        for layer in self.dilate_layers:
            dilate_weights.append(layer.conv.weight.data)
            dilate_biases.append(layer.conv.bias.data)
        model["dilate_weights"] = dilate_weights
        model["dilate_biases"] = dilate_biases

        model["max_dilation"] = self.max_dilation

        res_weights = []
        res_biases = []
        for layer in self.res_layers:
            res_weights.append(layer.conv.weight.data)
            res_biases.append(layer.conv.bias.data)
        model["res_weights"] = res_weights
        model["res_biases"] = res_biases

        skip_weights = []
        skip_biases = []
        for layer in self.skip_layers:
            skip_weights.append(layer.conv.weight.data)
            skip_biases.append(layer.conv.bias.data)
        model["skip_weights"] = skip_weights
        model["skip_biases"] = skip_biases

        model["use_embed_tanh"] = False

        return model

    @cached_property
    def nv_wavenet(self):
        from .nv_wavenet.nv_wavenet import NVWaveNet
        return NVWaveNet(**(self.export_weights()))

    def infer(self, x, chunk_length=None, chunk_overlap=0):
        with torch.no_grad():
            x = self.get_cond_input(x)
            x = x.view(
                x.size(0), self.n_layers, -1, x.size(2))
            # This makes the data channels x batch x num_layers x samples
            x = x.permute(2, 0, 1, 3)
            length = x.shape[-1]
            if chunk_length is None or length <= chunk_length:
                chunks = [x]
            else:
                n = math.ceil(
                    (length - chunk_overlap) / (chunk_length - chunk_overlap)
                )
                chunk_length = math.ceil(length/n) + chunk_overlap
                chunks = [
                    x[..., onset:onset+chunk_length]
                    for onset in range(
                        0, length - chunk_overlap, chunk_length - chunk_overlap
                    )
                ]
            audio = []
            for i, xi in enumerate(chunks):
                if xi.device == 'cpu':
                    raise NotImplementedError
                else:
                    from .nv_wavenet.nv_wavenet import Impl
                    xi = self.nv_wavenet.infer(xi, Impl.AUTO)
                    torch.cuda.synchronize(xi.device)
                    xi = mu_law_decode(xi, self.n_out_channels)
                if i > 0:
                    xi = xi[..., chunk_overlap:]
                audio.append(xi)
            audio = torch.cat(tuple(audio), dim=-1)
            return audio
