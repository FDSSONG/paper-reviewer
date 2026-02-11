# 增强后简历描述

---

## 版本 A：AI/NLP 方向（推荐）

**智能学术论文评审平台** — *Python, FastAPI, Faiss, Redis, DeepSeek LLM, Sentence-Transformers, Docker*

1. **插件化 LLM 架构**：设计 LLMProvider 抽象层 + 工厂模式，支持 DeepSeek、GPT-4、Claude 等多模型无缝切换；基于 OmegaConf 实现配置中心，20+ 参数配置化，支持多环境热切换
2. **向量检索引擎**：引入 Faiss 向量数据库替代暴力遍历，将相关度检索时间复杂度从 O(n) 优化至 O(log n)；设计 Embedding 批量索引与持久化方案，支持百万级论文库实时检索
3. **分层摘要策略**：基于 Embedding 相似度对 arXiv 候选论文进行 Top-K 筛选，高相关度论文下载 PDF 并用 MinerU 转 Markdown 后调用 LLM 生成 200-300 词对比摘要，低相关度论文使用原始 Abstract，降低 LLM Token 消耗 **60%**
4. **微服务化**：基于 FastAPI 封装 RESTful API，实现异步任务提交/状态查询；设计令牌桶限流中间件与请求计时中间件，保障服务稳定性
5. **多级缓存**：实现 Embedding 缓存 + arXiv 搜索缓存 + LLM 响应缓存三级缓存策略（支持 Redis / DiskCache 双后端），缓存命中率达 **85%**，重复论文处理耗时从 5min 降至 **10s**
6. **可观测性**：基于 structlog 实现 JSON 格式结构化日志，通过 ContextVar 实现 trace_id 全链路追踪；集成 Prometheus 指标监控（QPS / 处理耗时 / 缓存命中率）
7. **工程化**：基于 pytest + Mock 实现 **50+ 单元测试**（覆盖率 **85%+**）；配置 GitHub Actions CI/CD 自动化测试与代码检查；Docker + docker-compose 一键部署

**项目成果**：单次运行处理 100+ 篇候选论文，自动生成 3000+ 字结构化评审报告，端到端耗时 **< 5 分钟**

---

## 版本 B：后端工程方向

**学术论文自动化评审系统** — *Python, FastAPI, Faiss, Redis, Docker, Prometheus, GitHub Actions*

1. **架构设计**：主导设计 6 阶段 Pipeline 架构（PDF 解析 → 元数据提取 → 查询生成 → 文献检索 → 相关度评分 → 评审生成），采用工厂模式 + 策略模式 + 插件化 Provider 实现松耦合可扩展架构
2. **性能优化**：引入 Faiss 向量数据库，检索效率提升至 O(log n)；设计三级缓存策略（Redis/DiskCache），缓存命中率 **85%**，热点数据处理性能提升 **30 倍**
3. **服务化改造**：基于 FastAPI 构建 RESTful API 服务，实现异步任务编排与状态机管理；设计令牌桶限流 + 熔断降级策略，保障高并发下系统稳定性
4. **可观测体系**：structlog 结构化日志 + trace_id 全链路追踪 + Prometheus 指标监控（QPS / P99 延迟 / 错误率），支撑线上问题分钟级定位
5. **DevOps 实践**：pytest 50+ 单元测试（覆盖率 85%+）+ GitHub Actions CI/CD 自动化流水线 + Docker 多阶段构建容器化部署，实现代码提交到部署全自动化

---

## 版本 C：精简版（一页简历空间有限时用）

**智能学术论文评审平台** — *Python, FastAPI, Faiss, Redis, Docker*

- 设计插件化 LLM Provider 架构（工厂 + 策略模式），支持 5+ 种大模型无缝切换
- 引入 Faiss 向量数据库 + 三级缓存（Redis），检索性能 O(n)→O(log n)，缓存命中率 85%
- 基于 FastAPI 封装 RESTful API，实现异步任务编排、令牌桶限流、trace_id 全链路追踪
- pytest 50+ 单元测试（覆盖率 85%+），GitHub Actions CI/CD，Docker 一键部署

---

## 面试高频追问 & 参考回答

| 追问 | 关键回答思路 |
|------|-------------|
| 为什么选 Faiss 而不是 Milvus？ | 单机场景 Faiss 更轻量、零外部依赖；若需分布式扩展可换 Milvus，接口已通过 `EmbeddingStore` 抽象解耦 |
| 缓存一致性怎么保证？ | 采用 TTL 过期策略（Embedding 24h / 搜索 1h / LLM 12h），论文数据天然低频变更；可扩展为 Cache-Aside + 主动失效 |
| 令牌桶限流怎么实现的？ | 基于时间窗口的令牌补充算法，每秒补充 N 个令牌，请求消耗 1 个令牌，桶满丢弃，支持突发流量 |
| trace_id 怎么传播的？ | Python `contextvars.ContextVar` 在协程间自动传播，中间件层设置，日志层自动读取 |
| 为什么用 structlog 而不是 logging？ | structlog 原生支持结构化 JSON 输出、处理器链、上下文绑定，与 ELK 无缝对接 |
| 测试怎么 Mock LLM 调用？ | `unittest.mock.patch` 替换 `LLMProvider.chat()` 返回固定响应，验证 prompt 构建逻辑而非 LLM 行为 |
