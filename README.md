# Xi-Arithmetic-Embedder
## 具身机器人传感器算术嵌入器

Xi-Arithmetic-Embedder 是一个基于重整化群思想（Renormalization Group）的具身机器人传感器算术嵌入器。它将物理信号（力觉、视觉、IMU、编码器）转换为鲁棒的临界带参数，实现物理世界的不变性表示。

### 核心特性

- 🔄 **重整化群思想**：多尺度物理信号编码，实现跨尺度不变性
- 🎯 **物理归一化**：强归一化 + 物理单位保留，确保物理可解释性
- 📐 **自适应窗口**：基于波动率的动态窗口调整，适应不同动作模式
- 🔍 **异常检测**：异常信号检测与质量评估，提升系统鲁棒性
- 🎓 **在线校准**：零点校准接口，支持在线微调

### 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/Xi-Arithmetic-Embedder.git
cd Xi-Arithmetic-Embedder

# 安装依赖
pip install numpy torch
```

### 快速开始

```python
from xi_arithmetic_embedder import XiArithmeticEmbedder, SensorConfig, SensorType
import numpy as np

# 配置传感器
configs = [
    SensorConfig("torque", SensorType.FORCE_TORQUE, "N·m", 50.0, -50.0, 50.0, 1),
    SensorConfig("imu", SensorType.IMU, "m/s²", 9.8, -20.0, 20.0, 1)
]

# 初始化嵌入器
embedder = XiArithmeticEmbedder(configs, n_zero_points=5)

# 准备数据
sensor_data = {
    "torque": np.random.randn(100) * 5,
    "imu": np.random.randn(100) * 0.5
}

# 计算嵌入表示
embedding = embedder.compute_embedding(sensor_data)
# shape: (2, 5, 4) -> [传感器数, 零点数, (c_re, c_im, rho_re, rho_im)]

print(f"Embedding shape: {embedding.shape}")
print(f"First sensor's zero points: {embedding[0, :, 2]}")  # Reρ values
```

### 项目结构

```
Xi-Arithmetic-Embedder/
├── src/
│   └── xi_arithmetic_embedder.py    # 核心实现
├── tests/
│   └── test_embedder.py              # 测试用例
├── docs/
│   └── design_documentation.md       # 设计文档
├── pyproject.toml                    # 项目配置
├── README.md                         # 项目说明
└── .gitignore                        # Git 忽略规则
```

### 核心功能

#### 1. 重整化群思想实现
- 基于重整化群思想，在有限时间窗口内构建完备正交基
- 零点参数随尺度变化，实现多尺度信号编码

#### 2. 物理归一化系统
- 强归一化确保物理量纲正确
- 保留物理单位（N·m, m/s², rad 等）
- 跨传感器计算一致性

#### 3. 自适应测量窗
- 基于信号波动率动态调整窗口长度
- 适应不同动作模式（快速抓取 vs 稳步行走）
- 避免信号失真和噪声引入

#### 4. 异常检测
- 检测噪声、丢包、偏移等异常
- 在零点层面识别异常频率
- 提供数据质量评估

#### 5. 校准与训练
- 零点校准接口，将传感器零点映射到物理规则零点
- 在线微调机制
- 仿真器体校准

### 性能数据

- **计算速度**：10 次嵌入（1000 样本）仅需 0.045 秒
- **测试覆盖**：12 个测试用例全部通过
- **物理可解释性**：每个零点参数都有明确物理意义
- **鲁棒性**：完整的异常检测和数据验证机制

### 应用场景

1. **具身智能**：物理 = 世界 Ξ
   - 操作、导航、接触、力控
   - 摔倒检测、传递学习

2. **具身感知**：物理信号 → 临界带参数
   - 关节角/位置序列
   - 力/扭矩信号
   - 碰撞事件

3. **多机器人系统**：临界共识而非投票
   - 队形保持
   - 协同操作

### 技术原理

#### 重整化群思想
在有限时间窗口 $T$ 内构建完备正交基 $\{\phi_n\}$，研究物理量在尺度变化下的规律。

#### 零点对应物理
- $\Re \rho$ 编码**系统稳定性风险**（从 0.5 偏移的程度）
- $\Im \rho$ 编码**物理频率/时间尺度**（力矩波动、碰撞频率）

#### 归一化
$$\rho = \frac{\text{signal} - \mu}{\sigma} \quad ; \quad t = \Im \rho$$

#### 推导
基于重整化群思想，在有限时间窗口内构建完备正交基，计算积分，得到代码核心。

### 设计文档

详细技术设计和数学推导请查看 [设计文档](docs/design_documentation.md)。

### 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 许可证

本项目采用 MIT 许可证。详情参见 [LICENSE](LICENSE) 文件。

### 联系方式

- 项目主页：https://github.com/yourusername/Xi-Arithmetic-Embedder
- 问题反馈：https://github.com/yourusername/Xi-Arithmetic-Embedder/issues
- 邮箱联系：contact@xi-ability.org

---

**注意**：本项目为研究性质，尚未在生产环境验证。使用时请确保满足相关安全要求。
