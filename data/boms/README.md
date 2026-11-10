# 全开源整机 BOM 清单

一台整机一个 JSON：`<robot-id>.json`，`robot-id` 与 `data/robots/` 里的 id 一致。
只拆官方 BOM；官方未发布 BOM 的整机不建文件，在 `docs/BOM-ANALYSIS.md` 里标 `missing`。

BOM 行使用**行业惯例品类**，不强行套用站内部件品类。站内品类映射留给 `catalog_part_id`：

| category | 含义 |
| --- | --- |
| `actuator` | 舵机 / 关节电机 / 电缸 |
| `actuator_driver` | 伺服驱动器 / 电机驱动板 |
| `controller` | 主控 / 下位机 / MCU 板 |
| `compute` | 上位机 / Jetson / 树莓派 / 工控机 |
| `sensor` | IMU / 编码器 / 力传感器 / 温度等 |
| `perception` | 相机 / 深度相机 / 激光雷达 |
| `power` | 电池 / BMS / DC-DC / 电源 |
| `wiring` | 线材 / 线束 / 连接器 / 端子 |
| `pcb` | 裸 PCB / PCBA / 定制电路板 |
| `structural` | CNC 件 / 钣金件 / 型材 / 结构五金 |
| `printed_part` | 3D 打印件 |
| `fastener` | 螺丝 / 螺母 / 热熔嵌件 / 卡扣 |
| `transmission` | 轴承 / 同步带 / 齿轮 / 联轴器 / 丝杆 |
| `thermal` | 散热片 / 风扇 / 导热材料 |
| `interface` | 遥控器 / 急停 / 开关 / 显示屏 / 按键 |
| `cable_management` | 拖链 / 扎带 / 编织网管 / 理线 |
| `consumable` | 胶水 / 焊料 / 润滑脂 / 打印耗材 |
| `tooling` | 专用工装 / 夹具 / 校准件 / 治具 |
| `service` | 外协加工 / 组装 / 打样服务 |
| `misc` | 无法归类但 BOM 确实列出的条目 |

## 文件结构

```json
{
  "robot_id": "struct-so-arm100",
  "robot_name": "SO-100",
  "source": {
    "url": "https://github.com/TheRobotStudio/SO-ARM100#parts-for-two-arms-follower-and-leader-setup",
    "type": "github_markdown",
    "official": true,
    "fetched_at": "2026-11-10",
    "notes": "官方 README 的 parts 表；价格为官方列出的参考价"
  },
  "currency": "USD",
  "price_basis": "官方 BOM 标价，未含运费/税",
  "lines": [
    {
      "id": "line-001",
      "category": "actuator",
      "category_label": "执行器",
      "name": "STS3215 7.4V 30kg·cm",
      "spec": "C001/C018 舵机",
      "qty": 6,
      "unit": "pcs",
      "unit_price": 14.9,
      "currency": "USD",
      "subtotal": 89.4,
      "vendor": "Waveshare",
      "product_url": "https://...",
      "source_ref": "Parts for two arms, row 3",
      "catalog_part_id": null,
      "supplier_id": null,
      "equipment_id": null,
      "notes": null
    }
  ],
  "totals": {
    "line_count": 1,
    "item_count": 6,
    "priced_subtotal": 89.4,
    "unpriced_lines": 0,
    "by_category": {"actuator": 89.4}
  },
  "unresolved": [
    {"item": "M3 螺丝包", "reason": "BOM 未给数量"}
  ],
  "completeness": {
    "bom_published": true,
    "mechanical_files": true,
    "pcb_files": false,
    "firmware": true,
    "notes": "机械 STEP 与固件在仓库；无自制 PCB"
  }
}
```

## 纪律

- 价格只录原表确有数值；缺失写 `null`，在 `unresolved` 说明原因，不估算。
- 不同币种不换算，保留 `currency` 原值。
- `catalog_part_id` / `supplier_id` / `equipment_id` 只在**精确匹配**时填写，否则 `null`。
- 官方 BOM 的套装/两臂套餐按原表行拆，不擅自归一化数量。
- 每次写完跑 `python tools/validate_boms.py`。
