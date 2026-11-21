# ❍
Xi-Arithmetic-Embedder
Zeros for embodied intelligence

## 简介

Xi-Arithmetic-Embedder 是一个具身机器人传感器算术嵌入器，将物理信号转换为鲁棒的临界带参数。

## 📁 文件结构

```
Xi-Arithmetic-Embedder/
├── src/
│   └── xi_arithmetic_embedder.py
├── tests/
│   ├── test_embedder.py
│   └── test_config.json
├── docs/
│   └── design_documentation.md
├── .gitignore
├── README.md
└── pyproject.toml
```

## 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/yourusername/Xi-Arithmetic-Embedder.git
cd Xi-Arithmetic-Embedder

# 安装依赖
pip install numpy torch

# 运行测试
python -m pytest tests/ -v

# 运行示例
python examples/basic_usage.py
```

## 📊 核心特性

- 多传感器支持 (力、视觉、IMU、编码器)
- 物理归一化与单位保留
- 自适应测量窗调整
- 异常检测与质量评估
- 零点校准与在线微调

## 🔧 配置

```json
{
  "sensor_config": "src/configs/robot_config.json",
  "embedding_params": {
    "n_zero_points": 5,
    "window_size": 64,
    "overlap_rate": 0.5
  }
}
```

## 📝 许可证

MIT License
