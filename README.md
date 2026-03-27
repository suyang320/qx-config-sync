# QX-Config-Sync (Quantumult X 配置自动同步工具)

**QX-Config-Sync** 是一个基于 Python 的自动化配置生成工具，专为 iOS 代理软件 **Quantumult X** 设计。

它的核心理念是：**「底包 + 你的增量配置 = 最终可用配置」**。

你不再需要手动维护一个几千行的庞大配置文件，也不用担心更新底包时丢失自己的个性化设置。只需维护一份极简的 `config.yaml`，脚本就会：
1. 自动拉取最新的远程底包
2. 注入你的自定义规则、策略、节点和重写
3. 下载所有远程规则到你自己的仓库
4. 生成最终可用的配置文件
5. 自动提交回你的 GitHub，并通过 Telegram 通知你构建结果

---

## ✨ 核心特性 & 项目亮点

### 🤖 全自动无人值守
- GitHub Action 每日自动运行，无需你手动操作
- 每天帮你拉取最新底包，同步最新规则，生成最新配置
- 自动提交所有变化回你的仓库，永远保持最新

### 📩 贴心的 Telegram 通知
- **构建成功**：告诉你本次构建下载了多少规则，哪些文件有变化
- **构建失败**：直接把错误信息推送给你，不用去 GitHub 翻日志也能知道问题
- 只要配置有变化就会提醒你，没变化也会告诉你一切正常
- 支持 HTML 格式化排版，信息清晰易读

### 🌏 独家规则本地化功能
- 自动遍历你配置中所有 `filter_remote` 和 `rewrite_remote` 远程链接
- 自动把这些远程规则文件下载到**你自己的 GitHub 仓库**
- 自动把配置中的原远程链接替换为**你仓库的 Raw 链接**
- ✅ **彻底解决**：原链接失效、原服务器限速、CDN 缓存过期等问题
- ✅ 你的配置永远可用，不会因为大佬改链接导致规则失效

### 🚀 增量配置设计，极度省心
- 你只需要维护**一份很小的 `config.yaml`**，只写你和底包不同的部分
- 不需要手动复制粘贴，不需要维护几千行的大配置
- 更新底包时不会覆盖你的个性化设置，永远保留你的修改

### 🧹 智能清洗帮你精简配置
- 支持按关键词删除底包中你不需要的内容
- 比如你不想要底包自带的某些策略组、某些规则，一句话配置就自动删掉
- 让你的配置更干净，用起来更清爽

### 🎯 灵活的优先级控制
- 你自定义的所有规则，默认自动插入到底包规则的**最前面**，优先级更高
- 本地分流支持两种模式：
  - `top`：插入到最前面，优先级最高（适合你自己的规则优先匹配）
  - `bottom`：插入到最后面，优先级最低（适合兜底规则）

### 🔍 其他实用细节
- **策略映射**：自动把远程规则里的策略名（比如 `us-node`）替换成你自己的策略组名字，不用大佬规则适配你的策略
- **MITM 智能追加**：自动合并底包和你的 Hostname，不会覆盖掉底包原有的配置
- **模块化管理**：支持把大量规则拆分成多个小文件存放，更方便管理
- **防风控设计**：每下载一个文件等待 1 秒，避免被对方服务器拦截，下载成功率更高
- **失败重试兼容**：单个文件下载失败不影响整个构建，自动保留原链接，不会让你配置缺东西

---

## 🚀 新手一键部署

### 1. Fork 本仓库到你的账号

点击右上角 **Fork** 按钮，把这个仓库复制一份到你的 GitHub 账号。

### 2. 配置你的个性化设置

编辑 `profiles/config.yaml` 文件，这是你唯一需要维护的文件：

*   修改 `base.url` 为你想要的底包地址
*   在 `server_remote` 添加你的机场订阅链接
*   在 `policy` 自定义你的策略组
*   在 `rewrite_remote` 添加你需要的重写规则

> ✅ 里面已经写好详细注释，照着改就行

### 3. 在 GitHub 添加 Secrets

打开你的 GitHub 仓库 → 点击 `Settings` → 点击 `Secrets and variables` → `Actions` → 点击 `New repository secret`

