# struct-open-duck-mini 拆解发现

Open Duck Mini V2（Apache-2.0）。官方 BOM 是一张 Google Sheet，单工作表四段（Power / Servos, control and sensors / MISC / Expression package），计价币种 EUR。 <https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit>

- **同表两列价差极大**：除 unit price 外另有 Estimated lowest price（IMU 40→1、PLA 20→0、XT30 8→0.5），本文件只录 unit price，不把估价当标价。 <https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit>
- **两个官方合计**：398.10 €（基础机）/ 432.34 €（含 Expression package 表情包），官宣"<$400"只对应前者，对比时必须说清口径。 <https://github.com/apirrone/Open_Duck_Mini/tree/v2>
- 唯一精确挂上目录的件：Feetech STS3215 7.4V → `feetech-sts3215-7v4`，14 个 196 € 占 45% 成本。 <https://www.alibaba.com/product-detail/Robot-Servo-STS3215-7-4V-19kg_1600052037414.html>
- **站内缺 Pi Zero 2W**：controller_high 只有 RPi 4 / RPi 5，Zero 系空白，而一批小双足（含 Microduck）都靠 Zero 2W 板载跑策略。
- **BNO055 只有裸片**（`jlc-c93216`，立创 C93216，55.61 元），BOM 要的是带融合的成品模块 40 €，两者不能混算。
- **总线舵机驱动板缺格**：Waveshare Bus Servo Adapter (A)，站内 actuator_driver 只有达妙 DM 系列驱动器。 <https://www.waveshare.com/bus-servo-adapter-a.htm>
- **足底微动开关 SS-10 缺格**：站内仅 `omron-limit-switch`（通用限位开关），无 SS-10 具体型号；9g 头/天线舵机同样空缺（towerpro 只有 MG995）。
- **2S 供电套件缺格**：18650 电芯 + 2S 电池座 + 2S BMS + UBEC 5V，站内 power 只有航模电池与 3–6S BMS。 <https://www.nkon.nl/fr/molicel-inr18650-p30b-3000mah-30a.html>
- **BOM 行名本身有歧义**："XT15? XT30 ?" 连接器与 "5V regulator"（HENGE UBEC 4–12A），不能直接挂 `amass-xt30` / `generic-ubec-5v3a`。
- **耗材记账随意**：PLA 20 € 无链接、TPU 记 0 €（"negligeable cost"）、M3 热熔嵌件只写买一包，复现成本需自行重算。
- **机械源不在仓库**：只有导出的 STL 与 Onshape 文档，无可版本化的 STEP/URDF 源，标"全开源"宜注明 CAD 在 Onshape。 <https://cad.onshape.com/documents/64074dfcfa379b37d8a47762/w/3650ab4221e215a4f65eb7fe/e/0505c262d882183a25049d05>
- **无自制 PCB**：舵机总线板与稳压全是成品模块，买齐即装，是"零 PCB 门槛"的好样本。 <https://github.com/apirrone/Open_Duck_Mini_Runtime>
- **采购渠道是欧洲零售**：Amazon.fr / AliExpress / Alibaba / nkon.nl / Waveshare，与站内 234 家华强北向渠道几乎零交集。 <https://www.amazon.fr/dp/B0CXXSVFTV>
- **可联动设备**：3D 打印（PLA/TPU 件）→ `bambulab-a1-mini`；焊线端子 → `fnirsi-hs-02`；上电排故 → `uni-t-ut61e`、`alientek-dp100`。
- **舵机 16 个 vs dof 14**：BOM 14 个 STS3215 + 2 个 9g，URDF 另有 2 个被动天线关节，方案页 dof=14 与 BOM 数量不矛盾但极易读错。 <https://github.com/apirrone/Open_Duck_Mini/tree/v2/mini_bdx/robots/open_duck_mini_v2>
