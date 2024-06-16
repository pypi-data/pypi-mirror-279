import einops
import torch
from torch.nn import functional as F
from torch_fourier_shift import fourier_shift_image_2d
from torch_grid_utils import coordinate_grid

from torch_subpixel_crop.dft_utils import dft_center
from torch_subpixel_crop.grid_sample_utils import array_to_grid_sample


def subpixel_crop_2d(
    images: torch.Tensor, positions: torch.Tensor, sidelength: int,
):
    """Extract square patches from 2D images at positions with subpixel precision.

    Patches are extracted at the nearest integer coordinates then phase shifted
    such that the requested position is at the center of the patch.

    Parameters
    ----------
    images: torch.Tensor
        `(b, h, w)` or `(h, w)` array of 2D images.
    positions: torch.Tensor
        `(..., b, 2)` or `(..., 2)` array of coordinates for patch centers.
    sidelength: int
        Sidelength of square patches extracted from `images`.

    Returns
    -------
    patches: torch.Tensor
        `(..., b, sidelength, sidelength)` array of patches from `images` with their
        centers (DC components of fftshifted DFTs at `positions`.
    """
    if images.ndim == 2:
        images = einops.rearrange(images, 'h w -> 1 h w')
        positions = einops.rearrange(positions, '... yx -> ... 1 yx')
    positions, ps = einops.pack([positions], pattern='* t yx')
    positions = einops.rearrange(positions, 'b t yx -> t b yx')
    patches = einops.rearrange(
        [
            _extract_patches_from_single_image(
                image=_image,
                positions=_positions,
                output_image_sidelength=sidelength
            )
            for _image, _positions
            in zip(images, positions)
        ],
        pattern='t b h w -> b t h w'
    )
    [patches] = einops.unpack(patches, pattern='* t h w', packed_shapes=ps)
    return patches


def _extract_patches_from_single_image(
    image: torch.Tensor,  # (h, w)
    positions: torch.Tensor,  # (b, 2) yx
    output_image_sidelength: int,
) -> torch.Tensor:
    h, w = image.shape
    b, _ = positions.shape

    # find integer positions and shifts to be applied
    integer_positions = torch.round(positions)
    shifts = integer_positions - positions

    # generate coordinate grids for sampling around each integer position
    ph, pw = (output_image_sidelength, output_image_sidelength)
    center = dft_center((ph, pw), rfft=False, fftshifted=True, device=image.device)
    grid = coordinate_grid(
        image_shape=(ph, pw),
        center=center,
        device=image.device
    )  # (h, w, 2)
    broadcastable_positions = einops.rearrange(integer_positions, 'b yx -> b 1 1 yx')
    grid = grid + broadcastable_positions  # (b, h, w, 2)

    # extract patches, grid sample handles boundaries
    patches = F.grid_sample(
        input=einops.repeat(image, 'h w -> b 1 h w', b=b),
        grid=array_to_grid_sample(grid, array_shape=(h, w)),
        mode='nearest',
        padding_mode='zeros',
        align_corners=True
    )
    patches = einops.rearrange(patches, 'b 1 h w -> b h w')

    # phase shift to center images
    patches = fourier_shift_image_2d(images=patches, shifts=shifts)
    return patches