添加以下三个 Secrets（如果你已经把token填在代码里，可以只加后两个）：

| Name | Value |
|------|-------|
| `GITHUB_RAW_PREFIX` | `https://raw.githubusercontent.com/你的GitHub用户名/qx-config-sync/main/rules` |
| `TELEGRAM_BOT_TOKEN` | 你的 Telegram Bot Token（从 @BotFather 获取） |
| `TELEGRAM_CHAT_ID` | 你的 Telegram Chat ID（从 @getidsbot 获取） |

### 4. 启用 GitHub Actions

1. 点击你的仓库 → `Actions`
2. 点击 `I understand my workflows, go ahead and enable them`
3. 每天北京时间 **早上 6 点** 会自动运行构建
4. 你也可以手动触发：点击 `Actions` → `QX Builder` → `Run workflow`

---

## 📂 项目结构

```yaml
qx-config-sync/
├── .github/workflows/
│   └── build.yml              # GitHub Action 自动构建配置
├── profiles/
│   └── config.yaml           # 👈 你的核心配置文件（改这里！）
├── rules/                     # 存放本地化后的规则文件
│   ├── filter_remote/        # 本地化后的远程分流规则
│   └── rewrite_remote/       # 本地化后的远程重写规则
├── src/
│   ├── main.py               # 主程序入口
│   └── qx_core.py            # 核心处理逻辑
├── MyQuantumultX.conf        # [生成] 最终原始配置文件
├── MyQuantumultX_Local.conf  # [生成] 本地化后的配置文件（所有规则都存在你仓库，推荐用这个）
└── README.md
```

---

## ⚙️ 本地运行（开发调试用）

如果你想在自己电脑上运行：

### 1. 环境准备
*   Python 3.6+
*   安装依赖：
```bash
pip install -r requirements.txt
```

### 2. 运行构建
```bash
python src/main.py
```

### 3. 获取结果
生成了**两个配置文件**，两个都可以直接导入 Quantumult X 使用：

| 配置文件 | 说明 | 推荐使用场景 |
|---------|------|-------------|
| `MyQuantumultX.conf` | 保留所有规则的**原始远程链接**，只合并你的配置，不下载规则到本地 | 原链接都稳定可用，想保持最小仓库大小 |
| `MyQuantumultX_Local.conf` | 所有可下载的远程规则都已经下载到**你自己的仓库**，链接也替换成你的仓库地址 | 担心原链接失效、原链接限速，想要更稳定的体验 |

> 💡 如果使用原始链接时发现部分规则加载失败，直接切换到 `MyQuantumultX_Local.conf` 就能解决问题。

---

## 📝 完整配置说明（逐段解释 `config.yaml`）

`profiles/config.yaml` 是你唯一需要维护的文件，下面逐段解释每一部分怎么用：

### 🔹 `base` - 底包地址（必须）
```yaml
base:
  url: "https://ddgksf2013.top/Profile/QuantumultX.conf"
```
**作用**：你的整个配置基于这个"底包"来修改，底包一般是大佬维护好的完整配置，你只需要增量修改它。

**推荐**：默认已经填好了 ddgksf2013 的底包，直接用就好。

---

### 🔹 `patches` - 清洗底包（可选）
```yaml
patches:
  policy:
    keywords:
      - "Hijacking"   # 删除所有名字里带 "Hijacking" 的策略组
      - "广告"         # 删除所有名字里带 "广告" 的策略组
```
**作用**：在注入你的配置之前，先把底包里**你不想要的内容删掉**，让配置更干净。

**用法**：
- `patches.策略组名称`：你要清洗哪个段落（比如 `policy` 就是策略组段落）
- `keywords`：列出你要删除的内容包含的关键词

---

### 🔹 `general` - 全局设置（可选）
```yaml
general:
  geoip-url: "https://github.com/Hackl0us/GeoIP2-CN/raw/release/Country.mmdb"
  resource_parser_url: "https://raw.githubusercontent.com/KOP-XIAO/QuantumultX/master/Scripts/resource-parser.js"
```
**作用**：这里配置 Quantumult X 的全局参数，会**强制覆盖**底包里的对应参数。

