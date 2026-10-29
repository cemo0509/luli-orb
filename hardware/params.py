# -*- coding: utf-8 -*-
"""琉璃 ORB · 参数计算器
=========================================================
所有方案的尺寸都从这里出，改这里 → 文档里的数字跟着变。
跑法： python hardware/params.py
输出： 关键尺寸表 + 眼睛在屏上的像素坐标 + OpenSCAD 参数（SCAD_PARAMS）

设计链：球壳 → 内胆 → 窗口 → 屏 → 眼睛像素 → 底座
"""
import math

# ==================== 主参数（改这里） ====================
SPHERE_OD = 110.0      # 透明球外径 mm（Ø90 / Ø110 / Ø120 三档可选）
SHELL_T   = 3.0        # 球壳壁厚（吹塑亚克力常见 2~3mm）
GAP       = 2.5        # 球壳内壁 ↔ 内胆外壁 的间隙（防蹭、防牛顿环）
DOME_T    = 2.5        # 内胆壁厚
SCREEN_IN = 1.75       # 屏尺寸（英寸·对角线/直径）
SCREEN_PX = 466        # 屏分辨率
WINDOW_D  = 47.0       # 内胆前窗开孔直径（需 < 板 Ø51、> 屏 Ø44.4）
SCREEN_SETBACK = 10.0  # 屏面到球壳内表面的距离（越大视差越强、"悬浮"越明显）
BASE_OD   = 110.0      # 底座外径
BASE_H    = 14.0       # 底座高

# 参考视频实测比例（把 592×1280 的录屏帧按球径归一化，见 docs/01）
REF_EYE_W   = 0.064    # 眼宽 / 球径
REF_EYE_H   = 0.160    # 眼高 / 球径
REF_EYE_GAP = 0.215    # 眼中心距 / 球径

# ==================== 推导 ====================
SPHERE_ID = SPHERE_OD - 2 * SHELL_T                 # 球壳内径
DOME_OD   = SPHERE_ID - 2 * GAP                     # 内胆外径
DOME_ID   = DOME_OD - 2 * DOME_T                    # 内胆内腔直径
SCREEN_D  = SCREEN_IN * 25.4                        # 屏有效显示区直径（圆屏=对角线）
PPI       = SCREEN_PX / SCREEN_IN
MM_PER_PX = SCREEN_D / SCREEN_PX
INNER_R   = DOME_ID / 2.0

# 屏面所在的 z（以球心为 0，+z 朝前）
SCREEN_Z  = SPHERE_ID / 2.0 - SCREEN_SETBACK        # 屏面到球心的距离
FACE_D    = 2 * math.sqrt(max(0.0, (DOME_OD / 2.0) ** 2 - SCREEN_Z ** 2))   # 内胆前切平面直径
BOARD_D   = 51.0       # 微雪 1.75-B 板直径（屏+主控一体，Ø51×12.1）


def eye_mm():
    return (SPHERE_OD * REF_EYE_W, SPHERE_OD * REF_EYE_H, SPHERE_OD * REF_EYE_GAP)


