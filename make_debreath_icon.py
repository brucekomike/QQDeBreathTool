from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


def rounded_rectangle_mask(size, radius):
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    return mask


def draw_icon(size):
    scale = size / 256.0
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    badge = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(badge)
    r = int(48 * scale)
    bdraw.rounded_rectangle(
        (int(12 * scale), int(12 * scale), int(244 * scale), int(244 * scale)),
        radius=r,
        fill=(18, 23, 28, 255),
        outline=(76, 88, 96, 255),
        width=max(1, int(2.5 * scale)),
    )
    bdraw.rounded_rectangle(
        (int(20 * scale), int(20 * scale), int(236 * scale), int(132 * scale)),
        radius=int(38 * scale),
        fill=(35, 44, 51, 92),
    )
    img.alpha_composite(badge)

    draw = ImageDraw.Draw(img)
    cx = size / 2
    mid = int(139 * scale)
    left = int(47 * scale)
    right = int(209 * scale)

    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse(
        (int(151 * scale), int(83 * scale), int(228 * scale), int(169 * scale)),
        fill=(76, 208, 170, 54),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(max(1, int(10 * scale))))
    img.alpha_composite(glow)
    draw = ImageDraw.Draw(img)

    if size >= 48:
        grid_pen = (63, 76, 84, 120)
        for x in [76, 116, 156, 196]:
            draw.line((int(x * scale), int(47 * scale), int(x * scale), int(205 * scale)), fill=grid_pen, width=max(1, int(scale)))
        for y in [83, 139, 195]:
            draw.line((int(45 * scale), int(y * scale), int(211 * scale), int(y * scale)), fill=grid_pen, width=max(1, int(scale)))

    band_top = int(70 * scale)
    band_bottom = int(208 * scale)
    draw.rounded_rectangle(
        (int(43 * scale), band_top, int(213 * scale), band_bottom),
        radius=int(20 * scale),
        fill=(8, 12, 16, 92),
        outline=(49, 61, 68, 185),
        width=max(1, int(1.5 * scale)),
    )

    wave = [
        (47, 144),
        (57, 144),
        (66, 128),
        (74, 161),
        (84, 104),
        (94, 186),
        (105, 92),
        (116, 172),
        (127, 124),
        (138, 139),
        (149, 111),
        (162, 166),
        (174, 99),
        (187, 154),
        (199, 141),
        (209, 141),
    ]
    pts = [(int(x * scale), int(y * scale)) for x, y in wave]
    width = max(2, int(7 * scale))
    under_width = max(width + 2, int(11 * scale))
    draw.line(pts, fill=(5, 13, 17, 230), width=under_width, joint="curve")
    draw.line(pts, fill=(64, 224, 190, 255), width=width, joint="curve")
    if size >= 64:
        draw.line(pts, fill=(196, 255, 238, 210), width=max(1, int(2 * scale)), joint="curve")

    cut_x = int(132 * scale)
    draw.line((cut_x, int(54 * scale), cut_x, int(218 * scale)), fill=(17, 19, 20, 245), width=max(3, int(13 * scale)))
    draw.line((cut_x, int(54 * scale), cut_x, int(218 * scale)), fill=(245, 182, 71, 255), width=max(2, int(6 * scale)))
    if size >= 48:
        draw.ellipse(
            (
                cut_x - int(13 * scale),
                mid - int(13 * scale),
                cut_x + int(13 * scale),
                mid + int(13 * scale),
            ),
            fill=(255, 214, 118, 255),
            outline=(20, 18, 14, 220),
            width=max(1, int(2 * scale)),
        )

    if size >= 64:
        # Two quiet "separated breath" blocks, deliberately abstract and not text.
        for x, y, w, h, color in [
            (56, 222, 44, 9, (64, 224, 190, 210)),
            (157, 222, 42, 9, (245, 182, 71, 215)),
        ]:
            draw.rounded_rectangle(
                (int(x * scale), int(y * scale), int((x + w) * scale), int((y + h) * scale)),
                radius=max(1, int(5 * scale)),
                fill=color,
            )

    return img


def main():
    sizes = [16, 24, 32, 48, 64, 128, 256]
    images = [draw_icon(size) for size in sizes]
    preview = draw_icon(512)
    preview.save("debreath_icon_preview.png")
    images[-1].save("debreath_icon.ico", sizes=[(s, s) for s in sizes], append_images=images[:-1])
    for size, image in zip(sizes, images):
        image.save(f"debreath_icon_{size}.png")
    print("wrote debreath_icon.ico and preview")


if __name__ == "__main__":
    main()
