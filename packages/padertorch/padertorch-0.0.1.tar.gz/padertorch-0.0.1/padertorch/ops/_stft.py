import numpy as np
import torch
from einops import rearrange
import paderbox as pb
import typing
from math import ceil

from torch.nn import functional as F


def get_stft_kernel(size, window):
    length = len(window)
    real = np.array([
        [np.cos(-1 * n * 2 * np.pi / size * k) * window[k]
         for k in range(length)] for n in range(size // 2 + 1)
    ])
    imag = np.array([
        [np.sin(-1 * n * 2 * np.pi / size * k) * window[k]
         for k in range(length)] for n in range(size // 2 + 1)
    ])
    kernel = np.concatenate([real, imag], axis=0)
    # print(kernel.shape)
    return torch.from_numpy(kernel).unsqueeze(dim=1)


def get_istft_kernel(size, shift, window):
    window = pb.transform.module_stft._biorthogonal_window_fastest(
        window, shift) / size
    length = len(window)
    kernel_numpy = np.array([
        [np.cos(1 * f * 2 * np.pi / size * n) * window[n]
         for n in range(length)] for f in range(size)
    ])
    kernel_real = torch.from_numpy(kernel_numpy)
    kernel_real = torch.unsqueeze(kernel_real, dim=1)

    kernel_numpy = np.array([
        [np.sin(-1 * f * 2 * np.pi / size * n) * window[n]
         for n in range(length)] for f in range(size)
    ])
    kernel_imag = torch.from_numpy(kernel_numpy)
    kernel_imag = torch.unsqueeze(kernel_imag, dim=1)
    return kernel_real, kernel_imag


class STFT:
    def __init__(
            self,
            size: int = 1024,
            shift: int = 256,
            *,
            window: [str, typing.Callable] = 'blackman',
            window_length: int = None,
            fading: typing.Optional[typing.Union[bool, str]] = 'full',
            pad: bool = True,
            symmetric_window: bool = False,
            complex_representation: str = 'complex'
    ):
        """
        This is a torch stft implementation which mirrors the behavior of
        the numpy implementation in paderbox.transform.stft.
        For additional informations about the parameters please refer to
        the numpy implementation.
        Args:

            size: Scalar FFT-size.
            shift: Scalar FFT-shift. Typically shift is a fraction of size.
            window: Window function handle.
            window_length:
            fading:
            pad:
            symmetric_window:
            complex_representation: defines how to handle the real and
                imaginary part of the complex stft signal:
                                either complex, concat or stacked
                                complex is not supported at the moment
        """

        self.possible_out_types = ['concat', 'stacked', 'complex']
        assert complex_representation in self.possible_out_types, (
            f'Please choose one of the predefined output_types'
            f' {self.possible_out_types}, not {complex_representation}'
        )
        self.complex_representation = complex_representation
        assert size % 2 == 0, 'At the moment we only support even FFT sizes'
        self.size = size
        self.shift = shift
        self.window_length = window_length if window_length is not None \
            else size

        window = pb.transform.module_stft._get_window(
            window=window,
            symmetric_window=symmetric_window,
            window_length=self.window_length,
        )
        assert fading in [None, True, False, 'full', 'half'], fading
        self.fading = fading
        self.pad = pad
        self.stft_kernel = get_stft_kernel(size, window)
        self.istft_kernel_real, self.istft_kernel_imag = get_istft_kernel(
            size, shift, window)

    def __call__(self, inputs):
        """
        Args:
            inputs: shape: [..., T], T is #samples
            num_samples, list or tensor of #samples

        >>> mixture = torch.rand((2, 6, 203))
        >>> torch_stft = STFT(512, 20, window_length=40,\
                              complex_representation='concat')
        >>> torch_stft_out = torch_stft(mixture)
        >>> torch_stft_out.shape
        torch.Size([2, 6, 12, 514])
        >>> from paderbox.transform import stft
        >>> stft_out = stft(mixture.numpy(), 512, 20, window_length=40)
        >>> stft_signal = np.concatenate(\
                [np.real(stft_out), np.imag(stft_out)], axis=-1)
        >>> np.testing.assert_allclose(torch_stft_out, stft_signal, atol=1e-5)
        >>> mixture = torch.rand((2, 6, 203))
        >>> torch_stft = STFT(512, 20, window_length=40,\
                              complex_representation='complex')
        >>> torch_stft_out = torch_stft(mixture)
        >>> torch_stft_out.shape
        torch.Size([2, 6, 12, 257])
        >>> from paderbox.transform import stft
        >>> stft_out = stft(mixture.numpy(), 512, 20, window_length=40)
        >>> np.testing.assert_allclose(torch_stft_out.numpy(), stft_out, atol=1e-5)

        """
        org_shape = inputs.shape
        stride = self.shift
        length = self.window_length
        x = inputs.view((-1, org_shape[-1]))
        # Pad with zeros to have enough samples for the window function to fade.
        assert self.fading in [None, True, False, 'full', 'half'], self.fading
        if self.fading not in [False, None]:
            if self.fading == 'half':
                pad_width= (
                    (self.window_length - self.shift) // 2,
                    ceil((self.window_length - self.shift) / 2)
                )
            else:
                pad_width = self.window_length - self.shift
                pad_width = (pad_width, pad_width)
            x = F.pad(x, pad_width, mode='constant')

        if self.pad:
            if x.shape[-1] < length:
                pad_size = length - x.shape[-1]
                x = F.pad(x, (0, pad_size))
            elif stride != 1 and (x.shape[-1] + stride - length) % stride != 0:
                pad_size = stride - ((x.shape[-1] + stride - length) % stride)
                x = F.pad(x, (0, pad_size))

        x = torch.unsqueeze(x, 1) # [..., 1, T]
        weights = self.stft_kernel.to(x)
        encoded = F.conv1d(x, weight=weights, stride=stride)

        encoded = encoded.view(*org_shape[:-1], *encoded.shape[-2:])
        encoded = rearrange(encoded, '... feat frames -> ... frames feat')
        encoded = torch.chunk(encoded, 2, dim=-1)
        if self.complex_representation == 'stacked':
            encoded = torch.stack(encoded, dim=-1)
        elif self.complex_representation == 'concat':
            encoded = torch.cat(encoded, dim=-1)
        elif self.complex_representation == 'complex':
            encoded = torch.complex(*encoded)
        else:
            raise ValueError(
                f'Please choose one of the predefined output_types'
                f'{self.possible_out_types} not {self.complex_representation}'
            )
        return encoded

    def inverse(self, stft_signal):
        """
        Args:
            stft_signal:
                if complex_representation == 'complex':
                        shape: [..., frames, num_fbins]
                if complex_representation == 'stacked':
                        shape: [..., frames, num_fbins, 2]
                if complex_representation == 'concat':
                        shape: [..., frames, 2 * num_fbins]
            num_samples, list or tensor of #samples
        Returns:
            [..., T]

        >>> stft_signal = torch.rand((2, 4, 10, 514))
        >>> torch_stft = STFT(512, 20, window_length=40, \
                              complex_representation='concat')
        >>> torch_signal = torch_stft.inverse(stft_signal)
        >>> torch_signal.shape
        torch.Size([2, 4, 180])
        >>> from paderbox.transform import istft
        >>> signal_np = stft_signal.numpy()
        >>> complex_signal = signal_np[..., :257] + 1j* signal_np[..., 257:]
        >>> time_signal = istft(complex_signal, 512, 20, window_length=40)
        >>> np.testing.assert_allclose(torch_signal, time_signal, atol=1e-5)

        >>> stft_signal = torch.rand((2, 4, 10, 257, 2))
        >>> torch_stft = STFT(512, 20, window_length=40, \
                              complex_representation='stacked')
        >>> torch_signal = torch_stft.inverse(stft_signal)
        >>> torch_signal.shape
        torch.Size([2, 4, 180])
        >>> from paderbox.transform import istft
        >>> signal_np = stft_signal.numpy()
        >>> complex_signal = signal_np[..., 0] + 1j* signal_np[..., 1]
        >>> time_signal = istft(complex_signal, 512, 20, window_length=40)
        >>> np.testing.assert_allclose(torch_signal, time_signal, atol=1e-5)

        >>> stft_signal = torch.rand((2, 4, 10, 257), dtype=torch.complex128)
        >>> torch_stft = STFT(512, 20, window_length=40, \
                              complex_representation='complex')
        >>> torch_signal = torch_stft.inverse(stft_signal)
        >>> torch_signal.shape
        torch.Size([2, 4, 180])
        >>> from paderbox.transform import istft
        >>> signal_np = stft_signal.numpy()
        >>> time_signal = istft(signal_np, 512, 20, window_length=40)
        >>> np.testing.assert_allclose(torch_signal, time_signal, atol=1e-5)
        """

        if self.complex_representation == 'stacked':
            signal_real, signal_imag = rearrange(stft_signal, '... s -> s ...')
        elif self.complex_representation == 'concat':
            signal_real, signal_imag = torch.chunk(stft_signal, 2, dim=-1)
        elif self.complex_representation == 'complex':
            signal_real, signal_imag = stft_signal.real, stft_signal.imag
        else:
            raise ValueError(
                f'Please choose one of the predefined output_types'
                f'{self.possible_out_types} not {self.complex_representation}'
            )
        org_shape = signal_real.shape

        def _apply_kernel(signal, kernel, reflect):
            signal = signal.view(-1, *org_shape[-2:])
            signal = rearrange(signal, '... frames feat -> ... feat frames')
            if reflect:
                signal = torch.cat([
                    signal, -signal[:, 1:-1].flip(1)], dim=1)
            else:
                signal = torch.cat([
                    signal, signal[:, 1:-1].flip(1)], dim=1)
            return F.conv_transpose1d(signal, weight=kernel, stride=self.shift)

        decoded_real = _apply_kernel(
            signal_real, self.istft_kernel_real.to(signal_real), reflect=False)
        decoded_imag = _apply_kernel(
            signal_imag, self.istft_kernel_imag.to(signal_imag), reflect=True)

        time_signal = decoded_real + decoded_imag
        time_signal = time_signal.view(*org_shape[:-2], time_signal.shape[-1])
        if self.fading not in [None, False]:
            pad_width = (self.window_length - self.shift)
            if self.fading == 'half':
                pad_width /= 2
            cut_off = time_signal.shape[-1] - ceil(pad_width)
            time_signal = time_signal[..., int(pad_width): cut_off]
        return time_signal

    def samples_to_frames(self, samples):
        """
        Calculates number of STFT frames from number of samples in time domain.

        Args:
            samples: Number of samples in time domain.

        Returns:
            Number of STFT frames.

        """
        return pb.transform.module_stft._samples_to_stft_frames(
            samples, self.window_length, self.shift,
            pad=self.pad, fading=self.fading
        )

    def sample_index_to_frame_index(self, sample_index):
        """
        Calculates the best frame index for a given sample index

        Args:
            sample_index:

        Returns:

        """
        return pb.transform.module_stft.sample_index_to_stft_frame_index(
            sample_index, self.window_length, self.shift, fading=self.fading
        )

    def frames_to_samples(self, frames):
        """
        Calculates samples in time domain from STFT frames

        Args:
            frames: number of frames in STFT

        Returns: number of samples in time signal

        """
        return pb.transform.module_stft._stft_frames_to_samples(
            frames, self.window_length, self.shift, fading=self.fading
        )
