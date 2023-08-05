import glob
import os
from pathlib import Path

import numpy as np
import torch
import torchvision
import yaml
from PIL import Image
from torchvision.transforms import InterpolationMode

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}


def register_node(identifier: str, display_name: str):
    def decorator(cls):
        NODE_CLASS_MAPPINGS[identifier] = cls
        NODE_DISPLAY_NAME_MAPPINGS[identifier] = display_name

        return cls

    return decorator


def comfyui_to_native_torch(imgs: torch.Tensor):
    """
    Convert images in NHWC format to NCHW format.

    Use this to convert ComfyUI images to torch-native images.
    """
    return imgs.permute(0, 3, 1, 2)


def native_torch_to_comfyui(imgs: torch.Tensor):
    """
    Convert images in NCHW format to NHWC format.

    Use this to convert torch-native images to ComfyUI images.
    """
    return imgs.permute(0, 2, 3, 1)


def load_image(path):
    img = Image.open(path).convert("RGB")
    img = np.array(img).astype(np.float32) / 255.0
    img = torch.from_numpy(img).unsqueeze(0)
    return img


@register_node("JWImageLoadRGB", "Image Load RGB")
class JWImageLoadRGB:
    CATEGORY = "jamesWalker55"

    INPUT_TYPES = lambda: {
        "required": {
            "path": ("STRING", {"default": "./image.png"}),
        }
    }

    RETURN_NAMES = ("IMAGE",)
    RETURN_TYPES = ("IMAGE",)

    OUTPUT_NODE = False

    FUNCTION = "execute"

    def execute(self, path: str):
        assert isinstance(path, str)

        return load_image(path)


@register_node("JWImageResize", "Image Resize")
class JWImageResize:
    CATEGORY = "jamesWalker55"

    INPUT_TYPES = lambda: {
        "required": {
            "image": ("IMAGE",),
            "height": ("INT", {"default": 512, "min": 0, "step": 1, "max": 99999}),
            "width": ("INT", {"default": 512, "min": 0, "step": 1, "max": 99999}),
            "interpolation_mode": (
                ["bicubic", "bilinear", "nearest", "nearest exact"],
            ),
        }
    }

    RETURN_NAMES = ("IMAGE",)
    RETURN_TYPES = ("IMAGE",)

    OUTPUT_NODE = False

    FUNCTION = "execute"

    def execute(
        self,
        image: torch.Tensor,
        width: int,
        height: int,
        interpolation_mode: str,
    ):
        assert isinstance(image, torch.Tensor)
        assert isinstance(height, int)
        assert isinstance(width, int)
        assert isinstance(interpolation_mode, str)

        interpolation_mode = interpolation_mode.upper().replace(" ", "_")
        interpolation_mode = getattr(InterpolationMode, interpolation_mode)

        resizer = torchvision.transforms.Resize(
            (height, width),
            interpolation=interpolation_mode,
            antialias=True,
        )

        image = comfyui_to_native_torch(image)
        image = resizer(image)
        image = native_torch_to_comfyui(image)

        return (image,)


# @register_node("JWImageToSquare", "Image To Square")
# class JWImageToSquare:
#     CATEGORY = "jamesWalker55"

#     INPUT_TYPES = lambda: {
#         "required": {
#             "image": ("IMAGE",),
#             "size": ("INT", {"default": 512, "min": 0, "step": 1, "max": 99999}),
#             "fill_mode": (["ignore aspect ratio", "crop", "pad empty"],),
#             "interpolation_mode": (
#                 ["bicubic", "bilinear", "nearest", "nearest exact"],
#             ),
#         }
#     }

#     RETURN_NAMES = ("IMAGE",)
#     RETURN_TYPES = ("IMAGE",)

#     OUTPUT_NODE = False

#     FUNCTION = "execute"

#     def execute(
#         self,
#         image: torch.Tensor,
#         size: int,
#         fill_mode: str,
#         interpolation_mode: str,
#     ):
#         assert isinstance(image, torch.Tensor)
#         assert isinstance(size, int)
#         assert fill_mode in ("ignore aspect ratio", "crop", "pad empty")
#         assert isinstance(interpolation_mode, str)

#         interpolation_mode = interpolation_mode.upper().replace(" ", "_")
#         interpolation_mode = getattr(InterpolationMode, interpolation_mode)

#         resizer = torchvision.transforms.Resize(
#             (height, width),
#             interpolation=interpolation_mode,
#             antialias=True,
#         )

#         image = comfyui_to_native_torch(image)
#         image = resizer(image)
#         image = native_torch_to_comfyui(image)

#         return (image,)
