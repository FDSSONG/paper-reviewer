---
标题: PIP-LLM: Integrating PDDL-Integer Programming with LLMs for Coordinating Multi-Robot Teams Using Natural Language
作者: Guangyao Shi, Yuwei Wu, Vijay Kumar, Gaurav S. Sukhatme
发布日期: 2025-10-26
arXiv ID: 2510.22784v1
PDF: https://arxiv.org/pdf/2510.22784v1.pdf
---

# 对比摘要

**摘要对比分析**  
两篇论文均聚焦大语言模型（LLM）驱动的多机器人协作，但方法、实验与结论存在显著差异。  

1. **方法对比**  
源论文CLiMRS提出**自适应群体协商框架**，通过动态子组划分与多LLM交互实现协作，强调人类团队启发的实时反馈机制；候选论文PIP-LLM则采用**分层规划**，结合PDDL团队级规划与整数编程（IP）的机器人级分配，侧重结构化任务分解与优化。前者依赖LLM的自主协商能力，后者通过经典规划与优化算法弥补LLM的不足，技术路线差异显著。PIP-LLM对任务依赖的显式建模可视为对CLiMRS动态分组的补充，但未直接借鉴其协商机制。  

2. **实验差异**  
源论文使用**CLiMBench**测试异构机器人装配任务，以任务效率为核心指标，结果显示CLiMRS在复杂任务中效率提升40%；候选论文则构建**多场景基准**，评估任务成功率、旅行成本与负载均衡，PIP-LLM在成本优化与可扩展性上优于基线。两者场景不同：CLiMRS针对环境不确定性，PIP-LLM侧重大规模任务分配，实验设计反映各自方法优势。  

3. **结论异同**  
两文均验证了LLM在多机器人系统中的潜力，但结论侧重点不同：CLiMRS证明群体协商提升鲁棒性，PIP-LLM强调分层规划优化效率与可扩展性。二者互补性强——CLiMRS的动态适应可弥补PIP-LLM对实时反馈的不足，而PIP-LLM的优化框架可为CLiMRS提供任务分解的理论支撑。候选论文对经典规划的深度整合为源论文的纯LLM路径提供了替代思路。