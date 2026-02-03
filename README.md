# QX-Config-Sync (Quantumult X 配置同步工具)

**QX-Config-Sync** 是一个基于 Python 的自动化配置生成工具，专为 iOS 代理软件 **Quantumult X** 设计。

它的核心理念是：**“底包 + 增量配置 = 最终配置”**。

你不再需要手动维护一个几千行的庞大配置文件，也不用担心更新底包时丢失自己的个性化设置。只需维护一份极简的 `config.yaml`，脚本就会自动拉取最新的远程底包，注入你的自定义规则、策略和重写，生成最终可用的配置文件。

## ✨ 核心特性

*   **自动构建与持续集成 (CI/CD)**：告别手动复制粘贴。你只需要像写代码一样管理你的规则，每次提交（Push）代码到 GitHub，Action 机器人会自动运行构建脚本，生成一份最终可用的 `MyQuantumultX.conf`。
*   **自动同步底包**：自动下载并解析远程大神维护的 Quantumult X 配置文件（如 `ddgksf2013` 等）。
*   **增量更新**：你的个人配置（节点、分流、重写、MITM）独立存储，脚本运行时自动注入到底包中。
*   **智能清洗**：支持按关键字自动删除底包中不需要的策略组、DNS 或分流规则（如去除广告策略组）。
*   **优先级管理**：
    *   自定义的远程分流 (`filter_remote`) 和重写 (`rewrite_remote`) 自动置顶，优先级高于底包。
    *   本地分流 (`local_filters`) 支持 `top` (置顶) 和 `bottom` (垫底) 插入模式。
*   **策略映射**：自动将远程规则中的策略名（如 `proxy`, `streaming`）映射为你本地真实的策略组（如 `🚀 节点选择`, `🌍 国外媒体`）。
*   **MITM 智能追加**：自动合并底包和本地的 MITM Hostname 列表，避免覆盖丢失。
*   **模块化管理**：支持将复杂的规则、重写、MITM 列表拆分为独立文件管理。

## 🚀 快速开始

### 1. 环境准备
*   Python 3.6+
*   依赖库：`requests`, `pyyaml`

### 2. 配置你的规则
编辑 `profiles/config.yaml` 文件。这是你唯一需要维护的文件。

### 3. 运行生成
运行主程序，脚本会自动处理所有逻辑并生成最终文件。

### 4. 使用配置
生成的配置文件位于项目根目录：`MyQuantumultX.conf`。
你可以将此文件托管到 GitHub Gist 或私有仓库，然后在 Quantumult X 中引用该链接。

## 📂 项目结构
```yaml
qx-config-sync/
├── profiles/
│   └── config.yaml        # 你的核心配置文件
├── rules/                 # (可选) 存放本地规则文件
│   ├── my_custom.list
│   └── my_mitm.list
├── src/
│   ├── main.py            # 主程序入口
│   └── qx_core.py         # 核心处理逻辑
├── MyQuantumultX.conf     # [生成] 最终配置文件
└── README.md
```
## 🛠 部分配置示例

#### 基础源与订阅
```yaml
# 你的机场/自建节点订阅链接
server_remote:
  - "[https://example.com/api/v1/client/subscribe?token=xxx](https://example.com/api/v1/client/subscribe?token=xxx), tag=我的机场, enabled=true"

# 底包来源 (建议使用原作者的 Raw 链接)
base_config_url: "[https://raw.githubusercontent.com/ddgksf2013/Profile/master/QuantumultX.conf](https://raw.githubusercontent.com/ddgksf2013/Profile/master/QuantumultX.conf)"
```
#### 自定义策略组 (Policy)
```yaml
policy:
  # 定义一个名为 "香港节点" 的策略组，自动抓取包含 HK 或 港 的节点
  - "static=香港节点, server-tag-regex=(?=.*(港|HK)), img-url=..."
  
  # 定义一个嵌套策略组，包含上面的香港节点
  - "static=Netflix, 香港节点, 美国节点, img-url=..."
```
#### 引用外部规则 (Rules)
```yaml
# 远程引用 (订阅大佬的规则集)
rewrite_remote:
  - "[https://raw.githubusercontent.com/DivineEngine/Profiles/master/Quantumult/Rewrite/BlockAdvertising.conf](https://raw.githubusercontent.com/DivineEngine/Profiles/master/Quantumult/Rewrite/BlockAdvertising.conf), tag=去广告, update-interval=86400, opt-parser=true, enabled=true"

# 本地引用 (引用你自己写的规则)
rewrite_local:
  - "file://rules/my_scripts.conf"
```
#### 规则清洗 (Patches)
```yaml
patches:
  policy:
    keywords:
      - "香港节点"  # 删除底包中所有包含 "香港节点" 的行
      - "广告拦截"  # 删除底包中你不喜欢的策略组
  rewrite_remote:
    keywords:
      - "Youtube"   # 删除底包自带的 Youtube 重写
```
