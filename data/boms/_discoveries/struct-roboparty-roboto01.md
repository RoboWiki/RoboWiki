# struct-roboparty-roboto01 拆解发现

ROBOTO 01 / RP1.3.4（RoboParty）官方 04_BOM 同时发七自由度与五自由度两份 xlsx；本次拆 7DOF『总BOM』444 行、295 个唯一料号、1898 件，全表无单价。

- **两份配置不通用**：5DOF 与 7DOF 的臂部分别成套，本站只拆 7DOF，换配置要整份重拆。<https://github.com/Roboparty/RP1_hardware/tree/main/04_BOM>
- **紧固件占 74% 数量**：119 行 / 1404 颗，左右臂腿各重复一遍，item_count 1898 里结构件只有 141 件，成本讨论不能按行数看。<https://github.com/Roboparty/RP1_hardware/blob/main/04_BOM/RP1.3.4%20%EF%BC%88%E4%B8%83%E8%87%AA%E7%94%B1%E5%BA%A6%2B%E8%BF%90%E6%8E%A7%E5%A4%B4%EF%BC%89BOM%E8%A1%A8.xlsx>
- **12 行电机模组 28 台**：RMM6562-2E ×12、RMM10062-2E ×8、RMM8463-2E ×4、RZW5552-2C ×4，全是整机厂自研关节模组，站内 actuator 一条都挂不上。<https://github.com/Roboparty/RP1_hardware/tree/main/04_BOM>
- **BOM 里没有感知件**：整机页写 Intel D435i + 3D 激光雷达，BOM 中 perception 为 0 行，相机与雷达只能算选配。<https://roboparty.com/products/RP1>
- **BOM 里没有 Jetson Orin**：主控是 RBE-MAIN-RK3588S + Orange Pi CM5，只留了 3D 打印『达妙orin支架』，站内整机参数 Orin NX 16GB 的口径要改。<https://github.com/Roboparty/RP1_hardware/tree/main/02_PCB>
- **雷赛灵巧手只列转接件**：YCL.M000331 转接件 + 手转接板，手本体不在表内，末端成本无法从 BOM 得出。<https://github.com/Roboparty/RP1_hardware/tree/main/01_Mechanic>
- **50 行 3D 打印件（52 件）+ 131 行 CNC 件（141 件）**：打印件含 UFS9002 树脂头壳（需光固化），CNC 以 AL6061-T6 / 45# / P20 为主走外协，机器上只能做小件。<https://github.com/Roboparty/RP1_hardware/tree/main/01_Mechanic>
- **17 块自制 PCBA**：主控、IMU、电容板、风扇电源板、灯板、HOTSWAP、433TX、140W 充电板全为 RBE-* 自研，02_PCB 提供板级 BOM。<https://github.com/Roboparty/RP1_hardware/tree/main/02_PCB>
- **61 行线束命名规整**：RP1-ARM01~08 / LEG01~07 / BODY01~06 / POWER01~02 + BACK-*，可与 03_Harness 图纸一一对应，适合做线束级索引。<https://github.com/Roboparty/RP1_hardware/tree/main/03_Harness>
- **无 vendor、无价**：原表只有料号/名称/数量/材料，YCL 前缀是整机厂内部编码，反查不到供应商，supplier_id 与 unit_price 全空。<https://github.com/Roboparty/RP1_hardware/tree/main/04_BOM>
- **模板残留表**：『标准件』『电子元器件』『线材』『电机』四张工作表是 ATOM 02 项目模板，只有表头无数据；『包材』只重复航空箱一行，均未采用。<https://github.com/Roboparty/RP1_hardware/blob/main/04_BOM/README.md>
- **料号即索引**：官方 README 要求"通过料号查找配套资料"，机械件/线束/板卡共用 YCL 编码，站内若建 BOM 页面应按料号做跳转。<https://github.com/Roboparty/RP1_hardware/blob/main/04_BOM/README.md>
- **固件与描述分离**：固件在 RP1_firmware，URDF 在 RP1_description，BOM 仓库本身不含代码，整机复现需 4 个仓库联动。<https://github.com/Roboparty/RP1_firmware>
- **吊装件随箱发**：吊环 M6×12 与吊绳各 2 件、RP1 航空箱 1 只计入 BOM，调试/运输成本被算进整机物料，别当成结构件。<https://github.com/Roboparty/RP1_hardware/tree/main/04_BOM>
- **五自由度版少的是整条腕部**：5DOF 表 406 行，砍掉 RZW5552-2C 腕部模组 4 台、腕部结构、手转接板与 ARM07/08 线材，换成 7 个新型号腕部件，差价主要落在模组上。<https://github.com/Roboparty/RP1_hardware/blob/main/04_BOM/RP1.3.4%20%EF%BC%88%E4%BA%94%E8%87%AA%E7%94%B1%E5%BA%A6%2B%E8%BF%90%E6%8E%A7%E5%A4%B4%EF%BC%89BOM%E8%A1%A8.xlsx>
