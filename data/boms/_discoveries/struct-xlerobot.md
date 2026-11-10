# struct-xlerobot 拆解发现

XLeRobot 0.4（Apache-2.0）。官方 BOM 是一张 markdown 表，**四套币种价格 + 明确的可替代件说明**，是目前这批整机里最容易做成采购清单的一台。

## ① BOM 用到、站内 taxonomy 没有的行业品类

- **全向轮组（4" omni wheel）**：3 个轮子做成三轮全向底盘，BOM 品类表里没有 `wheel`，只能落到 `misc`。站内其实有 `wheel` 品类（`wheeltec-omni-127` / `wheeltec-mecanum-100` 等），属于"BOM 品类表缺一格"而不是"部件库缺货"。
  <https://github.com/Vector-Wangel/XLeRobot/blob/main/docs/en/source/hardware/getting_started/material.md>
- **户外电源 / 移动电源站（288Wh，双 USB-C 60W+）**：站内 `power` 全是航模电池与 BMS，没有"220V 输出 + PD 快充"这一类。
  <https://www.ankersolix.com/products/c300-dc?variant=49702163972426>
- **总线舵机驱动板（USB → TTL 半双工总线）**：站内 `motor_driver` 只有 DAMIAO 的 DM40/DM60/DM80/DM100-1E，缺舵机总线这一支。
  <https://www.amazon.com/Waveshare-Integrates-Control-Circuit-Supports/dp/B0CTMM4LWK/>
- **家居类车体（IKEA RÅSKOG 推车）／桌夹／USB Hub**：不是机器人件，但确实是整机 BOM 行，站内没有任何对应格。
- **5264 3P 舵机线**：站内有 `feetech-5264-cable`（伟利达 WLD 5264 3P 端子线），但 BOM 行是 4ft(约 1.2 m) 整根成品线，规格对不上，只能做近似替代。

## ② 高价值但部件库缺失的件

| 件 | 规格 | 证据 |
| --- | --- | --- |
| **Feetech STS3215 12V 30kg·cm** | 17 个，$14/个，占整机件数 1/3、成本 1/4 | BOM 第 1 行 <https://shop.wowrobo.com/products/feetech-sts3215-servo-12v-30kg-high-torque-servo-for-so-arm100> |
| STS3250-C002（12V 50kg·cm 升级件） | 官方给的 1.5 倍扭矩选项，"3 倍价" | 同页正文说明 |
| Waveshare 总线舵机驱动板 | 2 块，$10.55 | <https://www.amazon.com/Waveshare-Integrates-Control-Circuit-Supports/dp/B0CTMM4LWK/> |
| **Intel RealSense D415** | 可选 RGBD 头，$272；站内只有 D405/D435i/D455/D457 | <https://store.intelrealsense.com/buy-intel-realsense-depth-camera-d415.html> |
| Anker SOLIX C300 | 288Wh/300W，$179.99，单件最贵 | <https://www.ankersolix.com/products/c300-dc?variant=49702163972426> |
| IKEA RÅSKOG | $39.99，车体就是它 | <https://www.ikea.com/us/en/p/raskog-utility-cart-black-40582181/> |
| 4" 全向轮 | 3 个，$9.99；站内全向轮是 127/150 mm 且轮毂形式不同 | <https://www.vexrobotics.com/omni-wheels.html> |

> 站内 `servo` 品类只有 `feetech-sts3215-7v4`（7.4V 19 kg·cm），与 12V 30kg 是**两个 SKU**，不能直接挂。

## ③ 可联动的设备工具

- **3D 打印**：SO-101 臂件 + 底盘连接件 + 软爪（TPU95A）→ `bambulab-a1-mini`、`bambulab-p1s`、`snapmaker-u1`。
  <https://github.com/Vector-Wangel/XLeRobot/tree/main/hardware>
- **焊接/压线**：5264 端子需自行压接、舵机线要加长 → `hakko-fx888d`、`fnirsi-hs-02`。
- **万用表 + 直流电源**：舵机总线 12V 供电与压降排查（整机要 2 路 60W+）→ `uni-t-ut61e`、`alientek-dp100`。
- **示波器（可选）**：总线通信排故 → `fnirsi-1013d`。
- 官方明说"不含工具成本"，所以工具类条目在 BOM 里是**参考项**（M3 螺丝套装 / 斜口钳 / 螺丝刀套装合计 $27.98），联动时不能算进整机成本。

## ④ 可联动的采购库渠道

- **Wowrobo（深圳）**：官方推荐的 SO-101 打印件/整机套件卖家，也是 Feetech 舵机的 US 渠道，站内采购库没有该条。
  <https://shop.wowrobo.com/products/so-arm101-diy-kit-assembled-version-1>
- **Robu.in（印度）**、**AliExpress（欧洲）**、**淘宝/拼多多（中国）**：官方对同一行给了四地渠道，正好可以给站内"渠道对比"补非中国样本。
- **IKEA / Anker / Adafruit / VEX**：消费零售渠道，属于采购库里完全没有的类型（现有 234 家以华强北/淘宝元件商与机加工为主）。

## ⑤ 适合 RoboWiki 定位的其他发现

- **$660 是目前站内最便宜的"能跑 VLA 的双臂移动"**：17 舵机 + 推车 + 户外电源，比 OpenArm 的 $6,500 低一个数量级，适合做"入门 vs 进阶"对照。
- **官方自带四币种同表**：US/EU/CN/IN 四列价格 + "TODO" 空缺，是检验"保留原币种、不换算"纪律的最佳样本（本站目前只落了 US 列）。
- **明示可替代件**：电池只要"两路 60W+ USB-C"、车可用同类推车、舵机可升 STS3250——比一般 BOM 更适合做"替代件推荐"功能。
- **坐标系锚点明确**：工作空间 0.5–1.25 m 高、离车沿 0.36 m，整机 12 kg，可与 SO-101 单臂形成同一参数族对比。
- **硬件与仿真同仓**：URDF + MuJoCo/ManiSkill + LeRobot 训练脚本都在，BOM 页面可以直接链到"买完怎么训"。
  <https://xlerobot.readthedocs.io/en/latest/>
