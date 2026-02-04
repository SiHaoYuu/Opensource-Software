# Visual Studio Code 开源项目演化分析

>[!WARNING]
>如要执行`cyxcode.py`代码，请在第896行填入自己的GitHub Token.

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
│   └── code-oss-history.ipynb         # 📊 可视化分析Notebook
│
└── 📄 文档
    ├── 创新点.txt                     # 项目创新点说明
    └── 数据类型和数据结构.txt         # 数据字典
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

## 📝 注意事项

### 数据说明
- `vscode_commit_history.csv` 是最全的提交历史（91689行，建议作为主要分析数据源）
- 其他CSV文件是不同维度的补充数据
- 所有时间均为UTC时间，分析时可按需转换

---

## 📞 其他

如有问题，请参考本项目的其他文档文件：
- `创新点.txt` - 项目技术亮点说明
- `数据类型和数据结构.txt` - 数据字典详解
