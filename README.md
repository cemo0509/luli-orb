# 琉璃 ORB（LULI-ORB）

> 一个「透明球里悬浮着一双眼睛」的桌面 AI 伴侣。
> 只做壳体 + 电子 + 固件，不做商业化量产模具；目标是自己能装出来、拿在手上不廉价。

![剖面](docs/assets/orb-section.svg)

---

## 一句话方案

**Ø70 实心玻璃半球（凸面朝前、平面朝后）+ Ø68 黑色哑光遮光盖（贴平面）+ 1.75" 圆 AMOLED（Ø44.4）装在遮光盖中心的 Ø50 窗后 + 机身（电池/喇叭/灯环）。**

眼睛之所以「浮」在球心，靠的不是投影也不是全息，而是三件事：

1. **屏放在球心所在的平面上**——球心那一点发出的光，打到内外球面时**入射角都是 0°**，不折射 → 不放大、不位移、不畸变；
2. **球是实心的**——光从平面进、从球面出，走的是整块玻璃，才有"晶体"的厚度感；
3. **AMOLED 纯黑 + 哑光遮光盖**——屏不亮的地方是真黑，屏的圆形边界和遮光盖完全融合，看不见屏幕在哪。

这条链路不需要开孔、不需要合缝、不需要任何特殊光学件。

---

## 目录

| 文件 | 内容 |
|---|---|
| [MEMORY.md](MEMORY.md) | ★ **项目长期记忆**：铁律、参数、踩过的坑。新会话先读这个 |
| [docs/01_product.md](docs/01_product.md) | 产品定义、参考产品逐帧拆解、归一化测量、差异定位 |
| [docs/02_optics.md](docs/02_optics.md) | 显示与光学：为什么必须 AMOLED、屏边怎么藏、视差、遮光 |
| [docs/03_mechanical.md](docs/03_mechanical.md) | 结构分件、尺寸链、公差、打印参数 |
| [docs/04_electronics.md](docs/04_electronics.md) | 主控/供电/音频/灯环/接线表 |
| [docs/05_software.md](docs/05_software.md) | 小智固件、眼睛引擎、情绪状态机、MCP 工具、配网 OTA |
| [docs/06_bom.md](docs/06_bom.md) | BOM、成本、采购注意 |
| [docs/07_assembly.md](docs/07_assembly.md) | 装配工艺、粘接、消光、检验清单 |
| [docs/08_roadmap.md](docs/08_roadmap.md) | 四阶段路线图、风险表、待决策项 |
| [docs/09_purchase.md](docs/09_purchase.md) | ★ **买什么**：球/板/配件的下单清单、价位与卖家红线 |
| [docs/10_shell_material.md](docs/10_shell_material.md) | 球壳材料：玻璃 vs 亚克力 vs PC、UV 粘接 |
| [docs/11_solid_ball.md](docs/11_solid_ball.md) | ★ **实心/空心/整球**的全部论证（为什么是半球） |
| [docs/12_face_ui.md](docs/12_face_ui.md) | 面部 UI · 探索：五种设计语言 |
| [docs/13_face_spec.md](docs/13_face_spec.md) | ★ **面部定稿「一滴光」**：token、七状态、行为引擎、验收 |
| [hardware/hemisphere.py](hardware/hemisphere.py) | ★ 球径 → 屏占比 / 遮光板 / 眼睛像素 / 重量 |
| [hardware/back_cover.scad](hardware/back_cover.scad) | ★ 遮光后盖参数化模型（改 `BALL_D` 一个数） |
| [hardware/gen_face_assets.py](hardware/gen_face_assets.py) | 生成面部固件资源（bloom / hot / glint） |
| [hardware/params.py](hardware/params.py) | 早期空心球方案的参数计算器（存档） |
| [hardware/ball_lens.py](hardware/ball_lens.py) | 整球透镜核算（对照组，方案已否） |
| [firmware/assets/](firmware/assets) | 面部资源：bloom.png / hot.png / glint.png（合计 7.3 KB） |
| [tools/face-iris.html](tools/face-iris.html) | ★ **面部预览**：实尺寸 + 球内预览 + 行为引擎开关 + 3× 像素验收 |
| [tools/ball-view.html](tools/ball-view.html) | 整球透镜视角模拟（对照用） |
| [tools/face-lab.html](tools/face-lab.html) | 面部五概念实验台（存档） |
| [tools/eye-preview.html](tools/eye-preview.html) | 早期眼睛 UI 预览（存档） |
| [logs/](logs) | 每日工作记录 |

---

## 关键尺寸

| 项 | 值 |
|---|---|
| 球壳 | **Ø70 实心半球**，高 35（平面过球心），亚克力 106.6g |
| 屏 | 1.75" AMOLED，Ø44.4 有效区，466×466，**1px = 0.0954mm** |
| 屏占比 | 63.5%，四周黑边 12.8mm |
| 黑遮光盖 | **Ø68 × 2**，中心开 **Ø50** 窗，四角 M2 盲孔 |
| 主板 | Ø51.2 × 12.1（屏板一体，屏在其前表面） |
| 眼睛 | **59 × 147 px**（=5.6×14.0mm，20% 球径），中心距 190px（25.9%），y=236 |
| 机身 | 约 Ø66 × 26，含 1000mAh + 喇叭 + 灯环 |
| 整机 | 约 Ø70 × 75，**≈ 330g** |

> 参数改动请跑 `python hardware/hemisphere.py <球径>`，别手算。

---

## 现在到哪一步

- [x] 参考产品逐帧拆解、比例归一化
- [x] 光学路线收敛到「实心半球 + 屏在球心平面」
- [x] 全尺寸链推导，参数化脚本 + SCAD 可跑
- [x] 面部 UI 定稿（v2，含行为引擎）
- [x] 固件资源三张 PNG
- [x] **球已买**：Ø70 实心半球 ¥28（烟林塑胶）
- [ ] 球到货验收：称重 106.6g → 灯管测试 → 手机贴平面看眼睛
- [ ] 定主板：1.43C-EN（Ø46/Ø36.75屏）或 1.75-B（Ø51/Ø44.4屏）
- [ ] 打遮光后盖 + 机身（`back_cover.scad`，`BALL_D=70`）
- [ ] 电子联调（小智固件点亮）
- [ ] LVGL 面部组件 + 真机验收

---

## 常见误解（先说清楚，少走弯路）

| 误解 | 事实 |
|---|---|
| 球应该是整球 | ❌ 整球是球透镜，放大 3.5×、可见区只剩 Ø28、要"弹性顶球"机构。**必须半球** |
| 球越大越好 | ❌ Ø70 已够（屏占 63.5%）；Ø100 贵 3 倍、重 3 倍，观感提升有限 |
| 一定要实心，空心不行 | ⚠️ 光学上等效，但空心罩口不规整、封板漏光、面型有波纹 —— 省 ¥30 换三个变量 |
| 屏贴球外表面也行 | ❌ 贴外表面 = 3.5 倍放大 + 严重球差，眼睛会糊成一片 |
| 眼睛做好看就够了 | ❌ 静止的眼睛 10 秒内会被判定为"一张图"。必须有**扫视 + 非对称 + 眨眼变体** |

---

## 许可

文档 CC BY-NC-SA 4.0；硬件脚本 MIT。
参考产品「程野与路遥」为他人作品，本项目仅做结构原理学习与自用复刻，不用于销售。
