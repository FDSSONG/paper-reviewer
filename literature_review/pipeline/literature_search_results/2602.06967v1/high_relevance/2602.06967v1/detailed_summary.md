---
标题: Leveraging Adaptive Group Negotiation for Heterogeneous Multi-Robot Collaboration with Large Language Models
作者: Siqi Song, Xuanbing Xie, Zonglin Li, Yuqiang Li, Shijie Wang
发布日期: 2025-12-29
arXiv ID: 2602.06967v1
PDF: https://arxiv.org/pdf/2602.06967v1.pdf
---

# 对比摘要

Multi-robot collaboration tasks often require heterogeneous robots to work together over long horizons under spatial constraints and environmental uncertainties. Although Large Language Models (LLMs) excel at reasoning and planning, their potential for coordinated control has not been fully explored. Inspired by human teamwork, we present CLiMRS (Cooperative Large-Language-Model-Driven Heterogeneous Multi-Robot System), an adaptive group negotiation framework among LLMs for multi-robot collaboration. This framework pairs each robot with an LLM agent and dynamically forms subgroups through a general proposal planner. Within each subgroup, a subgroup manager leads perception-driven multi-LLM discussions to get commands for actions. Feedback is provided by both robot execution outcomes and environment changes. This grouping-planning-execution-feedback loop enables efficient planning and robust execution. To evaluate these capabilities, we introduce CLiMBench, a heterogeneous multi-robot benchmark of challenging assembly tasks. Our experiments show that CLiMRS surpasses the best baseline, achieving over 40% higher efficiency on complex tasks without sacrificing success on simpler ones. Overall, our results demonstrate that leveraging human-inspired group formation and negotiation principles significantly enhances the efficiency of heterogeneous multi-robot collaboration. Our code is available here: https://github.com/song-siqi/CLiMRS.