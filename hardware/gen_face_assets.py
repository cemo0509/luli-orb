# -*- coding: utf-8 -*-
"""生成「一滴光」面部所需的 3 张固件资源（PNG，带 alpha）。
用法： python hardware/gen_face_assets.py
输出： luli-orb/firmware/assets/bloom.png  hot.png  glint.png
"""
import os, math
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'firmware', 'assets')
os.makedirs(OUT, exist_ok=True)


def ellipse_glow(w, h, k):
    """椭圆高斯柔光：alpha = exp(-k * r²)，r 为归一化到 [0,1] 的椭圆半径"""
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    px = img.load()
    cx, cy = (w - 1) / 2.0, (h - 1) / 2.0
    for y in range(h):
        for x in range(w):
            rx = (x - cx) / cx
            ry = (y - cy) / cy
            r2 = rx * rx + ry * ry
            if r2 >= 1.0:
                continue
            a = math.exp(-k * r2)
            px[x, y] = (255, 255, 255, int(round(a * 255)))
    return img


def glint(w, h):
    """竖向玻璃高光：上端淡入、中上最亮、下端淡出；左右边缘更淡"""
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    px = img.load()
    # 纵向 profile（对应设计稿 0 / .22 / .72 / 1 四个 stop）
    def prof(t):
        if t <= 0.22:
            return 0.62 * (t / 0.22)
        if t <= 0.72:
            return 0.62 + (0.30 - 0.62) * ((t - 0.22) / 0.50)
        return 0.30 * (1 - (t - 0.72) / 0.28)
    for y in range(h):
        a0 = max(0.0, min(1.0, prof(y / (h - 1.0))))
        for x in range(w):
            # 横向余弦衰减，两端 55%
            fx = 0.55 + 0.45 * math.sin(math.pi * (x + 0.5) / w)
            px[x, y] = (255, 255, 255, int(round(a0 * fx * 255)))
    return img


def main():
    bloom = ellipse_glow(96, 192, 2.0)     # 外发光
    hot   = ellipse_glow(80, 80, 2.6)      # 内部光源
    gl    = glint(8, 130)                  # 偏置高光

    for name, im in (('bloom', bloom), ('hot', hot), ('glint', gl)):
        p = os.path.join(OUT, name + '.png')
        im.save(p)
        print('  %-8s %3d×%-3d  %5.1f KB' % (name, im.width, im.height, os.path.getsize(p) / 1024))

    # 预览图（叠在黑底上，方便肉眼检查）
    prev = Image.new('RGB', (420, 240), (0, 0, 0))
    b = Image.new('RGBA', (96, 192), (138, 240, 250, 255))
    b.putalpha(bloom.split()[3].point(lambda v: int(v * 0.55)))
    prev.paste(b, (12, 24), b)
    h2 = Image.new('RGBA', (80, 80), (244, 255, 255, 255))
    h2.putalpha(hot.split()[3])
    prev.paste(h2, (130, 80), h2)
    g = Image.new('RGBA', (8, 130), (255, 255, 255, 255))
    g.putalpha(gl.split()[3])
    g = g.resize((24, 130), Image.NEAREST)
    prev.paste(g, (236, 55), g)
    prev.save(os.path.join(OUT, '_preview.png'))
    print('  预览已存 firmware/assets/_preview.png')


if __name__ == '__main__':
    main()
