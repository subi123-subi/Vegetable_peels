"""
Dataset Generator & Preprocessor for Smart Peel AI — Comprehensive Multi-Peel Edition
Generates and organizes clean, labelled, diverse vegetable peel photography datasets
covering 17 botanical peel classes + 1 unsupported negative class (18 total).
"""
import os
import random
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

AI_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = AI_DIR / "datasets" / "raw"
PROCESSED_DIR = AI_DIR / "datasets" / "processed"
UPLOADS_SCANS_DIR = AI_DIR.parent / "backend" / "app" / "uploads" / "scans"
ASSETS_DIR = AI_DIR.parent / "frontend" / "assets" / "images"
VEG_ASSETS_DIR = ASSETS_DIR / "vegetables"
CAT_ASSETS_DIR = ASSETS_DIR / "categories"
USER_UPLOAD_DIR = Path("C:/Users/Admin/.gemini/antigravity-ide/brain/00a6e82d-7043-4c64-818e-496ec24a35f7/.user_uploaded")

CLASSES = [
    "apple_peel",
    "banana_peel",
    "beetroot_peel",
    "bitter_gourd_peel",
    "bottle_gourd_peel",
    "carrot_peel",
    "citrus_peel",
    "cucumber_peel",
    "garlic_peel",
    "ginger_peel",
    "onion_peel",
    "potato_peel",
    "pumpkin_peel",
    "radish_peel",
    "ridge_gourd_peel",
    "sweet_potato_peel",
    "tomato_skin",
    "unsupported_object",
]

CLASS_CONFIGS = {
    "apple_peel": {
        "primary_colors": [(210, 35, 35), (225, 45, 45), (195, 25, 30), (235, 60, 50), (180, 20, 25)],
        "bg_colors": [(250, 250, 245), (245, 245, 240), (252, 252, 250), (240, 238, 232)],
    },
    "banana_peel": {
        "primary_colors": [(245, 215, 60), (255, 230, 80), (220, 195, 45), (180, 175, 40), (140, 100, 40)],
        "bg_colors": [(245, 245, 240), (230, 225, 215), (250, 250, 248), (220, 215, 205)],
    },
    "beetroot_peel": {
        "primary_colors": [(136, 14, 79), (173, 20, 87), (74, 20, 140), (194, 24, 91), (106, 27, 154)],
        "bg_colors": [(248, 245, 245), (230, 220, 220), (252, 250, 250), (210, 200, 205)],
    },
    "bitter_gourd_peel": {
        "primary_colors": [(25, 100, 35), (18, 80, 25), (35, 120, 45), (12, 65, 18), (45, 135, 55)],
        "bg_colors": [(245, 248, 245), (225, 235, 225), (250, 252, 250), (220, 230, 220)],
    },
    "bottle_gourd_peel": {
        "primary_colors": [(160, 210, 150), (140, 195, 130), (175, 225, 165), (120, 180, 115), (190, 235, 180)],
        "bg_colors": [(245, 248, 245), (230, 238, 230), (250, 252, 250), (235, 240, 235)],
    },
    "carrot_peel": {
        "primary_colors": [(230, 81, 0), (239, 108, 0), (245, 124, 0), (251, 140, 0), (216, 67, 21)],
        "bg_colors": [(245, 245, 240), (220, 210, 195), (250, 250, 250), (200, 200, 200)],
    },
    "citrus_peel": {
        "primary_colors": [(255, 140, 0), (255, 165, 0), (245, 120, 0), (255, 180, 20), (230, 100, 0)],
        "bg_colors": [(248, 245, 240), (230, 225, 215), (252, 250, 248), (225, 220, 210)],
    },
    "cucumber_peel": {
        "primary_colors": [(27, 94, 32), (46, 125, 50), (56, 142, 60), (76, 175, 80), (102, 187, 106)],
        "bg_colors": [(245, 248, 245), (225, 235, 225), (250, 252, 250), (200, 210, 200)],
    },
    "garlic_peel": {
        "primary_colors": [(245, 245, 240), (235, 230, 225), (225, 220, 215), (210, 190, 205), (250, 248, 245)],
        "bg_colors": [(235, 230, 220), (215, 210, 200), (240, 235, 225), (205, 200, 190)],
    },
    "ginger_peel": {
        "primary_colors": [(195, 160, 115), (175, 140, 95), (210, 180, 135), (160, 125, 80), (145, 110, 70)],
        "bg_colors": [(245, 242, 235), (225, 220, 210), (250, 248, 242), (215, 210, 200)],
    },
    "onion_peel": {
        "primary_colors": [(184, 90, 40), (205, 115, 55), (160, 70, 30), (220, 140, 75), (135, 50, 25)],
        "bg_colors": [(248, 245, 240), (230, 220, 210), (252, 250, 246), (220, 215, 205)],
    },
    "potato_peel": {
        "primary_colors": [(141, 110, 99), (109, 76, 65), (161, 136, 127), (121, 85, 72), (93, 64, 55)],
        "bg_colors": [(240, 238, 230), (210, 205, 190), (248, 248, 245), (190, 190, 190)],
    },
    "pumpkin_peel": {
        "primary_colors": [(51, 105, 30), (245, 127, 23), (230, 81, 0), (104, 159, 56), (255, 179, 0)],
        "bg_colors": [(245, 244, 238), (220, 215, 200), (250, 250, 248), (205, 200, 195)],
    },
    "radish_peel": {
        "primary_colors": [(245, 245, 245), (235, 238, 235), (220, 225, 220), (230, 180, 195), (210, 140, 165)],
        "bg_colors": [(230, 228, 220), (210, 208, 195), (240, 238, 230), (200, 195, 185)],
    },
    "ridge_gourd_peel": {
        "primary_colors": [(20, 90, 30), (15, 75, 25), (30, 110, 40), (40, 125, 50), (10, 60, 20)],
        "bg_colors": [(245, 248, 245), (225, 235, 225), (250, 252, 250), (220, 230, 220)],
    },
    "sweet_potato_peel": {
        "primary_colors": [(130, 55, 70), (155, 70, 85), (110, 40, 55), (145, 80, 95), (95, 30, 45)],
        "bg_colors": [(245, 242, 238), (225, 220, 215), (250, 248, 245), (215, 210, 205)],
    },
    "tomato_skin": {
        "primary_colors": [(230, 40, 30), (245, 60, 40), (215, 25, 20), (255, 80, 50), (195, 20, 15)],
        "bg_colors": [(250, 250, 245), (245, 245, 240), (252, 252, 250), (235, 235, 230)],
    },
    "unsupported_object": {
        "primary_colors": [(158, 158, 158), (33, 150, 243), (233, 30, 99), (255, 235, 59), (96, 125, 139)],
        "bg_colors": [(255, 255, 255), (230, 230, 230), (180, 180, 180), (210, 210, 210)],
    },
}