def report():
    ew, eh, eg = eye_mm()
    print('=' * 78)
    print('琉璃 ORB 参数表   （球 Ø%.0f，屏 %.2f" %dpx）' % (SPHERE_OD, SCREEN_IN, SCREEN_PX))
    print('=' * 78)
    rows = [
        ('球壳', '外径 Ø%.1f / 壁厚 %.1f / 内径 Ø%.1f' % (SPHERE_OD, SHELL_T, SPHERE_ID)),
        ('内胆', '外径 Ø%.1f / 壁厚 %.1f / 内腔 Ø%.1f' % (DOME_OD, DOME_T, DOME_ID)),
        ('间隙', '球壳内壁 ↔ 内胆 %.1f mm（单边）' % GAP),
        ('前窗', '开孔 Ø%.1f，屏 Ø%.1f，单边压边 %.1f' % (WINDOW_D, SCREEN_D, (WINDOW_D - SCREEN_D) / 2)),
        ('屏', '%.2f" %dpx = %.1f ppi，1px = %.4f mm' % (SCREEN_IN, SCREEN_PX, PPI, MM_PER_PX)),
        ('屏位', '屏面在球心前 %.2f mm，距球壳内表面 %.1f mm' % (SCREEN_Z, SCREEN_SETBACK)),
        ('前切面', 'Ø%.1f 平面（需 ≥ 板 Ø%.0f，余量 %.1f）%s'
            % (FACE_D, BOARD_D, (FACE_D - BOARD_D) / 2, '✅' if FACE_D > BOARD_D + 0.6 else '❌ 板装不进')),
        ('眼睛(设计)', '宽 %.1f × 高 %.1f mm，中心距 %.1f mm' % (ew, eh, eg)),
        ('眼睛(像素)', '宽 %d px × 高 %d px，中心距 %d px，圆角 %d px'
            % (round(ew / MM_PER_PX), round(eh / MM_PER_PX), round(eg / MM_PER_PX), round(ew / MM_PER_PX / 2))),
        ('视野占用', '眼高占球径 %.1f%%（参考视频 %.1f%%）' % (eh / SPHERE_OD * 100, REF_EYE_H * 100)),
        ('底座', 'Ø%.1f × %.1f，球体落座圆心' % (BASE_OD, BASE_H)),
    ]
    for k, v in rows:
        print('  %-11s %s' % (k, v))
    # 屏是否放得下
    need = ew / MM_PER_PX + eg / MM_PER_PX
    print('  %-11s %d px ＜ %d px 上限 → %s' % ('像素校验', round(need), SCREEN_PX,
                                              '✅ 放得下' if need < SCREEN_PX else '❌ 眼距过大'))
    print('-' * 78)
    print('  SCAD 参数：')
    print('    SPHERE_OD=%.1f; SHELL_T=%.1f; DOME_OD=%.1f; DOME_T=%.1f;' % (SPHERE_OD, SHELL_T, DOME_OD, DOME_T))
    print('    WINDOW_D=%.1f; SCREEN_Z=%.2f; BASE_OD=%.1f; BASE_H=%.1f;' % (WINDOW_D, SCREEN_Z, BASE_OD, BASE_H))
    print('=' * 78)


def compare():
    """三档球径对比：眼高占球径不变时，屏够不够用"""
    print('\n不同球径下的可行性（1.75" / 466px 屏，眼距按参考比例）')
    print('  %-8s %-10s %-12s %-12s %s' % ('球径', '眼高', '眼距', '屏直径', '结论'))
    for d in (90, 110, 120):
        ew, eh, eg = d * REF_EYE_W, d * REF_EYE_H, d * REF_EYE_GAP
        span = eg + ew
        ok = '✅ 余量 %.0f mm' % (SCREEN_D - span) if span < SCREEN_D * 0.95 else '⚠️ 眼距撑满屏'
        print('  Ø%-7.0f %-10.1f %-12.1f %-12.1f %s' % (d, eh, eg, SCREEN_D, ok))


if __name__ == '__main__':
    import sys
    # 用法: python params.py [球径] [屏距] [壁厚]   例: python params.py 100 11 2.5
    if len(sys.argv) > 3:
        SHELL_T = float(sys.argv[3])
    if len(sys.argv) > 1:
        SPHERE_OD = float(sys.argv[1]); BASE_OD = SPHERE_OD
        SPHERE_ID = SPHERE_OD - 2 * SHELL_T
        DOME_OD = SPHERE_ID - 2 * GAP
        DOME_ID = DOME_OD - 2 * DOME_T
        INNER_R = DOME_ID / 2.0
    if len(sys.argv) > 2:
        SCREEN_SETBACK = float(sys.argv[2])
    SCREEN_Z = SPHERE_ID / 2.0 - SCREEN_SETBACK
    FACE_D = 2 * math.sqrt(max(0.0, (DOME_OD / 2.0) ** 2 - SCREEN_Z ** 2))
    report()
    compare()
