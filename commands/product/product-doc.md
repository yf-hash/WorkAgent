---
name: product-doc
description: B2B产品资料体系生成器，覆盖24类标准产品文档，支持白皮书、彩页、解决方案、测试文档、操作手册、培训材料、版本说明等全套输出
user-invocable: true
argument-hint: "<产品名称> [--type whitepaper|brochure|solution|case|manual|training|release|bid-params|tech-intro|biz-intro] [--industry fintech|gov|healthcare|edu|mfg|retail|saas] [--lang zh|en]"
---

# /product-doc — B2B产品资料体系生成器

加载技能：`skills/product-doc-writer/SKILL.md`

## 触发条件
需要生成 B2B 产品的标准化文档资料，包括：产品介绍、白皮书、彩页、解决方案、操作手册、培训材料、测试文档、版本说明、招投标参数等24类文档时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--type` | 文档类型（见下表） | `biz-intro` |
| `--industry` | 目标行业 | — |
| `--lang` | 输出语言 | `zh` |

### 文档类型速查（24类）

| `--type` | 文档名称 | 推荐格式 | 密级 | 重要性 |
|----------|---------|---------|------|--------|
| `biz-intro` | 产品介绍-商务版 | PPT大纲 | 可公开 | ★★★ |
| `whitepaper` | 产品白皮书 | Word | 可公开 | ★★★ |
| `brochure` | 产品彩页 | Word/PDF | 可公开 | ★★ |
| `sales-guide` | 产品销售指南（一页禅） | Word | 可公开 | ★★★ |
| `model-list` | 产品型号及功能清单 | Excel | 可公开 | ★★★ |
| `case` | 成功案例 | Word | 可公开 | ★★★ |
| `faq` | 销售常见问题 | Word | 可公开 | ★★★ |
| `competitive` | 竞品分析（A/B/C/D优势项） | PPT大纲 | **内部保密** | ★★★ |
| `bid-params` | 产品招投标参数 | Excel | **内部保密** | ★★★ |
| `bid-proof` | 产品招投标证明材料 | Word | 可公开 | ★★★ |
| `qualification` | 产品资质证书目录 | Word | 可公开 | ★★ |
| `solution` | 产品解决方案 | Word | 可公开 | ★★★ |
| `tech-intro` | 产品介绍-技术版 | PPT大纲 | 可公开 | ★★★ |
| `tech-whitepaper` | 技术白皮书 | Word | **内部保密** | ★★★ |
| `demo` | 产品Demo说明文档 | Word | 可公开 | ★★ |
| `test-doc` | 产品测试文档 | Word | 可公开 | ★★★ |
| `compat` | 兼容性支持文档 | Word | 可公开 | ★★ |
| `contact` | 产品联系人 | Word | 可公开 | ★★ |
| `user-manual` | 产品操作手册 | Word | 可公开 | ★★★ |
| `deploy-manual` | 产品部署及配置手册 | Word | 可公开 | ★★★ |
| `training-ppt` | 产品介绍-培训版 | PPT大纲 | 可公开 | ★★★ |
| `training-quiz` | 产品培训试题 | Word | 可公开 | ★★ |
| `release-notes` | 产品新版本发布说明 | PPT大纲 | 可公开 | ★★★ |
| `checklist` | 产品文档自查清单 | — | 内部 | ★★★ |

## 行业变体

| `--industry` | 典型客户 | 核心痛点 | 参考监管/标准 |
|--------------|---------|---------|-------------|
| `fintech` | 银行/保险/证券 | 数据安全、合规审计、风控 | 等保2.0/行业监管系列 |
| `gov` | 政府/事业单位 | 数据安全合规、网络安全法 | 数安法/网安法/关基条例 |
| `healthcare` | 医院/卫生机构 | 患者数据保护、系统安全 | 医疗信息安全相关规范 |
| `edu` | 高校/教育机构 | 学生数据保护、科研安全 | 教育信息化相关规范 |
| `mfg` | 制造业/能源 | 工控安全、OT网络防护 | 工业互联网安全规范 |
| `retail` | 零售/电商 | 用户数据、交易安全 | 个人信息保护法/PCI-DSS |
| `saas` | SaaS/互联网企业 | 多租户隔离、API安全 | ISO 27001/SOC 2 |

## 文档命名规范

```
格式：[产品名]【版本号】[文档类别名]_版本号.扩展名
示例：智能运维平台【v3.1】产品白皮书_v3.1.docx
      数据安全网关【v1.0】产品销售指南_v1.0.docx

命名规则：
- 版本号格式：v主版本.次版本（如 v1.0、v2.1）
- 禁止使用日期作为主版本标识
- 更新时同步修改文档内的变更页
```

## 使用示例

```
/product-doc 数据安全网关 --type whitepaper
/product-doc 智能运维平台 --type solution --industry fintech
/product-doc 零信任访问控制系统 --type bid-params --industry gov
/product-doc API安全防护平台 --type training-ppt
/product-doc 终端检测响应系统 --type competitive
/product-doc 云原生安全平台 --type release-notes
/product-doc 身份认证系统 --type checklist
```

## 执行流程

```
Step 1: 产品信息收集
  → 确认产品全称、版本、核心功能定位
  → 识别目标客户类型（To G / To B / SaaS / 行业化）
  → 确认文档密级（可公开 / 内部 / 保密）

Step 2: 结构生成
  → 按模板框架生成对应文档结构
  → 植入产品核心卖点和差异化优势
  → 确保关键章节符合企业规范要求

Step 3: 内容填充
  → 填充产品技术参数、功能描述
  → 生成行业场景化案例和数据
  → 添加法律声明、版权信息（按企业标准）

Step 4: 质量核验
  → 对照产品文档自查清单14项逐一核查
  → 检查公司名称/产品名称是否为最新
  → 验证版本号、修订记录完整性
  → 输出待确认事项清单
```

## 参考规范

| 规范 | 说明 |
|------|------|
| B2B产品资料体系（24类） | 文档格式、密级、必选/可选标准 |
| 产品文档自查清单（14项） | 格式/内容/上传三类质量检查项 |
| 企业文档命名规范 | 文件命名和版本管理标准 |
| 兼容性文档规范 | 平台/环境兼容性测试记录标准 |
