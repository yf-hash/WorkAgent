---
name: resume-screener
description: >
  简历智能筛选技能。解析多格式简历，基于 JD 进行硬性过滤与六维度评分，
  输出候选人排名、淘汰原因和面试建议，支持匿名化与多种报告格式。
  触发关键词：简历筛选、resume screening、JD匹配、候选人排名、面试建议
user-invocable: false
effort: high
argument-hint: "--jd <file> [--weights balanced|tech|management|campus|custom] [--top <n>] <resume...>"
---

# 简历智能筛选技能

## 流程

1. JD 解析：岗位、职责、技能要求、学历经验
2. 简历结构化提取：教育/经历/技能/项目/成就
3. 硬性过滤：学历、年限、必备技能、黑名单
4. 六维度评分：
   - 技能匹配度
   - 工作经验
   - 教育背景
   - 项目相关度
   - 成就影响力
   - 综合素质
5. 排名与报告输出

## 权重预设

- balanced：30/25/15/15/10/5
- tech：强化技能和经验
- management：强化经验和成就
- campus：强化教育和项目
- custom：自定义权重

## 输出类型

- full
- table
- brief
- interview

## 报告核心内容

- 候选人排名表
- 每位候选人的亮点与不足
- 淘汰名单与原因
- A/S 级候选人的面试问题建议
