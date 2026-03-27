# QX-Config-Sync 项目文档

> QuantumultX 配置自动构建与同步工具 V5.1

---

## 目录

- [项目概述](#项目概述)
- [项目结构](#项目结构)
- [技术栈](#技术栈)
- [核心功能](#核心功能)
- [使用指南](#使用指南)
- [配置说明](#配置说明)
- [API 参考](#api-参考)
- [自动化部署](#自动化部署)
- [常见问题](#常见问题)

---

## 项目概述

QX-Config-Sync 是一个用于自动构建 QuantumultX 配置文件的开源工具。它通过 YAML 配置文件管理所有规则和策略，支持底包下载、规则注入、远程引用等功能，并通过 GitHub Actions 实现自动化构建和同步。

### 主要特点

- **模块化配置**：使用 YAML 文件统一管理所有配置
- **增量构建**：基于底包进行增量修改，保留原有配置
- **灵活注入**：支持本地文件引用和远程规则引用
- **策略映射**：支持将外部策略组映射到底包真实策略
- **自动化部署**：集成 GitHub Actions 实现定时自动构建
- **规则清洗**：支持黑名单/白名单模式过滤底包内容

---

## 项目结构

```
qx-config-sync/
├── .github/
│   └── workflows/
│       └── build.yml           # GitHub Actions 自动构建配置
├── profiles/
│   └── config.yaml             # 主配置文件
├── rules/                      # 自定义规则目录
│   ├── my_custom.list          # 自定义分流规则
│   ├── my_mitm_hosts.list      # MITM hostname 配置
│   └── my_rewrites.list        # 重写规则
├── src/
│   ├── main.py                 # 主入口文件
│   └── qx_core.py              # 核心配置管理类
├── requirements.txt            # Python 依赖
├── .gitignore                  # Git 忽略规则
└── MyQuantumultX.conf          # 输出配置文件（自动生成）
```

---

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.9+ | 主要开发语言 |
| requests | - | HTTP 请求库，用于下载底包 |
| PyYAML | - | YAML 配置文件解析 |
| GitHub Actions | - | 自动化构建与部署 |

---

## 核心功能

### 1. 底包下载与解析

从指定 URL 下载 QuantumultX 配置底包，并按标准节点解析到内存中。

```python
manager.load_from_url(config['base']['url'])
```

### 2. 配置清洗 (Patches)

在注入新规则前，先过滤掉底包中不需要的内容。

支持两种模式：
- **黑名单模式 (blacklist)**：移除包含指定关键词的规则
- **白名单模式 (whitelist)**：只保留包含指定关键词的规则

```yaml
patches:
  policy:
    keywords:
      - "Hijacking"
      - "广告"
      - "static"
    strategy: "blacklist"
```

### 3. KV 配置覆盖

支持对 General、MITM、HTTP Backend 等节点的 Key-Value 配置进行覆盖。

```yaml
general:
  geoip-url: "https://github.com/Hackl0us/GeoIP2-CN/raw/release/Country.mmdb"
```

### 4. 规则注入

支持将规则注入到指定节点的头部或尾部。

- **追加模式**：注入到节点末尾（默认）
- **头部注入**：注入到节点开头（用于高优先级规则）

```python
manager.add_list_item("filter_local", rule, position="start")
```

### 5. 本地文件引用

支持通过 `file://` 协议引用本地规则文件。

```yaml
local_filters:
  top:
    - "file://rules/my_custom.list"
```

### 6. 远程规则引用

支持引用 GitHub 上的开源规则库，目前支持：

- **blackmatrix7**：内置源简写，自动拼接 GitHub URL
- **自定义 URL**：直接指定完整的规则 URL

```yaml
filter_remote:
  - name: "TikTok"
    source: "blackmatrix7"
    policy: "us-node"
    tag: "TikTok"
```

### 7. 策略组映射

将外部规则中的策略名称映射到底包的真实策略组名称。

```yaml
policy_map:
  us-node: "美国节点"
  direct: "direct"
  reject: "reject"
```

---

## 使用指南

### 本地运行

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 修改配置文件

编辑 `profiles/config.yaml`，根据需要调整各项配置。

3. 运行构建

```bash
python src/main.py
```

4. 查看输出

生成的配置文件保存在项目根目录下的 `MyQuantumultX.conf`。

### 在 QuantumultX 中使用

1. 将生成的 `MyQuantumultX.conf` 上传到支持外链的云存储
2. 在 QuantumultX 中添加下载配置
3. 输入配置文件的 URL 即可下载使用

---

## 配置说明

### config.yaml 完整配置说明

#### 1. 基础设置 (Base)

```yaml
base:
  url: "https://ddgksf2013.top/Profile/QuantumultX.conf"
```

指定底包配置的下载 URL，所有修改都将基于此文件进行。

#### 2. 补丁排除 (Patches)

```yaml
patches:
  policy:
    keywords:
      - "Hijacking"
      - "广告"
      - "static"
    strategy: "blacklist"
```

| 参数 | 类型 | 说明 |
|------|------|------|
| section | string | 要清洗的节点名称 |
| keywords | list | 关键词列表 |
| strategy | string | 策略：blacklist（黑名单）或 whitelist（白名单） |

#### 3. 全局设置 (General)

```yaml
general:
  geoip-url: "https://github.com/Hackl0us/GeoIP2-CN/raw/release/Country.mmdb"
  resource_parser_url: "https://raw.githubusercontent.com/KOP-XIAO/QuantumultX/master/Scripts/resource-parser.js"
  server_check_url: "http://www.gstatic.com/generate_204"
```

#### 4. DNS 配置

```yaml
dns:
  - "server=/suversal.com/192.168.1.1"
```

#### 5. 策略组映射 (Policy Map)

```yaml
policy_map:
  us-node: "美国节点"
  direct: "direct"
  reject: "reject"
```

将外部规则中的策略名称映射到底包的真实策略组名称。

#### 6. 策略组定义 (Policy)

```yaml
policy:
  - "static=苹果服务, direct, 香港节点, 台湾节点, 美国节点, 日本节点, 狮城节点, proxy, 手动选择, img-url=https://raw.githubusercontent.com/Koolson/Qure/master/IconSet/Color/Apple.png"
```

支持以下策略类型：

| 类型 | 说明 |
|------|------|
| static | 静态策略组，固定节点顺序 |
| url-latency-benchmark | URL 测速策略组，自动选择最快节点 |
| server-tag-regex | 正则匹配服务器标签 |

#### 7. 远程服务器 (Server Remote)

```yaml
server_remote:
  - "https://我的机场.com, tag=机场, enabled=true"
```

#### 8. 本地分流规则 (Local Filters)

```yaml
local_filters:
  top:
    - "file://rules/my_custom.list"
    - "ip6-cidr,::/0,direct"
  bottom:
    - "geoip,cn,direct"
```

- **top**：注入到分流规则最前面（优先级最高）
- **bottom**：注入到分流规则最后面（优先级最低）

#### 9. 远程分流规则 (Filter Remote)

```yaml
filter_remote:
  - name: "TikTok"
    source: "blackmatrix7"
    policy: "us-node"
    tag: "TikTok"
```

| 参数 | 类型 | 说明 |
|------|------|------|
| name | string | 规则名称（仅用于 blackmatrix7 源） |
| source | string | 源类型：blackmatrix7 或自定义 URL |
| policy | string | 使用的策略组名称 |
| tag | string | 规则标签 |
| url | string | 完整规则 URL（自定义源时使用） |

#### 10. 重写规则 (Rewrite)

```yaml
rewrite_local:
  - "file://rules/my_rewrites.list"
  - "^https://google.cn url 302 https://google.com"

rewrite_remote:
  - "https://limbopro.com/Adblock4limbo.conf, tag=毒奶特供(去网页广告计划), enabled=true"
```

#### 11. MITM 配置

```yaml
mitm:
  hostname: "file://rules/my_mitm_hosts.list"
```

MITM hostname 必须是一行，用逗号分隔：

```
*.google.com, *.googleapis.com, *.apple.com, *.icloud.com, *.instagram.com
```

---

## API 参考

### QXConfigManager 类

核心配置管理类，提供所有配置操作接口。

#### 方法列表

| 方法 | 说明 |
|------|------|
| `load_from_url(url)` | 从 URL 下载并解析底包 |
| `load_rules_from_file(path)` | 从本地文件加载规则 |
| `patch_section(section, keywords, strategy)` | 清洗指定节点内容 |
| `set_kv(section, key, value)` | 设置 KV 配置 |
| `add_list_item(section, item, position)` | 添加列表项到指定位置 |
| `add_remote_rule(url, tag, policy)` | 添加远程规则引用 |
| `save(filename)` | 保存配置到文件 |

#### load_from_url(url)

从指定 URL 下载底包配置。

```python
manager.load_from_url("https://example.com/config.conf")
```

#### patch_section(section, keywords, strategy)

清洗指定节点的规则。

```python
# 黑名单模式：移除包含关键词的规则
manager.patch_section("policy", ["广告", "Hijacking"], "blacklist")

# 白名单模式：只保留包含关键词的规则
manager.patch_section("dns", ["google"], "whitelist")
```

#### set_kv(section, key, value)

设置 KV 配置，支持覆盖和追加模式。

```python
# 覆盖模式
manager.set_kv("general", "geoip-url", "https://example.com/GeoIP.mmdb")

# 追加模式（hostname 特殊处理）
manager.set_kv("mitm", "hostname", "*.example.com")
```

#### add_list_item(section, item, position)

向列表节点添加规则。

```python
# 追加到末尾
manager.add_list_item("filter_local", "host-suffix,google.com,direct")

# 插入到开头
manager.add_list_item("filter_local", "ip6-cidr,::/0,direct", position="start")
```

---

## 自动化部署

### GitHub Actions 配置

项目已配置 GitHub Actions 实现自动化构建和部署。

#### 触发机制

| 触发方式 | 说明 |
|---------|------|
| 定时执行 | 每天北京时间 06:00 自动运行 |
| 手动触发 | 在 GitHub 网页上点击 "Run workflow" 按钮 |
| 代码推送 | 当 profiles/、rules/、src/ 目录文件变更时触发 |

#### 构建流程

1. 拉取最新代码
2. 设置 Python 3.9 环境
3. 安装项目依赖
4. 运行构建脚本
5. 提交生成的配置文件到仓库

#### 配置文件位置

`.github/workflows/build.yml`

---

## 常见问题

### Q1: 如何添加自己的自定义规则？

**A:** 在 `rules/` 目录下创建新的 `.list` 文件，然后在 `config.yaml` 中引用：

```yaml
local_filters:
  top:
    - "file://rules/your_custom.list"
```

### Q2: 如何引用其他开源规则库？

**A:** 使用 `filter_remote` 配置：

```yaml
filter_remote:
  - source: "blackmatrix7"
    name: "Netflix"
    policy: "us-node"
    tag: "Netflix"
```

或者使用自定义 URL：

```yaml
filter_remote:
  - url: "https://raw.githubusercontent.com/xxx/rules/main/list.list"
    policy: "us-node"
    tag: "Custom"
```

### Q3: 如何修改策略组的节点顺序？

**A:** 在 `config.yaml` 的 `policy` 部分修改策略组定义：

```yaml
policy:
  - "static=全球加速, 自动选择, direct, 香港节点, 台湾节点..."
```

### Q4: MITM hostname 如何配置？

**A:** 在 `rules/my_mitm_hosts.list` 中配置（注意必须是一行，逗号分隔）：

```
*.google.com, *.googleapis.com, *.apple.com
```

然后在 `config.yaml` 中引用：

```yaml
mitm:
  hostname: "file://rules/my_mitm_hosts.list"
```

### Q5: 如何删除底包中的某些配置？

**A:** 使用 `patches` 配置进行清洗：

```yaml
patches:
  policy:
    keywords:
      - "要删除的策略组名称"
    strategy: "blacklist"
```

### Q6: 为什么某些规则没有生效？

**A:** 检查以下几点：

1. 规则文件路径是否正确
2. 策略组名称是否在 `policy_map` 中正确映射
3. 规则优先级是否正确（top/bottom）
4. 底包清洗是否误删除了相关配置

---

## 版本历史

### V5.1 (Fixed)

- 修复 `filter_remote` 字段处理问题
- 优化策略映射逻辑
- 改进日志输出

### V5.0

- 重构核心架构
- 支持远程规则引用
- 新增策略组映射功能
- 优化 MITM hostname 处理

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

---

## 许可证

本项目采用 MIT 许可证。

---

## 联系方式

如有问题或建议，请在 GitHub Issues 中提出。

---

**文档生成日期**: 2026-03-01