常用配置：
- `geoip-url`: 更新 GeoIP 数据库（解决底包数据过时问题）
- `resource_parser_url`: 资源解析器地址
- `server_check_url`: 节点测速地址

---

### 🔹 `dns` - 自定义 DNS（可选）
```yaml
dns:
  - "server=/suversal.com/192.168.1.1" # 你的内网域名走内网 DNS
```
**作用**：添加自定义 DNS 规则。

---

### 🔹 `policy_map` - 策略组映射（必须）
```yaml
policy_map:
  us-node: "美国节点"      # 外部规则叫 us-node → 实际走你配置的「美国节点」策略组
  direct: "direct"
  reject: "reject"
```
**作用**：当你引用第三方远程规则时，第三方规则里的策略名需要映射到你自己的策略组名字，这里就是做这个映射的。

**用法**：`"第三方规则里的名字": "你自己策略组的名字"`

---

### 🔹 `policy` - 自定义策略组（必须）
```yaml
policy:
  # 1. 自动测速分组：定期自动选延迟最低的节点
  - "url-latency-benchmark=香港节点, server-tag-regex=(?=.*(港|HK|(?i)Hong))^((?!(台|日|韩|新|美)).)*$, check-interval=900, tolerance=0, img-url=https://raw.githubusercontent.com/Orz-3/mini/master/Color/HK.png"

  # 2. 静态分组：固定包含这些节点/策略
  - "static=苹果服务, direct, 香港节点, 台湾节点, 美国节点, img-url=..."
```
**作用**：这里定义你自己的所有策略组，这是配置的核心部分。

两种类型：
- `url-latency-benchmark=`：自动测速分组，根据延迟自动选择最优节点
- `static=`：静态分组，你手动指定包含哪些节点/其他策略

参数说明：
- `server-tag-regex=正则表达式`：自动从你的订阅里匹配符合规则的节点
- `check-interval=900`：测速间隔，单位是秒（900秒 = 15分钟）
- `img-url=`：策略组图标链接

---

### 🔹 `server_remote` - 你的机场订阅（必须）
```yaml
server_remote:
  - "https://你的机场订阅链接, tag=我的机场, enabled=true"
```
**作用**：填写你的机场节点订阅链接，Quantumult X 会自动拉取你的节点。

---

### 🔹 `local_filters` - 本地分流规则（可选）
```yaml
local_filters:
  top:
    - "file://rules/my_custom.list"  # 从本地文件读取规则
    - "ip6-cidr,::/0,direct"           # 或者直接写在这里
  bottom:
    - "geoip,cn,direct"
```
**作用**：添加你自己的本地分流规则。

位置说明：
- `top`：插到**所有分流规则最前面**，优先级最高（适合你自己的规则优先匹配）
- `bottom`：插到**所有分流规则最后面**，优先级最低（适合兜底规则）

格式说明：
- `file://路径`：从 `rules/` 目录下读取文件，方便你把大量规则分开管理

---

### 🔹 `filter_remote` - 远程分流规则（可选）
```yaml
filter_remote:
  - name: "TikTok"
    source: "blackmatrix7" # 内置简写，自动生成正确链接
    policy: "us-node"      # 这些分流走哪个策略
    tag: "TikTok"
```
**作用**：引用第三方远程分流规则。

支持内置简写：`source: "blackmatrix7"` 会自动拼接正确的规则地址，不用你记长链接。

---

### 🔹 `rewrite_local` - 本地重写（可选）
```yaml
rewrite_local:
  - "file://rules/my_rewrites.list" # 从本地文件读取
  - "^https://google.cn url 302 https://google.com" # 直接写在这里
```
**作用**：添加你自己的本地重写规则（重写用来做去广告、修改响应、跳转等）。

---

### 🔹 `rewrite_remote` - 远程重写（推荐添加）
```yaml
rewrite_remote:
  - "https://limbopro.com/Adblock4limbo.conf, tag=毒奶特供(去网页广告计划), enabled=true"
```
**作用**：引用第三方远程重写规则（一般用来去广告）。

本工具会**自动下载这些文件到你自己仓库**，并替换链接为你的仓库地址，不怕原链接失效。

---

