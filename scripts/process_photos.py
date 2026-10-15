#!/usr/bin/env python3
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

SRC = Path("/Users/chewatkins/.cursor/projects/Users-chewatkins-Projects-Villa-Giaggioli/assets")
DEST = Path("/Users/chewatkins/Projects/Villa-Giaggioli/media")
DEST.mkdir(parents=True, exist_ok=True)

PHOTOS = {
    "house-facade.jpg": "8EC0D23A-BC77-4A81-90EB-E1AFFDF8A4E2_1_105_c-f0a9e9f9-87a5-4c56-97d1-0b18608d99f2.png",
    "courtyard.jpg": "B2B6EB8C-C3E3-4622-82BD-85D14DC37FFF_1_105_c-6b960182-bc66-4b22-aa16-b8703d424328.png",
    "olives-view.jpg": "3E0AA468-4167-4CC8-B619-E7B3586D42D1_1_105_c-9388d906-630c-4222-a148-5b1741fc2c84.png",
    "courtyard-stone.jpg": "0F28D664-B7A2-49E4-92DA-330B72A257C1_1_105_c-5b03ba64-1b60-49ee-96c9-7a190637749c.png",
    "cottage.jpg": "B7A79D19-D851-44D5-97C4-8E70C8B2FA30_1_105_c-dedd4ed7-9d85-4df1-a995-74f20aac40bd.png",
    "stone-wall.jpg": "D4DD0BC2-B0F4-4773-BE17-86F311287931_1_105_c-ec489c32-ad45-446b-a4dc-3583bef24d1a.png",
    "garden-path.jpg": "F75B72BD-E37A-450F-9F2E-AC1699177DD8_1_105_c-e980b68e-f467-4bc2-bb35-af8fd8304901.png",
    "patio.jpg": "41774C0E-9131-476B-8989-388582F08427_1_105_c-79c051e9-a7cb-43c2-a825-f09ca2eea880.png",
    "fountain.jpg": "952BD6B8-363B-4983-82AE-FA10E17076C8_1_105_c-4f0a1c8c-5c5c-4e07-a5ac-5e076c1dfdca.png",
    "dining-room.jpg": "CF3981A5-CEB8-4FB8-86B2-45F3D88214B5_1_105_c-2e829eac-9eda-4f12-8fbc-1ffd05754846.png",
    "long-table.jpg": "1C8AAA78-296C-443D-87DC-4969DCF0E330_1_105_c-e4345b98-6ff7-4dd2-bda5-b7735d53d5dd.png",
    "terrace.jpg": "78E7C77F-730E-4F5E-8789-BBED1B4C3184_1_105_c-7edb0974-abdd-430c-ba67-4c5bb6d96934.png",
    "aperitivo.jpg": "3A817A4A-8C05-4826-9B2D-65DB84A86105_1_105_c-18ee1d42-c5d4-40f0-959d-b777ab531bb5.png",
    "table-evening.jpg": "5FFD0979-C346-47A9-85FF-B1F71124982F_1_105_c-fb5856a4-f410-48a6-b9dc-3d5db6e9ddd6.png",
    "bruschetta.jpg": "69B43BD8-7361-48E8-BEE7-10265A416236_1_105_c-a6b3aabd-ae4e-4f13-8796-23531e386d9d.png",
    "approach.jpg": "CEE7E6E2-EB80-41D5-9F75-FFB6820E4ACC_1_105_c-6a663732-01a6-44e9-a422-fed5c2054279.png",
    "road.jpg": "BFE869C9-37A7-4C62-8C61-89B0B68E69CC_1_105_c-9f4d1929-0922-4578-bd01-8eb8ac94e38d.png",
}


def _is_album_strip(strip: np.ndarray) -> bool:
    return float(strip.std()) < 30 and float(strip.mean()) < 85


def crop_album(im: Image.Image) -> Image.Image:
    arr = np.asarray(im.convert("RGB"))
    lum = arr.mean(axis=2)
    height, width = lum.shape
    mid_x0, mid_x1 = int(width * 0.22), int(width * 0.78)
    mid_y0, mid_y1 = int(height * 0.22), int(height * 0.78)

    top = 0
    while top < height * 0.32 and _is_album_strip(lum[top, mid_x0:mid_x1]):
        top += 1
    bottom = height - 1
    while bottom > height * 0.68 and _is_album_strip(lum[bottom, mid_x0:mid_x1]):
        bottom -= 1
    left = 0
    while left < width * 0.32 and _is_album_strip(lum[mid_y0:mid_y1, left]):
        left += 1
    right = width - 1
    while right > width * 0.68 and _is_album_strip(lum[mid_y0:mid_y1, right]):
        right -= 1

    if right - left < width * 0.45 or bottom - top < height * 0.45:
        return im

    inset = max(10, int(min(bottom - top, right - left) * 0.018))
    box = (left + inset, top + inset, right - inset + 1, bottom - inset + 1)
    return im.crop(box)


def save_web(im: Image.Image, dest: Path, max_edge: int = 2000) -> None:
    im = ImageOps.exif_transpose(im)
    im = im.convert("RGB")
    im.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
    im.save(dest, "JPEG", quality=86, optimize=True, progressive=True)


def main() -> None:
    for name, filename in PHOTOS.items():
        src = SRC / filename
        if not src.exists():
            print(f"missing {filename}")
            continue
        im = Image.open(src)
        cropped = crop_album(im)
        dest = DEST / name
        save_web(cropped, dest)
        print(f"{name}: {cropped.size[0]}x{cropped.size[1]} -> {dest.stat().st_size // 1024}kb")


if __name__ == "__main__":
    main()
