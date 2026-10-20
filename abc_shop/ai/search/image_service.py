"""AI / application layer: image encoder f(I) -> z (unchanged from Assignment 06).

A hand-made encoder instead of a neural network, so the prototype stays small and offline:
  * colour part: 4x4x4 RGB histogram of the foreground (object) pixels   -> 64 values
  * shape part:  8x8 occupancy grid of the foreground mask               -> 64 values
Both parts are L2-normalised and concatenated (128-d). The background colour is estimated
from the image border, so photos on a different plain background still match.
"""
import numpy as np
from PIL import Image

SIZE = 64


class ImageService:

    def encode(self, image_path):
        img = Image.open(image_path).convert("RGB").resize((SIZE, SIZE))
        pixels = np.asarray(img, dtype=float)

        border = np.concatenate([pixels[0], pixels[-1], pixels[:, 0], pixels[:, -1]])
        background = np.median(border, axis=0)
        mask = np.linalg.norm(pixels - background, axis=2) > 40

        fg = pixels[mask] if mask.any() else pixels.reshape(-1, 3)
        bins = np.minimum((fg // 64).astype(int), 3)
        color = np.bincount(bins[:, 0] * 16 + bins[:, 1] * 4 + bins[:, 2], minlength=64)

        shape = mask.reshape(8, SIZE // 8, 8, SIZE // 8).mean(axis=(1, 3)).ravel()

        return np.concatenate([_unit(color.astype(float)), _unit(shape)])


def _unit(v):
    n = np.linalg.norm(v)
    return v / n if n else v