### 🔹 `task_local` - 定时任务（可选）
```yaml
task_local:
  - "0 9 * * * https://example.com/sign.js, tag=每日签到"
```
**作用**：添加 Quantumult X 定时任务（比如自动签到）。

---

### 🔹 `mitm` - MITM 配置（可选）
```yaml
mitm:
  hostname: "file://rules/my_mitm_hosts.list"
```
**作用**：配置 HTTPS 解密需要的域名列表。

> 💡 提示：如果域名很多，建议放在 `rules/` 目录下的单独文件里引用，不要直接写在 `config.yaml` 里，更干净。

---

## ❓ 常见问题

### Q: 什么是「规则本地化」？为什么需要这个？
A: 很多去广告规则大佬会更新他们的规则，但是原链接有时候会限速或者失效。本地化就是把这些规则下载到**你自己的 GitHub 仓库**，这样你的 Quantumult X 每次都是从你的仓库拉取，稳定不失效。

### Q: 多久自动构建一次？
A: 默认是每天北京时间早上 6 点自动构建一次，保证你拿到最新规则。你也可以随时手动构建。

### Q: 构建完了怎么在 Quantumult X 使用？
A: 两个配置文件都可以用，根据你的需要选：
- 推荐用本地化版本：复制 `https://raw.githubusercontent.com/你的用户名/qx-config-sync/main/MyQuantumultX_Local.conf`
- 如果想用原始链接：复制 `https://raw.githubusercontent.com/你的用户名/qx-config-sync/main/MyQuantumultX.conf`

打开 Quantumult X → 配置 → 下载配置 → 填入链接 → 导入就可以用了。

### Q: 为什么配置好后 Telegram 收不到通知？
A: 检查一下：
1. Bot Token 和 Chat ID 是否正确
2. 你需要先给你的 Bot 发一条消息，否则 Bot 没法主动给你发消息
3. 检查 GitHub Secrets 名字是否正确，不能有空格

### Q: 构建失败了怎么办？
A: Telegram 会通知你构建失败，并且告诉你错误原因。你可以去 GitHub → Actions → 最新一次运行那里看完整日志。大部分情况是：
1. 你的 `config.yaml` 格式错了（YAML 对缩进要求严格，仔细检查）
2. 某个远程链接下载失败（一般重试一次就好，或者换个链接）

---

## 📊 当前版本更新日志

*   ✅ 添加 Telegram 通知，成功失败都提醒，显示变化文件
*   ✅ 添加 1 秒下载间隔，防止被风控拦截
*   ✅ 统一 HTTP 客户端，更稳定
*   ✅ 所有配置支持环境变量，安全适配 GitHub Secrets
*   ✅ 自动检测配置文件和规则目录变化

---

## 👍 感谢各方分享

本项目配置中使用了以下大佬分享的底包、规则和资源，在此特别感谢：

*   **底包**: [ddgksf2013](https://github.com/ddgksf2013) - 提供了非常完善的 Quantumult X 基础配置
*   **分流规则**: [blackmatrix7](https://github.com/blackmatrix7/ios_rule_script) - 维护了完整全面的去广告和分流规则
*   **去广告**:
    *   [limbopro](https://github.com/limbopro/Adblock4limbo) - 毒奶特供去网页广告计划
    *   [blackmatrix7](https://github.com/blackmatrix7/ios_rule_script) - 多种应用去广告规则
    *   [keleecn](https://github.com/keleecn) - 提供了多款国内 App 去广告 Loon 规则（兼容 QX）
*   **工具**:
    *   [Peng-YM](https://github.com/Peng-YM/Sub-Store) - 高级订阅管理器
    *   [iab0x00](https://github.com/iab0x00/ProxyRules) - PluginHub 转换规则
*   **图标资源**:
    *   [Orz-3](https://github.com/Orz-3/mini) - 极简风格图标
    *   [Koolson](https://github.com/Koolson/Qure) - 彩色风格图标
    *   [ddgksf2013](https://github.com/ddgksf2013) - 应用图标

感谢所有大佬的开源分享，让我们能用到这么好用的规则和配置！

---

## 致谢
感谢各位规则大佬分享的规则，也感谢前辈们的思路让这个项目更完善。