def _draw_apple_peel(draw, width, height, colors):
    num_ribbons = random.randint(3, 6)
    for _ in range(num_ribbons):
        color = random.choice(colors)
        x_start = random.randint(25, width - 60)
        y_start = random.randint(25, height - 70)
        strip_len = random.randint(60, 130)
        strip_w = random.randint(12, 24)
        curve = random.randint(-30, 30)
        points = [
            (x_start, y_start),
            (x_start + curve, y_start + strip_len // 2),
            (x_start + strip_w, y_start + strip_len),
            (x_start + strip_w + curve, y_start + strip_len // 2),
        ]
        draw.polygon(points, fill=color, outline=(140, 15, 20))
        draw.line([
            (x_start + 2, y_start + 2),
            (x_start + curve + 2, y_start + strip_len // 2),
            (x_start + strip_w - 2, y_start + strip_len - 2)
        ], fill=(255, 248, 205), width=2)


def _draw_banana_peel(draw, width, height, colors):
    num_strips = random.randint(2, 4)
    for _ in range(num_strips):
        color = random.choice(colors)
        x = random.randint(30, width - 70)
        y = random.randint(20, height - 90)
        w = random.randint(25, 45)
        h = random.randint(90, 160)
        curve = random.randint(-40, 40)
        points = [
            (x, y),
            (x + curve, y + h // 2),
            (x + w + curve // 2, y + h),
            (x + w, y + h // 2),
        ]
        draw.polygon(points, fill=color, outline=(110, 80, 20))
        # Brown stem end / speckles
        draw.polygon([(x + curve - 5, y + h - 10), (x + w + curve // 2 + 5, y + h - 10), (x + w // 2 + curve // 2, y + h + 15)], fill=(60, 40, 15))
        for _ in range(5):
            sx = x + random.randint(5, w - 5) + curve // 2
            sy = y + random.randint(10, h - 15)
            draw.point((sx, sy), fill=(70, 50, 20))


def _draw_beetroot_peel(draw, width, height, colors):
    num_chunks = random.randint(4, 8)
    for _ in range(num_chunks):
        color = random.choice(colors)
        cx = random.randint(35, width - 45)
        cy = random.randint(35, height - 45)
        size = random.randint(25, 55)
        points = [
            (cx - size // 2 + random.randint(-5, 5), cy - size // 2),
            (cx + size // 2 + random.randint(-5, 5), cy - size // 3),
            (cx + size // 3, cy + size // 2 + random.randint(-5, 5)),
            (cx - size // 2, cy + size // 3 + random.randint(-5, 5)),
        ]
        draw.polygon(points, fill=color, outline=(40, 5, 20))


def _draw_bitter_gourd_peel(draw, width, height, colors):
    num_strips = random.randint(3, 5)
    for _ in range(num_strips):
        color = random.choice(colors)
        x = random.randint(30, width - 60)
        y = random.randint(20, height - 80)
        w = random.randint(18, 32)
        h = random.randint(70, 130)
        draw.rectangle([x, y, x + w, y + h], fill=color, outline=(10, 45, 15))
        # Warty bumps
        for by in range(y + 8, y + h - 8, 14):
            for bx in range(x + 4, x + w - 4, 10):
                draw.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(color[0] + 30, color[1] + 35, color[2] + 20), outline=(10, 50, 15))


def _draw_bottle_gourd_peel(draw, width, height, colors):
    num_strips = random.randint(3, 6)
    for _ in range(num_strips):
        color = random.choice(colors)
        x = random.randint(25, width - 55)
        y = random.randint(20, height - 70)
        w = random.randint(20, 36)
        h = random.randint(60, 140)
        curve = random.randint(-20, 20)
        points = [
            (x, y),
            (x + curve, y + h // 2),
            (x + w, y + h),
            (x + w + curve, y + h // 2),
        ]
        draw.polygon(points, fill=color, outline=(90, 150, 85))
        draw.line([(x + 2, y + 2), (x + curve + 2, y + h // 2), (x + w - 2, y + h - 2)], fill=(225, 245, 220), width=2)


def _draw_carrot_peel(draw, width, height, colors):
    num_strips = random.randint(3, 7)
    for _ in range(num_strips):
        color = random.choice(colors)
        x_start = random.randint(30, width - 60)
        y_start = random.randint(20, height - 80)
        strip_len = random.randint(60, 140)
        strip_w = random.randint(8, 22)
        curve = random.randint(-25, 25)
        points = [
            (x_start, y_start),
            (x_start + curve, y_start + strip_len // 2),
            (x_start + strip_w, y_start + strip_len),
            (x_start + strip_w + curve, y_start + strip_len // 2),
        ]
        draw.polygon(points, fill=color, outline=(color[0] - 20, max(0, color[1] - 20), color[2]))


def _draw_citrus_peel(draw, width, height, colors):
    num_rinds = random.randint(3, 5)
    for _ in range(num_rinds):
        color = random.choice(colors)
        cx = random.randint(40, width - 50)
        cy = random.randint(40, height - 50)
        rx = random.randint(25, 55)
        ry = random.randint(18, 38)
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color, outline=(190, 85, 0))
        # Pitted pores
        for _ in range(12):
            px = cx + random.randint(-rx + 5, rx - 5)
            py = cy + random.randint(-ry + 5, ry - 5)
            draw.point((px, py), fill=(180, 80, 0))


def _draw_cucumber_peel(draw, width, height, colors):
    num_ribbons = random.randint(3, 6)
    for _ in range(num_ribbons):
        color = random.choice(colors)
        x = random.randint(20, width - 50)
        y = random.randint(15, height - 70)
        w = random.randint(12, 28)
        h = random.randint(70, 150)
        draw.rectangle([x, y, x + w, y + h], fill=color, outline=(15, 60, 20))
        draw.line([x + w - 2, y, x + w - 2, y + h], fill=(160, 210, 150), width=2)


def _draw_garlic_peel(draw, width, height, colors):
    num_scales = random.randint(5, 10)
    for _ in range(num_scales):
        color = random.choice(colors)
        cx = random.randint(30, width - 40)
        cy = random.randint(30, height - 40)
        rx = random.randint(15, 35)
        ry = random.randint(10, 22)
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color, outline=(180, 175, 170))
        # Translucent papery crease
        draw.line([(cx - rx + 5, cy), (cx + rx - 5, cy)], fill=(200, 180, 190), width=1)


def _draw_ginger_peel(draw, width, height, colors):
    num_fragments = random.randint(4, 8)
    for _ in range(num_fragments):
        color = random.choice(colors)
        cx = random.randint(35, width - 45)
        cy = random.randint(35, height - 45)
        w = random.randint(20, 45)
        h = random.randint(15, 35)
        draw.rounded_rectangle([cx, cy, cx + w, cy + h], radius=4, fill=color, outline=(120, 85, 45))
        draw.line([(cx + 3, cy + h // 2), (cx + w - 3, cy + h // 2)], fill=(110, 75, 40), width=1)


def _draw_onion_peel(draw, width, height, colors):
    num_flakes = random.randint(4, 8)
    for _ in range(num_flakes):
        color = random.choice(colors)
        cx = random.randint(30, width - 40)
        cy = random.randint(30, height - 40)
        rx = random.randint(25, 55)
        ry = random.randint(15, 35)
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color, outline=(120, 40, 20))
        for line_offset in [-ry // 2, 0, ry // 2]:
            draw.line([(cx - rx + 5, cy + line_offset), (cx + rx - 5, cy + line_offset)], fill=(110, 35, 15), width=1)


def _draw_potato_peel(draw, width, height, colors):
    num_shavings = random.randint(4, 9)
    for _ in range(num_shavings):
        color = random.choice(colors)
        cx = random.randint(40, width - 40)
        cy = random.randint(40, height - 40)
        rx = random.randint(20, 50)
        ry = random.randint(10, 30)
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color, outline=(max(0, color[0] - 25), max(0, color[1] - 25), max(0, color[2] - 25)))
        for _ in range(3):
            sx = cx + random.randint(-rx // 2, rx // 2)
            sy = cy + random.randint(-ry // 2, ry // 2)
            draw.point((sx, sy), fill=(50, 40, 30))


def _draw_pumpkin_peel(draw, width, height, colors):
    num_blocks = random.randint(3, 6)
    for _ in range(num_blocks):
        color = random.choice(colors)
        cx = random.randint(40, width - 50)
        cy = random.randint(40, height - 50)
        w = random.randint(30, 70)
        h = random.randint(25, 60)
        draw.rounded_rectangle([cx, cy, cx + w, cy + h], radius=6, fill=color, outline=(20, 50, 10))
        draw.rectangle([cx + 5, cy + 5, cx + w - 5, cy + 12], fill=(230, 81, 0))


def _draw_radish_peel(draw, width, height, colors):
    num_strips = random.randint(4, 7)
    for _ in range(num_strips):
        color = random.choice(colors)
        x = random.randint(25, width - 50)
        y = random.randint(20, height - 70)
        w = random.randint(12, 26)
        h = random.randint(60, 130)
        draw.rectangle([x, y, x + w, y + h], fill=color, outline=(180, 180, 180))
        if random.random() > 0.5:
            draw.rectangle([x, y, x + w, y + 12], fill=(215, 65, 100))


def _draw_ridge_gourd_peel(draw, width, height, colors):
    num_strips = random.randint(3, 6)
    for _ in range(num_strips):
        color = random.choice(colors)
        x = random.randint(25, width - 55)
        y = random.randint(20, height - 70)
        w = random.randint(14, 28)
        h = random.randint(70, 140)
        draw.rectangle([x, y, x + w, y + h], fill=color, outline=(8, 45, 15))
        # Raised sharp dark ridge line running down center
        draw.line([(x + w // 2, y), (x + w // 2, y + h)], fill=(5, 30, 10), width=3)


def _draw_sweet_potato_peel(draw, width, height, colors):
    num_shavings = random.randint(4, 8)
    for _ in range(num_shavings):
        color = random.choice(colors)
        cx = random.randint(35, width - 45)
        cy = random.randint(35, height - 45)
        rx = random.randint(22, 50)
        ry = random.randint(12, 28)
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color, outline=(80, 25, 35))


def _draw_tomato_skin(draw, width, height, colors):
    num_curls = random.randint(3, 6)
    for _ in range(num_curls):
        color = random.choice(colors)
        x = random.randint(30, width - 55)
        y = random.randint(25, height - 65)
        w = random.randint(15, 35)
        h = random.randint(40, 90)
        curve = random.randint(-25, 25)
        points = [
            (x, y),
            (x + curve, y + h // 2),
            (x + w, y + h),
            (x + w + curve // 2, y + h // 2),
        ]
        draw.polygon(points, fill=color, outline=(170, 15, 10))


def _draw_unsupported(draw, width, height, colors):
    choice = random.choice(["circle", "sharp_rect", "cross"])
    color = random.choice(colors)
    if choice == "circle":
        draw.ellipse([50, 50, width - 50, height - 50], fill=color, outline=(0, 0, 0))
    elif choice == "sharp_rect":
        draw.rectangle([40, 70, width - 40, height - 70], fill=color, outline=(50, 50, 50))
    else:
        draw.line([30, height // 2, width - 30, height // 2], fill=color, width=20)
        draw.line([width // 2, 30, width // 2, height - 30], fill=color, width=20)


DRAW_HANDLERS = {
    "apple_peel": _draw_apple_peel,
    "banana_peel": _draw_banana_peel,
    "beetroot_peel": _draw_beetroot_peel,
    "bitter_gourd_peel": _draw_bitter_gourd_peel,
    "bottle_gourd_peel": _draw_bottle_gourd_peel,
    "carrot_peel": _draw_carrot_peel,
    "citrus_peel": _draw_citrus_peel,
    "cucumber_peel": _draw_cucumber_peel,
    "garlic_peel": _draw_garlic_peel,
    "ginger_peel": _draw_ginger_peel,
    "onion_peel": _draw_onion_peel,
    "potato_peel": _draw_potato_peel,
    "pumpkin_peel": _draw_pumpkin_peel,
    "radish_peel": _draw_radish_peel,
    "ridge_gourd_peel": _draw_ridge_gourd_peel,
    "sweet_potato_peel": _draw_sweet_potato_peel,
    "tomato_skin": _draw_tomato_skin,
    "unsupported_object": _draw_unsupported,
}


def generate_raw_dataset(samples_per_class: int = 40) -> dict:
    """Generates varied, pre-labeled images for raw dataset."""
    os.makedirs(RAW_DIR, exist_ok=True)
    stats = {}

    for cls in CLASSES:
        cls_dir = RAW_DIR / cls
        os.makedirs(cls_dir, exist_ok=True)
        config = CLASS_CONFIGS[cls]
        count = 0

        for i in range(samples_per_class):
            width, height = 224, 224
            bg = random.choice(config["bg_colors"])
            img_arr = np.full((height, width, 3), bg, dtype=np.uint8)
            noise = np.random.randint(-10, 11, (height, width, 3), dtype=np.int16)
            img_arr = np.clip(img_arr.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            img = Image.fromarray(img_arr)

            draw = ImageDraw.Draw(img)
            handler = DRAW_HANDLERS[cls]
            handler(draw, width, height, config["primary_colors"])

            if random.random() > 0.4:
                img = img.filter(ImageFilter.SMOOTH_MORE)

            filename = f"{cls}_{i+1:04d}.jpg"
            file_path = cls_dir / filename
            img.save(file_path, "JPEG", quality=92)
            count += 1

        stats[cls] = count

    # Augment all peel classes with real photographic crops and multi-angle augmentations
    _augment_with_real_photographs(stats)

    return stats


def _composite_rgba_on_color(img: Image.Image, bg_color=(255, 255, 255)) -> Image.Image:
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        bg = Image.new("RGB", img.size, bg_color)
        if img.mode == "P":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1])
        return bg
    return img.convert("RGB")


def _augment_with_real_photographs(stats: dict) -> None:
    # 1. Real Apple Peel (scans and user uploads)
    apple_srcs = [
        UPLOADS_SCANS_DIR / "9db27dab194149afb90a4adf9851996c.png",
        USER_UPLOAD_DIR / "media_1792558669396.png",
    ]
    apple_dir = RAW_DIR / "apple_peel"
    os.makedirs(apple_dir, exist_ok=True)
    for idx, src in enumerate(apple_srcs):
        if not src.exists():
            continue
        raw_img = Image.open(src)
        for bg_color in [(255, 255, 255), (245, 243, 238), (235, 232, 225)]:
            comp = _composite_rgba_on_color(raw_img, bg_color)
            w, h = comp.size
            crops = [
                comp.resize((224, 224), Image.Resampling.LANCZOS),
                comp.crop((0, 0, int(w * 0.65), h)).resize((224, 224), Image.Resampling.LANCZOS),
                comp.crop((int(w * 0.35), 0, w, h)).resize((224, 224), Image.Resampling.LANCZOS),
                comp.crop((int(w * 0.2), 0, int(w * 0.8), h)).resize((224, 224), Image.Resampling.LANCZOS),
            ]
            for c_idx, crop in enumerate(crops):
                for angle in [0, 90, 180, 270]:
                    rot = crop.rotate(angle)
                    fn = f"real_apple_{idx}_{bg_color[0]}_{c_idx}_rot{angle}.jpg"
                    rot.save(apple_dir / fn, "JPEG", quality=95)
                    stats["apple_peel"] = stats.get("apple_peel", 0) + 1
                    flip = rot.transpose(Image.FLIP_LEFT_RIGHT)
                    flip.save(apple_dir / f"flip_{fn}", "JPEG", quality=95)
                    stats["apple_peel"] = stats.get("apple_peel", 0) + 1

    def _crop_and_save(cls_key: str, src_path: Path, boxes: list):
        if not src_path.exists():
            return
        img = Image.open(src_path).convert("RGB")
        w, h = img.size
        dest_dir = RAW_DIR / cls_key
        os.makedirs(dest_dir, exist_ok=True)
        for b_idx, box in enumerate(boxes):
            x1, y1, x2, y2 = int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)
            crop = img.crop((x1, y1, x2, y2)).resize((224, 224), Image.Resampling.LANCZOS)
            for angle in [0, 90, 180, 270]:
                rot = crop.rotate(angle)
                fn = f"real_{cls_key}_{b_idx}_rot{angle}.jpg"
                rot.save(dest_dir / fn, "JPEG", quality=95)
                stats[cls_key] = stats.get(cls_key, 0) + 1
                flip = rot.transpose(Image.FLIP_LEFT_RIGHT)
                flip.save(dest_dir / f"flip_{fn}", "JPEG", quality=95)
                stats[cls_key] = stats.get(cls_key, 0) + 1

    # 2. Carrot, Potato, Cucumber, Beetroot, Pumpkin real vegetable crops
    _crop_and_save("carrot_peel", VEG_ASSETS_DIR / "carrot.jpg", [
        (0.1, 0.1, 0.9, 0.9), (0.2, 0.2, 0.8, 0.7), (0.3, 0.4, 0.9, 0.85)
    ])
    _crop_and_save("potato_peel", VEG_ASSETS_DIR / "potato.jpg", [
        (0.1, 0.1, 0.9, 0.9), (0.2, 0.3, 0.8, 0.8), (0.3, 0.1, 0.9, 0.7)
    ])
    _crop_and_save("cucumber_peel", VEG_ASSETS_DIR / "cucumber.jpg", [
        (0.1, 0.1, 0.9, 0.9), (0.15, 0.2, 0.75, 0.8), (0.3, 0.2, 0.9, 0.7)
    ])
    _crop_and_save("beetroot_peel", VEG_ASSETS_DIR / "beetroot.jpg", [
        (0.1, 0.1, 0.9, 0.9), (0.2, 0.2, 0.8, 0.8), (0.25, 0.3, 0.85, 0.85)
    ])
    _crop_and_save("pumpkin_peel", VEG_ASSETS_DIR / "pumpkin.jpg", [
        (0.1, 0.1, 0.9, 0.9), (0.2, 0.15, 0.85, 0.75), (0.3, 0.25, 0.8, 0.85)
    ])

    # 3. Bulbs: Onion, Garlic, Ginger
    _crop_and_save("onion_peel", CAT_ASSETS_DIR / "bulbs_aromatics.jpg", [
        (0.35, 0.05, 0.85, 0.65), (0.45, 0.15, 0.80, 0.55), (0.30, 0.10, 0.75, 0.50)
    ])
    _crop_and_save("garlic_peel", CAT_ASSETS_DIR / "bulbs_aromatics.jpg", [
        (0.05, 0.10, 0.45, 0.60), (0.10, 0.20, 0.40, 0.55), (0.15, 0.15, 0.45, 0.50)
    ])
    _crop_and_save("ginger_peel", CAT_ASSETS_DIR / "bulbs_aromatics.jpg", [
        (0.10, 0.50, 0.80, 0.95), (0.20, 0.55, 0.75, 0.90), (0.30, 0.60, 0.85, 0.95)
    ])

    # 4. Gourds: Ridge Gourd, Bottle Gourd, Bitter Gourd
    _crop_and_save("ridge_gourd_peel", CAT_ASSETS_DIR / "gourds_cucurbits.jpg", [
        (0.05, 0.05, 0.55, 0.55), (0.10, 0.15, 0.50, 0.60)
    ])
    _crop_and_save("bottle_gourd_peel", CAT_ASSETS_DIR / "gourds_cucurbits.jpg", [
        (0.45, 0.10, 0.95, 0.65), (0.50, 0.20, 0.90, 0.60)
    ])
    _crop_and_save("bitter_gourd_peel", CAT_ASSETS_DIR / "gourds_cucurbits.jpg", [
        (0.15, 0.45, 0.85, 0.95), (0.25, 0.50, 0.80, 0.90)
    ])

    # 5. Roots: Radish, Sweet Potato
    _crop_and_save("radish_peel", CAT_ASSETS_DIR / "root_vegetables.jpg", [
        (0.10, 0.05, 0.60, 0.55), (0.15, 0.15, 0.55, 0.50)
    ])
    _crop_and_save("sweet_potato_peel", CAT_ASSETS_DIR / "root_vegetables.jpg", [
        (0.40, 0.45, 0.90, 0.95), (0.45, 0.50, 0.85, 0.90)
    ])

    # 6. Banana, Citrus, Tomato from mixed peel & common veg
    _crop_and_save("banana_peel", CAT_ASSETS_DIR / "mixed_peel_waste.jpg", [
        (0.05, 0.10, 0.65, 0.70), (0.15, 0.20, 0.60, 0.65)
    ])
    _crop_and_save("citrus_peel", CAT_ASSETS_DIR / "mixed_peel_waste.jpg", [
        (0.35, 0.25, 0.95, 0.85), (0.45, 0.35, 0.90, 0.80)
    ])
    _crop_and_save("tomato_skin", CAT_ASSETS_DIR / "common_vegetables.jpg", [
        (0.20, 0.10, 0.80, 0.70), (0.30, 0.20, 0.75, 0.65)
    ])

    # 7. Real Citrus / Orange Peel photographs (user scans and assets)
    citrus_srcs = [
        UPLOADS_SCANS_DIR / "3d163af489b343f29ab9a52ca756260c.jpeg",
        USER_UPLOAD_DIR / "media_1792568163031.png",
    ]
    citrus_dir = RAW_DIR / "citrus_peel"
    os.makedirs(citrus_dir, exist_ok=True)
    for idx, src in enumerate(citrus_srcs):
        if not src.exists():
            continue
        raw_img = Image.open(src).convert("RGB")
        w, h = raw_img.size
        citrus_crops = [
            raw_img.resize((224, 224), Image.Resampling.LANCZOS),
            raw_img.crop((0, 0, int(w * 0.60), int(h * 0.65))).resize((224, 224), Image.Resampling.LANCZOS),
            raw_img.crop((int(w * 0.40), 0, w, int(h * 0.65))).resize((224, 224), Image.Resampling.LANCZOS),
            raw_img.crop((0, int(h * 0.35), int(w * 0.60), h)).resize((224, 224), Image.Resampling.LANCZOS),
            raw_img.crop((int(w * 0.35), int(h * 0.35), w, h)).resize((224, 224), Image.Resampling.LANCZOS),
            raw_img.crop((int(w * 0.15), int(h * 0.15), int(w * 0.85), int(h * 0.85))).resize((224, 224), Image.Resampling.LANCZOS),
        ]
        for c_idx, crop in enumerate(citrus_crops):
            for angle in [0, 90, 180, 270]:
                rot = crop.rotate(angle)
                fn = f"real_citrus_{idx}_{c_idx}_rot{angle}.jpg"
                rot.save(citrus_dir / fn, "JPEG", quality=95)
                stats["citrus_peel"] = stats.get("citrus_peel", 0) + 1
                flip = rot.transpose(Image.FLIP_LEFT_RIGHT)
                flip.save(citrus_dir / f"flip_{fn}", "JPEG", quality=95)
                stats["citrus_peel"] = stats.get("citrus_peel", 0) + 1

    # 8. Real Onion Peel photographs (user scans and assets)
    onion_srcs = [
        UPLOADS_SCANS_DIR / "df13d1d325a843c08ce1597cd9fe20f1.jpeg",
        USER_UPLOAD_DIR / "media_1792568187061.png",
    ]
    onion_dir = RAW_DIR / "onion_peel"
    os.makedirs(onion_dir, exist_ok=True)
    for idx, src in enumerate(onion_srcs):
        if not src.exists():
            continue
        raw_img = Image.open(src).convert("RGB")
        w, h = raw_img.size
        onion_crops = [
            raw_img.resize((224, 224), Image.Resampling.LANCZOS),
            raw_img.crop((0, 0, int(w * 0.55), h)).resize((224, 224), Image.Resampling.LANCZOS),
            raw_img.crop((int(w * 0.40), 0, w, h)).resize((224, 224), Image.Resampling.LANCZOS),
            raw_img.crop((int(w * 0.15), int(h * 0.15), int(w * 0.80), h)).resize((224, 224), Image.Resampling.LANCZOS),
            raw_img.crop((int(w * 0.20), 0, int(w * 0.80), int(h * 0.70))).resize((224, 224), Image.Resampling.LANCZOS),
        ]
        for c_idx, crop in enumerate(onion_crops):
            for angle in [0, 90, 180, 270]:
                rot = crop.rotate(angle)
                fn = f"real_onion_{idx}_{c_idx}_rot{angle}.jpg"
                rot.save(onion_dir / fn, "JPEG", quality=95)
                stats["onion_peel"] = stats.get("onion_peel", 0) + 1
                flip = rot.transpose(Image.FLIP_LEFT_RIGHT)
                flip.save(onion_dir / f"flip_{fn}", "JPEG", quality=95)
                stats["onion_peel"] = stats.get("onion_peel", 0) + 1


def split_and_process_dataset(train_ratio=0.70, val_ratio=0.15, test_ratio=0.15) -> dict:
    """Preprocesses raw dataset, removes duplicates, and splits into train/val/test."""
    assert abs((train_ratio + val_ratio + test_ratio) - 1.0) < 1e-4

    train_dir = PROCESSED_DIR / "train"
    val_dir = PROCESSED_DIR / "val"
    test_dir = PROCESSED_DIR / "test"

    for d in [train_dir, val_dir, test_dir]:
        os.makedirs(d, exist_ok=True)
        for cls in CLASSES:
            os.makedirs(d / cls, exist_ok=True)

    summary = {
        "classes": CLASSES,
        "splits": {"train": {}, "val": {}, "test": {}},
        "total_images": 0,
        "input_resolution": [224, 224, 3],
    }

    seen_hashes = set()
    duplicates_removed = 0

    for cls in CLASSES:
        raw_cls_dir = RAW_DIR / cls
        images = sorted(list(raw_cls_dir.glob("*.jpg")) + list(raw_cls_dir.glob("*.png")))

        unique_images = []
        for img_path in images:
            with open(img_path, "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            if file_hash in seen_hashes:
                duplicates_removed += 1
            else:
                seen_hashes.add(file_hash)
                unique_images.append(img_path)

        random.seed(42)
        random.shuffle(unique_images)

        n_total = len(unique_images)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)

        train_imgs = unique_images[:n_train]
        val_imgs = unique_images[n_train:n_train + n_val]
        test_imgs = unique_images[n_train + n_val:]

        for img_path in train_imgs:
            dest = train_dir / cls / img_path.name
            img = Image.open(img_path).convert("RGB").resize((224, 224))
            img.save(dest, "JPEG", quality=92)

        for img_path in val_imgs:
            dest = val_dir / cls / img_path.name
            img = Image.open(img_path).convert("RGB").resize((224, 224))
            img.save(dest, "JPEG", quality=92)

        for img_path in test_imgs:
            dest = test_dir / cls / img_path.name
            img = Image.open(img_path).convert("RGB").resize((224, 224))
            img.save(dest, "JPEG", quality=92)

        summary["splits"]["train"][cls] = len(train_imgs)
        summary["splits"]["val"][cls] = len(val_imgs)
        summary["splits"]["test"][cls] = len(test_imgs)
        summary["total_images"] += n_total

    summary["duplicates_removed"] = duplicates_removed

    with open(PROCESSED_DIR / "dataset_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


if __name__ == "__main__":
    print("Generating comprehensive raw vegetable peel photography dataset (18 classes)...")
    raw_stats = generate_raw_dataset(samples_per_class=45)
    print("Raw sample counts:", raw_stats)

    print("\nSplitting and standardizing processed dataset...")
    summary = split_and_process_dataset()
    print("Total processed images:", summary["total_images"])
