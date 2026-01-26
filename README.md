# Visual Studio Code 开源项目演化分析

## 📋 项目概览

本项目针对[Visual Studio Code - Open Source ("Code - OSS")](https://github.com/microsoft/vscode)开源软件，对其历史提交信息、贡献者、社区活跃度等多维度数据进行深入分析统计，并通过可视化展示项目演化规律。

### 项目背景
- **研究对象**：Microsoft Visual Studio Code (Code-OSS)
- **研究方向**：开源项目演化分析 - 数据分析与可视化
- **研究跨度**：2015年至今（约10年的完整历史）
- **分析维度**：贡献者、提交历史、社区活跃度、代码质量、项目成熟度

### 项目成果物
- 完整的数据采集（12个维度的CSV数据）
- 深度的数据分析和可视化（12+个分析图表）
- 系统的项目演化规律总结

---

## 📁 项目结构

```
.
├── README.md                          # 项目说明文档
├── requirements.txt                   # Python依赖库清单
│
├── 📊 原始数据文件 (爬虫产出)
│   ├── 1_contributors.csv             # 贡献者信息 (301行)
│   ├── 2_commits.csv                  # 提交记录 (920行)
│   ├── 3_issues_open.csv              # Issue数据 (604行)
│   ├── 4_prs_open.csv                 # PR数据 (398行)
│   ├── 5_stargazers.csv               # Star历史 (301行)
│   ├── 6_forks.csv                    # Fork历史 (101行)
│   ├── 7_releases.csv                 # 版本发布 (54行)
│   ├── 8_branches.csv                 # 分支信息 (31行)
│   ├── 9_repository_stats.csv         # 仓库统计 (2行)
│   ├── commits_massive.csv            # 大规模提交数据 (4900行)
│   ├── contributors_massive.csv       # 大规模贡献者 (329行)
│   └── vscode_commit_history.csv      # 完整提交历史 (91689行) ⭐
│
├── 📝 分析代码
│   ├── run.py                         # 本地Git仓库分析脚本
│   ├── cyxcode.py                     # 数据爬虫脚本
│   └── code-oss-history.ipynb         # 📊 可视化分析Notebook (你的工作)
│
└── 📄 文档
    ├── 创新点.txt                     # 项目创新点说明
    └── 数据类型和数据结构.txt         # 数据字典
```

---

## 🛠️ 环境配置指南

### 1️⃣ Python版本要求
```
Python 3.10
```

### 2️⃣ 使用Anaconda配置（推荐）

```bash
# 1. 创建环境
conda env create -f environment.yml

# 2. 激活环境
conda activate vscode-analysis

# 3. 启动Jupyter
jupyter notebook
# 或
jupyter lab
```

### 3️⃣ 依赖库清单

| 库名称 | 版本 | 用途 |
|-------|------|------|
| pandas | 2.1.4 | 数据加载、清洗、转换 |
| numpy | 1.24.3 | 数值计算 |
| matplotlib | 3.8.2 | 静态数据可视化 |
| seaborn | 0.13.0 | 统计图表美化 |
| plotly | 5.18.0 | 交互式图表 |
| scipy | 1.11.4 | 统计分析 |
| scikit-learn | 1.3.2 | 机器学习、趋势分析 |
| statsmodels | 0.14.0 | 时间序列分析 |
| jupyter | 1.0.0 | Notebook环境 |
| jupyterlab | 4.0.9 | JupyterLab界面 |
| ipywidgets | 8.1.1 | Jupyter交互组件 |

### 4️⃣ 验证安装

在Jupyter Notebook中运行：
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

print("✅ 所有库导入成功！")
```

---

## 📊 工作流程

### **第一阶段：数据准备**
- 配置Python虚拟环境 ← **你在这里**
- 加载和检查所有CSV数据
- 数据清洗和格式统一
- 生成数据概览报告

### **第二阶段：指标计算**
- 计算贡献者指标（排名、分布、增长）
- 计算提交指标（频率、类型、趋势）
- 计算社区指标（Issue、PR、Stars、Forks）
- 计算演化指标（版本、分支、质量）

### **第三阶段：可视化分析**
- 必做图表（6个基础图表）
- 进阶图表（6个高级图表）
- 高级分析（3个专题分析）

### **第四阶段：报告撰写**
- 整理Jupyter Notebook
- 撰写分析结论
- 补充项目见解

---

## 🚀 快速开始

```bash
# 1. 创建Anaconda环境
conda env create -f environment.yml

# 2. 激活环境
conda activate vscode-analysis

# 3. 启动Jupyter
jupyter notebook

# 4. 打开 code-oss-history.ipynb
# 开始分析工作
```

---

## 📈 分析成果预览

### 核心分析指标
- ✅ 贡献者规模与分布
- ✅ 代码活跃度趋势（月度、周度）
- ✅ 项目质量演化（Bug修复率）
- ✅ 社区健康度评估
- ✅ 团队规模增长
- ✅ 版本发布周期

### 可视化图表（12+个）
1. Top 20贡献者排行榜
2. 月度提交趋势
3. 贡献者分布特征
4. 提交类型分布
5. Issue/PR活跃度
6. Stars增长曲线
7. 核心贡献者识别（帕累托）
8. 提交热力图
9. 代码质量演化
10. 团队规模增长
11. 版本发布周期
12. 交互式仪表盘（可选）

---

## 👥 小组成员与分工

| 角色 | 负责任务 |
|-----|--------|
| 爬虫团队 | 数据采集与爬取（已完成✅） |
| **你** | **可视化分析与报告撰写** 📊 |

---

## 📝 注意事项

### 数据说明
- `vscode_commit_history.csv` 是最全的提交历史（91689行，建议作为主要分析数据源）
- 其他CSV文件是不同维度的补充数据
- 所有时间均为UTC时间，分析时可按需转换

### 常见问题
**Q: 如何加速数据加载？**  
A: 可以对大文件进行分块读取，或预先筛选需要的列

**Q: 时间数据格式如何处理？**  
A: 使用`pd.to_datetime()`统一转换为datetime类型

**Q: 如何处理缺失值？**  
A: 根据具体分析需求决定是否填充或删除

---

## 📚 参考资源

### Pandas数据处理
- [Pandas官方文档](https://pandas.pydata.org/docs/)
- [数据透视表和分组](https://pandas.pydata.org/docs/user_guide/groupby.html)

### 数据可视化
- [Matplotlib教程](https://matplotlib.org/stable/tutorials/index.html)
- [Seaborn配置库](https://seaborn.pydata.org/)
- [Plotly交互图表](https://plotly.com/python/)

### 统计分析
- [Scipy统计函数](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Statsmodels时间序列](https://www.statsmodels.org/stable/tsa.html)

---

## ✅ 检查清单

配置完成后，在Jupyter中验证：

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy import stats
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.seasonal import seasonal_decompose

# 验证数据加载
commits = pd.read_csv('vscode_commit_history.csv')
print(f"✅ 提交记录: {len(commits)} 行")
```

环境配置完成标志：
- [ ] Conda环境已激活
- [ ] `conda env create -f environment.yml` 成功
- [ ] Jupyter能正常启动
- [ ] 所有库能成功导入
- [ ] CSV数据文件可读取

---

## 📞 其他

如有问题，请参考本项目的其他文档文件：
- `创新点.txt` - 项目技术亮点说明
- `数据类型和数据结构.txt` - 数据字典详解