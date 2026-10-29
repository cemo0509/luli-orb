# -*- coding: utf-8 -*-
"""实心球当放大镜（ball lens）的光学核算。
用来判定：参考产品是「空心球+内胆」还是「实心球+屏在球后」。

球透镜（paraxial，主平面近似在球心）：
    EFL = n*R / (2*(n-1))        n=1.5 时 EFL = 1.5R
    1/f = 1/o + 1/i              o = 屏到球心的距离
    m = |i/o|                    虚像 = 屏幕上看到的大小倍数
球体把视场裁到球的轮廓，所以：
    可见屏直径 = 球外径 / m
    要眼高占球径 16%，屏上眼高 = 0.16*球径 / m
"""
N_GLASS = 1.51     # K9
N_ACRY = 1.49
RHO = {'K9': 2.51, '亚克力': 1.19}


def calc(D, n, gap, target_ratio=0.16):
    R = D / 2
    f = n * R / (2 * (n - 1))
    o = R + gap
    i = 1.0 / (1.0 / f - 1.0 / o)          # 负 = 虚像，在球后
    m = abs(i / o)
    field = D / m                            # 可见屏直径
    eye_mm = target_ratio * D / m            # 屏上应有的眼高
    return dict(D=D, n=n, gap=gap, f=f, o=o, i=i, m=m, field=field, eye_mm=eye_mm)


def mass(D, rho):
    return 4.0 / 3.0 * 3.14159265 * (D / 2) ** 3 / 1000.0 * rho   # g


if __name__ == '__main__':
    print('=' * 86)
    print('实心球当放大镜：屏贴在球后 3mm')
    print('=' * 86)
    print('  %-8s %-8s %-9s %-9s %-8s %-11s %-10s %s'
          % ('球径', 'EFL', '放大率m', '可见屏径', '眼高(屏)', '眼高(像素)', '球重', '说明'))
    for D in (60, 80, 90, 100, 110):
        r = calc(D, N_GLASS, 3)
        print('  Ø%-7.0f %-8.1f %-9.2f %-9.1f %-8.1f %-11d %-10.0f g'
              % (D, r['f'], r['m'], r['field'], r['eye_mm'],
                 round(r['eye_mm'] / 0.0954), mass(D, RHO['K9'])))

    print('\n  屏距越远，放大越狠、可见区越小（Ø100 玻璃球）')
    print('  %-8s %-9s %-10s %s' % ('屏距', '放大率', '可见屏径', '屏上眼高'))
    for gap in (0, 3, 5, 8, 12, 20):
        r = calc(100, N_GLASS, gap)
        print('  %-8.1f %-9.2f %-10.1f %.1f mm (%d px)'
              % (gap, r['m'], r['field'], r['eye_mm'], round(r['eye_mm'] / 0.0954)))

    print('\n  对比：空心薄壁球（2.5mm 壁，同心）的净光焦度 ≈ 0，放大率 ≈ 1.0')
    print('  → 透过它看屏幕，眼睛就是屏幕上的原尺寸（17.6mm = 17.6% 球径）')

    print('\n  判定实验：把球放报纸上')
    for D in (80, 100):
        r = calc(D, N_GLASS, 0)
        print('    Ø%-4.0f 实心球：字被放大约 %.1f 倍，且边缘明显变形/彩虹边' % (D, r['m']))
