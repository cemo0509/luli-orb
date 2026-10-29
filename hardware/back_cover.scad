// ============================================================
// 琉璃 ORB · 后盖（黑遮光盖）参数化模型  v2
// ------------------------------------------------------------
// 作用：压在半球平面背后，提供整块"黑面"，并把屏幕压在正中。
//
// 层次（从前到后）：
//   玻璃平面 ─ 0.5mm 黑EVA圈 ─ 本件前盘(2mm, 中心 Ø50 窗)
//            ─ 屏幕/主板 Ø51.2×12.1 ─ 容腔 ─ 后壳盖板
//
// 装配要点：
//   1) 前盘用 0.5mm 黑 EVA 或 UV 胶粘在玻璃平面上（不要打孔，亚克力易裂）
//   2) 主板从后面放进容腔，靠后壳的泡棉往前顶
//   3) 螺丝只连"本件 ↔ 后壳"，**不穿到正面**，避免漏光
//
// 用法：改参数 → F5 预览 → F6 渲染 → 导出 STL
//       前盘朝下贴床打印（最平的那一面贴玻璃）
// ============================================================

/* [球壳] */
BALL_D   = 70;     // ★ 半球外径：改这一个数，全件跟着变
PLATE_T  = 2.0;    // 前盘厚（贴着玻璃的那层）

/* [屏幕] */
WIN_D    = 50;     // 中心窗口（屏 Ø44.4，压边 2.8）
BOARD_D  = 51.2;   // 微雪 1.75-B 板径 + 0.2
BOARD_T  = 12.1;   // 板厚
CAV_GAP  = 0.6;    // 容腔单边间隙
FOAM     = 1.5;    // 板后面的泡棉预留

/* [结构] */
WALL     = 2.4;    // 侧壁 / 后盖板厚
SCREW_M  = 2.0;    // M2
SCREW_N  = 4;
BARREL_D = 5.0;    // 螺丝柱外径
BARREL_H = 4.0;    // 柱子向后凸出高度
BODY_WALL = 4.5;   // 杯体壁厚（前盘后面收细，省料）
HOLE_D   = 1.8;    // M2 自攻底孔
HOLE_DEP = 6.0;    // 底孔深度（盲孔，不通到正面）

/* [渲染] */
$fn = 96;

// ------------------------------------------------------------
CAV_D   = BOARD_D + 2 * CAV_GAP;              // 容腔内径
CAV_H   = BOARD_T + FOAM;                     // 容腔净深
PLATE_D = BALL_D - 2;                         // 前盘外径，比球径小 2（露出一圈玻璃边）
BODY_D  = CAV_D + 2 * BODY_WALL;              // 杯体外径（前盘之后）
RING_R  = (BODY_D + CAV_D) / 4;               // 螺丝分布圆半径
TOTAL_H = PLATE_T + CAV_H + WALL;

module cover() {
    difference() {
        union() {
            // 前盘（贴玻璃）
            cylinder(d = PLATE_D, h = PLATE_T);
            // 杯体（比前盘细，省料）
            translate([0, 0, PLATE_T])
                cylinder(d = BODY_D, h = CAV_H);
            // 后盖板
            translate([0, 0, PLATE_T + CAV_H])
                cylinder(d = BODY_D, h = WALL);

            // 螺丝柱（向后凸出，接后壳）
            for (i = [0 : SCREW_N - 1])
                rotate([0, 0, i * 360 / SCREW_N + 45])
                    translate([RING_R, 0, TOTAL_H - 0.1])
                        cylinder(d = BARREL_D, h = BARREL_H + 0.1);
        }

        // ① 中心窗口（直壁 Ø50，穿透前盘）
        translate([0, 0, -0.1])
            cylinder(d = WIN_D, h = PLATE_T + 0.2);

        // ①b 正面喇叭口（Ø50 → Ø53，形成陷光台阶，只切 1mm 深）
        translate([0, 0, -0.1])
            cylinder(h = 1.0, d1 = WIN_D + 3, d2 = WIN_D + 0.02);

        // ② 屏幕容腔（从前盘背面往里挖 CAV_H，保留后盖板）
        translate([0, 0, PLATE_T])
            cylinder(d = CAV_D, h = CAV_H);

        // ③ 螺丝盲孔（从后往前的盲孔，绝不穿透前盘）
        for (i = [0 : SCREW_N - 1])
            rotate([0, 0, i * 360 / SCREW_N + 45])
                translate([RING_R, 0, TOTAL_H + BARREL_H - HOLE_DEP])
                    cylinder(d = HOLE_D, h = HOLE_DEP + 0.2);

        // ④ 走线缺口（后盖板边缘）
        translate([0, BODY_D / 2, PLATE_T + CAV_H])
            cube([14, 8, WALL + 0.6], center = true);
    }
}

cover();
