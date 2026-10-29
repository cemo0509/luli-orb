# -*- coding: utf-8 -*-
"""实心半球（平背）方案的关键尺寸。
用法： python hardware/hemisphere.py            # 列出 60~110 全部
       python hardware/hemisphere.py 80         # 只算 Ø80
"""
import sys, math

SCREEN_D = 1.75 * 25.4      # 1.75" 屏有效显示区 Ø44.4
SCREEN_PX = 466
MM_PER_PX = SCREEN_D / SCREEN_PX
RHO_ACRY = 1.19
RHO_K9 = 2.51
EYE_RATIO = 0.16            # 眼高占球径（对齐参考视频）
CAP_RATIO = 0.86            # 黑遮光板占球径


def calc(D, h=None):
    """h = 球缺高度（平背到球顶的距离）。h=D/2 是标准半球，h>D/2 是 ¾ 球。"""
    if h is None:
        h = D / 2
    R = D / 2
    flat_d = 2 * math.sqrt(max(0.0, R * R - (h - R) ** 2)) if h >= R else 2 * math.sqrt(max(0.0, R * R - (R - h) ** 2))
    vol = math.pi * h * h * (3 * R - h) / 3 / 1000.0
    eye_mm = D * EYE_RATIO
    return dict(
        D=D, h=h, R=R,
        flat_d=flat_d,
        ratio=SCREEN_D / D * 100,
        cap=CAP_RATIO * D,
        eye_mm=eye_mm,
        eye_px=round(eye_mm / MM_PER_PX),
        gap=round(eye_mm * 1.34 / MM_PER_PX),
        w_acr=vol * RHO_ACRY,
        w_k9=vol * RHO_K9,
    )


def verdict(r):
    p = r['ratio']
    if p > 80:
        return '❌ 屏撑满，没有黑边'
    if p > 70:
        return '⚠️ 太满，黑边只剩 %.1fmm' % ((r['D'] - SCREEN_D) / 2)
    if p > 60:
        return '⚠️ 勉强，黑边 %.1fmm' % ((r['D'] - SCREEN_D) / 2)
    return '✅ 黑边 %.1fmm，比例接近参考' % ((r['D'] - SCREEN_D) / 2)


def show(r):
    print('  Ø%-4.0f h=%-4.1f 平面Ø%5.1f 屏占比%4.0f%% 遮光板Ø%4.1f 眼高%4.1fmm(%3dpx) 中心距%3dpx '
          '亚克力%3.0fg K9%4.0fg  %s'
          % (r['D'], r['h'], r['flat_d'], r['ratio'], r['cap'], r['eye_mm'], r['eye_px'], r['gap'],
             r['w_acr'], r['w_k9'], verdict(r)))


if __name__ == '__main__':
    print('屏：1.75" 466px，有效区 Ø%.1fmm，1px=%.4fmm\n' % (SCREEN_D, MM_PER_PX))
    if len(sys.argv) > 1:
        for a in sys.argv[1:]:
            d = float(a)
            r = calc(d)
            print('球径 Ø%.0f（标准半球 h=D/2）' % d)
            for k, v in r.items():
                print('   %-8s %.2f' % (k, v))
            print('   →', verdict(r))
    else:
        print('  标准半球（平背过球心）')
        print('  %-6s %-6s %-7s %-8s %-8s %-9s %-7s %-9s %s' % ('球径', '高度', '平面', '屏占比', '遮光板', '眼高', '中心距', '重量', '结论'))
        for D in (50, 60, 70, 80, 90, 100, 110):
            show(calc(D))
        print('\n  ¾ 球（平背在球心后 0.18D，侧面更包裹）')
        print('  %-6s %-6s %-7s %-8s %-8s %-9s %-7s %-9s %s' % ('球径', '高度', '平面', '屏占比', '遮光板', '眼高', '中心距', '重量', '结论'))
        for D in (70, 80, 100):
            show(calc(D, h=D * 0.68))
