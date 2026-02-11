---
标题: Capability-Aware Shared Hypernetworks for Flexible Heterogeneous Multi-Robot Coordination
作者: Kevin Fu, Shalin Anand Jain, Pierce Howell, Harish Ravichandar
发布日期: 2025-01-10
arXiv ID: 2501.06058v5
PDF: https://arxiv.org/pdf/2501.06058v5.pdf
---

# 对比摘要

**摘要对比分析**  

1. **方法对比**  
   源论文CLiMRS提出基于大语言模型（LLM）的自适应群体协商框架，通过动态子群划分和多LLM讨论实现异构机器人协作，核心是**人类启发的协商机制**。候选论文CASH则采用**超网络架构**，通过软参数共享动态生成机器人策略，强调**能力感知的权重适应**。两者均关注异构协作，但技术路线迥异：CLiMRS依赖LLM的推理能力，CASH基于神经网络参数优化。CASH的方法对CLiMRS的启发在于动态策略生成可结合LLM的规划能力，但未直接改进后者。  

2. **实验差异**  
   CLiMRS在定制基准CLiMBench上测试装配任务，对比传统规划方法，效率提升40%；CASH则在多任务（灭火、采矿等）和多种学习范式（模仿学习、RL）下验证，使用JaxMARL和Robotarium平台，参数减少60%-80%且支持零样本泛化。实验场景不同：CLiMRS侧重长期规划，CASH强调动态适应能力。CASH的基线更全面（含独立策略与共享策略），但两者均未直接比较对方方法。  

3. **结论异同**  
   两文均认为**异构协作需动态适应能力**，但结论侧重点不同：CLiMRS证明LLM协商可提升复杂任务效率，CASH则表明超网络能平衡多样性与效率。二者互补性强——CLiMRS的群体协商机制可整合CASH的能力感知架构，而CASH的零样本泛化为CLiMRS的未训练机器人问题提供解决思路。矛盾之处在于CLiMRS依赖预训练LLM，而CASH完全基于数据驱动，后者可能更适合资源受限场景。  

综上，两文从不同技术路径推进异构机器人协作，CASH在参数效率和泛化性上更优，而CLiMRS展示了LLM在高层规划中的潜力，未来工作可探索二者结合。