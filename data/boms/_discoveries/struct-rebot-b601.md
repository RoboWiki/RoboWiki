# struct-rebot-b601 拆解发现

Seeed reBot B601 DM（达妙 43 系电机）。官方 BOM 是 readme 里 7 张 Markdown 表，本次拆出 83 行；价格为逐件 Reference Price，另有两行整批均价。
<https://github.com/Seeed-Projects/reBot-DevArm/blob/main/hardware/reBot_B601_DM/readme.md>

- 结构件全部自加工：21 种 CNC/钣金铝件（5052）只给整批均价 250 USD，逐件全缺；站内 `structural` 没有"按 STEP 外协机加"条目。
- 3D 打印件 19 种同样只有整批 50 USD 均价，材料按 Bambu ABS/PLA 分色；站内无打印耗材/打印服务条目可对。
- 外购件 25 行里 9 行螺丝只有 `14+`/`30+` 最小包量且无单价，2 行定位销写 `Several` 无数量，只能进 unresolved。
- 唯一 CNY 行是 M3x2.5 六角螺母（2 个，2.10 CNY），与整表 USD 冲突，按不换算纪律未计入合计。
- 站内精确对上 3 行：DM4310(V4)→`达妙-dm-dm-j4310-2ec-v1-1`、DM4340P(V4)→`达妙-dm-dm-j4340p-2ec`、CAN 驱动板→`damiao-usb2can`；后两者 Seeed 版次/命名与目录有偏差，已在 notes 标注。
- 目录缺口：DM4310/DM4340P 的 V4 版次、6707ZZ/6803ZZ/AXK5578 轴承、MGN9-170 导轨与 MGN9 滑块、模数 1 16T 齿轮、XT30/XT60 成品线、LRS-350-24 电源。
- 相机只给兼容支架（打印件），Orbbec Gemini2 本体与价格未进主 BOM；整机套件价只在 Seeed 商店页 <https://www.seeedstudio.com/reBot-Arm-B601-DM-Bundle.html>
- RS 版（RobStride 电机）BOM 在兄弟目录 <https://github.com/Seeed-Projects/reBot-DevArm/tree/main/hardware/reBot_B601_RS>，本次只拆 DM 版。
