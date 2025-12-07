from pathlib import Path

import torch
from loguru import logger
from torchvision.io import decode_image
from torchvision.transforms import v2

torch.manual_seed(1)

def main():
    img = decode_image(str(Path(__file__).parent / "assets/astronaut.jpg"))
    logger.info(f"{type(img)=}, {img.dtype=}, {img.shape=}")
    transforms = v2.Compose([
        v2.RandomResizedCrop(size=(224, 224), antialias=True),
        v2.RandomHorizontalFlip(p=0.5),
        v2.ToDtype(torch.float32, scale=True),
        v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    out = transforms(img)
    logger.info(f"{type(out)=}, {out.dtype=}, {out.shape=}")

if __name__ == "__main__":
    main()
