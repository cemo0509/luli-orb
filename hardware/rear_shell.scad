// ============================================================
// 琉璃 ORB · 后半球（一体机身）  v3
// ------------------------------------------------------------
// 玻璃半球（前）+ 打印后半球（后）= 一整颗 Ø70 球
// 后半球一次解决四件事：
//   ① 球的后半外观（黑色哑光）
//   ② 遮光面（赤道平面 + Ø39 窗）
//   ③ 装板 / 电池 / 喇叭的容腔
//   ④ 出声孔 + Type-C 出线孔
//
// 【构造】实心半球 − 内腔（从 z=T 往上挖）
//   这样赤道板的厚度正好是 T，且与球壳是同一个实体，不会分成两块
//
// 【打印】赤道平面朝下贴床，穹顶朝上。内部顶端需要树状支撑。
// 【装配】打完翻转 180°，玻璃半球 UV 胶 / VHB 直接粘在平面上
//        接触面是整个 Ø70 平面（38.5 cm²），不用止口、不打孔
// ============================================================

/* [球壳] */
OD        = 70;
T         = 2.5;    // 壁厚 & 赤道板厚

/* [屏幕] */
WIN_D     = 39;     // 窗口（1.43 屏 Ø36.75，压边 1.1）
WIN_CHAM  = 1.2;    // 窗口内侧陷光倒角

/* [电子] */
BOARD_D   = 46.2;   // 主板定位环内径
RING_H    = 1.2;    // 定位环高
SPK_CHAM  = 30;     // 喇叭腔 Ø30
SPK_PORT  = 20;     // 出声孔 Ø20
SPK_DEEP  = 9;      // 喇叭腔深度
USB_W     = 11;
USB_H     = 4.5;

$fn = 140;

R  = OD / 2;
RI = R - T;

module rear_half() {
    difference() {
        // ① 实心半球（z ≥ 0）
        intersection() {
            sphere(r = R);
            cylinder(h = R, r = R + 1);
        }

        // ② 内腔：球 RI 只保留 z ≥ T 的部分 → 赤道板厚正好 T
        intersection() {
            sphere(r = RI);
            translate([0, 0, T]) cylinder(h = R, r = R + 1);
        }

        // ③ 中心窗口（穿透赤道板）
        translate([0, 0, -0.1]) cylinder(d = WIN_D, h = T + 0.2);

        // ④ 窗口内侧陷光倒角
        translate([0, 0, T - 0.9])
            cylinder(h = 1.0, d1 = WIN_D, d2 = WIN_D + 2*WIN_CHAM);

        // ⑤ 喇叭腔 + 出声锥（都从球顶往里）
        translate([0, 0, R - T - SPK_DEEP])
            cylinder(h = SPK_DEEP, d1 = SPK_CHAM, d2 = SPK_PORT);
        translate([0, 0, R - T - 0.3])
            cylinder(d = SPK_PORT, h = T + 0.6);

        // ⑥ Type-C 出线孔（+Y 侧，赤道板上方 5mm）
        translate([0, R - 3, T + 5])
            rotate([90, 0, 0])
                cube([USB_W, USB_H, 10], center = true);
    }

    // ⑦ 主板定位环（加料，不是挖料）
    difference() {
            cylinder(h = RING_H, d = BOARD_D + 1.6);
        translate([0, 0, T - 0.1])
            cylinder(h = RING_H + 0.2, d = BOARD_D);
    }
}

rear_half();
