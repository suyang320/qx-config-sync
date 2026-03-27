import yaml
import os
import sys
import logging
import re
import time
import requests

# === 【关键修复】确保能导入 qx_core ===
# 获取当前脚本所在目录 (src)
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将 src 目录加入 Python 搜索路径
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from qx_core import QXConfigManager, logger
except ImportError as e:
    print(f"❌ 严重错误: 无法导入 qx_core.py。请检查该文件是否在 {current_dir} 目录下。")
    print(f"详细错误: {e}")
    sys.exit(1)

# === 路径定义 ===
# 项目根目录 (src 的上一级)
BASE_DIR = os.path.dirname(current_dir)
CONFIG_PATH = os.path.join(BASE_DIR, "profiles", "config.yaml")
OUTPUT_FILE = os.path.join(BASE_DIR, "MyQuantumultX.conf")
LOCALIZED_OUTPUT_FILE = os.path.join(BASE_DIR, "MyQuantumultX_Local.conf")
RULES_DIR = os.path.join(BASE_DIR, "rules")

# ==========================================
# 🔴 GitHub 仓库 Raw 链接前缀配置
# ==========================================
# 优先从环境变量读取，读取不到则使用这里配置的值
URL_RAW_PREFIX = "https://raw.githubusercontent.com/suversal/qx-config-sync/main/rules"

# ==========================================
# 📱 Telegram 通知配置 (可选)
# ==========================================
# 优先从环境变量读取，读取不到则使用这里配置的值
TELEGRAM_BOT_TOKEN = "xxx"
TELEGRAM_CHAT_ID = "xxx"

# KV 类型的节点 (覆盖式)
KV_SECTIONS = {"general", "mitm", "http_backend"}

# 【关键修改】需要特殊处理的节点列表 (在通用循环中跳过)
# local_filters: 有 top/bottom 逻辑，需单独处理
# filter_remote: 内容是字典，需单独处理
# remote_filters: 兼容旧版本字段
# base/patches/policy_map: 非节点配置
SKIP_SECTIONS = [
    "base", "patches", "policy_map",
    "local_filters", "remote_filters",
    "filter_remote" # <--- 这次报错就是因为缺了这个
]

def check_environment():
    """环境自检"""
    if not os.path.exists(RULES_DIR):
        try:
            os.makedirs(RULES_DIR)
            logger.info(f"📂 [Init] 自动创建规则目录: {RULES_DIR}")
        except Exception:
            pass

def resolve_rules(manager, raw_rules, mapping=None):
    """递归解析规则 (支持 file:// 和 策略映射)"""
    final_rules = []
    if not raw_rules: return []
    # 兼容单个字符串的情况
    if isinstance(raw_rules, str): raw_rules = [raw_rules]

    for rule in raw_rules:
        # 过滤 None 或空字符串 (防止 YAML 解析出 None 导致崩溃)
        if not rule:
            continue

        # 如果规则是字典 (比如错误地进入了这里)，跳过或报错，防止崩溃
        if isinstance(rule, dict):
            logger.warning(f"⚠️ [Skip] 跳过无法解析的字典规则: {rule}")
            continue

        # 处理文件引用
        if rule.startswith("file://"):
            file_path = rule.replace("file://", "").strip()
            # 这里的日志由 Core 打印
            file_content = manager.load_rules_from_file(file_path)
            final_rules.extend(resolve_rules(manager, file_content, mapping))
        else:
            # 处理策略映射
            if mapping:
                for k, v in mapping.items():
                    # 替换规则中的策略组 (如 ", proxy," -> ", 🚀 节点选择,")
                    if f", {k}," in rule:
                        rule = rule.replace(f", {k},", f", {v},")
            final_rules.append(rule)
    return final_rules

def localize_remote_rules(manager, github_prefix):
    """抓取远程链接并保存到本地，替换为自己的仓库链接"""
    logger.info("🌐 [Localize] 开始抓取并本地化远程规则链接...")
    sections_to_process = ["filter_remote", "rewrite_remote"]
    
    for sec in sections_to_process:
        if sec not in manager.sections:
            continue
            
        new_lines = []
        sec_dir = os.path.join(RULES_DIR, sec)
        if not os.path.exists(sec_dir):
            os.makedirs(sec_dir)
            
        for line in manager.sections[sec]:
            if not line or line.startswith("#") or line.startswith(";"):
                new_lines.append(line)
                continue
                
            # 正则匹配提取 URL 和后面的参数(如 tag=xxx)
            match = re.match(r'^(https?://[^,]+)(.*)$', line.strip())
            if match:
                original_url = match.group(1)
                rest_of_line = match.group(2)
                
                # 提取文件名
                file_name = original_url.split('/')[-1]
                if "?" in file_name: file_name = file_name.split("?")[0]
                if not file_name: file_name = "unknown.txt"
                    
                local_path = os.path.join(sec_dir, file_name)
                
                logger.info(f"⬇️ 正在下载: {file_name}")
                logger.info(f"   🔗 源地址: {original_url}")
                logger.info(f"   📁 保存至: {local_path}")
                
                try:
                    # 模拟 QX 客户端的 UA，使用 requests 统一 HTTP 客户端
                    headers = {'User-Agent': 'Quantumult X/1.0.31'}
                    response = requests.get(original_url, headers=headers, timeout=1)
                    response.raise_for_status()
                    content = response.content
                    with open(local_path, 'wb') as f:
                        f.write(content)
                    size_kb = len(content) / 1024
                    logger.info(f"   ✅ 下载成功! 文件大小: {size_kb:.2f} KB")

                    # 替换为自己的 GitHub 链接
                    new_url = f"{github_prefix}/{sec}/{file_name}"
                    new_lines.append(f"{new_url}{rest_of_line}")
                    # 间隔1秒避免风控
                    time.sleep(1)
                except Exception as e:
                    logger.error(f"  ❌ 下载失败 {original_url}: {e}")
                    new_lines.append(line) # 下载失败则保留原链接，防止丢失
                    # 即使失败也等待1秒，避免频繁请求
                    time.sleep(1)
            else:
                new_lines.append(line)
                
        # 更新内存中的配置列表
        manager.sections[sec] = new_lines

def send_telegram_message(bot_token, chat_id, message):
    """发送 Telegram 消息通知"""
    if not bot_token or not chat_id:
        logger.debug("⚠️ 未配置 Telegram，跳过通知")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        logger.info("📤 [Telegram] 通知发送成功")
        return True
    except Exception as e:
        logger.error(f"❌ [Telegram] 通知发送失败: {e}")
        return False

def check_file_changed(file_path):
    """检查文件是否与之前版本有变化"""
    if not os.path.exists(file_path):
        return True  # 新文件肯定变化

    # Git 里的版本对比，或者工作区对比
    # 使用 git diff 检查是否有变化
    import subprocess
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", str(file_path)],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        # 如果输出不为空，说明有变化
        return bool(output)
    except Exception as e:
        # 如果 git 命令失败，简单对比内容哈希（和上一次相比）
        import hashlib
        logger.debug(f"⚠️ Git 检查失败，使用哈希对比: {e}")
        return True

def build_notification_message(build_success, stats, changed_files):
    """构建通知消息"""
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 从 GitHub Actions 环境变量获取额外信息
    github_repo = os.environ.get('GITHUB_REPOSITORY', '')
    github_sha = os.environ.get('GITHUB_SHA', '')[:7]  # 只取短哈希

    status_emoji = "✅" if build_success else "❌"
    status_text = "构建成功" if build_success else "构建失败"

    message = (
        f"{status_emoji} <b>Quantumult X 配置自动构建完成</b>\n\n"
        f"⏰ <b>构建时间:</b> {now}\n"
    )

    # 如果在 GitHub Actions 运行，添加仓库信息
    if github_repo:
        repo_url = f"https://github.com/{github_repo}"
        message += f"📦 <b>仓库:</b> <a href=\"{repo_url}\">{github_repo}</a>\n"
        if github_sha:
            commit_url = f"{repo_url}/commit/{github_sha}"
            message += f"🔖 <b>最新提交:</b> <a href=\"{commit_url}\">{github_sha}</a>\n"

    message += (
        f"\n📊 <b>构建统计</b>\n"
        f"• 远程规则下载: {stats['download_success']} 成功, {stats['download_failed']} 失败\n"
        f"• 注入自定义规则: {stats['rules_added']} 条\n"
    )

    if changed_files:
        message += f"\n🔄 <b>检测到配置更新:</b>\n"
        for f in changed_files:
            message += f"  • {os.path.basename(f)}\n"
    else:
        message += f"\n✓ <b>配置文件无变化</b>\n"

    if stats['download_failed'] > 0:
        message += f"\n⚠️ 注意: 有 {stats['download_failed']} 个文件下载失败，请检查日志\n"

    message += f"\n#QXConfig #AutoSync"
    return message

def main():
    logger.info("🚀 === QX Builder V5.1 (Fixed) Started ===")
    check_environment()

    # 优先读取 Telegram 配置
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', TELEGRAM_BOT_TOKEN)
    chat_id = os.environ.get('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID)

    try:
        if not os.path.exists(CONFIG_PATH):
            logger.error(f"❌ 找不到配置文件: {CONFIG_PATH}")
            raise FileNotFoundError(f"配置文件不存在: {CONFIG_PATH}")

        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        manager = QXConfigManager()

        # 1. 下载底包
        if config and 'base' in config:
            manager.load_from_url(config['base']['url'])

        # 2. 全局清洗 (Patches)
        if config and 'patches' in config:
            logger.info("🧹 [Step] 执行配置清洗 (Patches)...")
            for section, rules in config['patches'].items():
                manager.patch_section(section, rules.get('keywords', []), rules.get('strategy', 'blacklist'))

        # 3. 动态处理大部分节点 (General, DNS, Policy, Rewrite...)
        policy_map = config.get('policy_map', {}) if config else {}

        if config:
            for section_name, content in config.items():
                # 跳过特殊处理的字段
                if section_name in SKIP_SECTIONS:
                    continue

                # 处理 KV 节点 (General, MITM) - 覆盖模式
                if section_name in KV_SECTIONS:
                    if isinstance(content, dict):
                        for k, v in content.items():
                            # 支持 mitm hostname 引用文件
                            if isinstance(v, str) and v.startswith("file://"):
                                resolved = resolve_rules(manager, [v], None)
                                v = resolved[0] if resolved else ""
                            manager.set_kv(section_name, k, str(v))

                # 处理 List 节点 (DNS, Policy, Server...) - 追加模式
                else:
                    if isinstance(content, list):
                        # 这里只会处理纯字符串列表，不会再处理 filter_remote 的字典了
                        rules = resolve_rules(manager, content, policy_map)
                        if rules:
                            logger.info(f"⚡️ [Inject] 向 [{section_name}] 注入 {len(rules)} 条规则")
                            for rule in rules:
                                # 【修改】对于 rewrite_remote，强制插入到头部 (start)
                                if section_name == "rewrite_remote":
                                    manager.add_list_item(section_name, rule, position="start")
                                else:
                                    manager.add_list_item(section_name, rule)

        # 4. 专门处理本地分流 (Local Filters - 支持 top/bottom)
        if config and 'local_filters' in config:
            logger.info("🌪 [Step] 处理本地分流 (Local Filters)...")
            if 'top' in config['local_filters']:
                rules = resolve_rules(manager, config['local_filters']['top'], policy_map)
                logger.info(f"   └── 注入 Top 规则: {len(rules)} 条")
                for r in rules: manager.add_list_item("filter_local", r, "start")

            if 'bottom' in config['local_filters']:
                rules = resolve_rules(manager, config['local_filters']['bottom'], policy_map)
                logger.info(f"   └── 注入 Bottom 规则: {len(rules)} 条")
                for r in rules: manager.add_list_item("filter_local", r, "end")

        # 5. 专门处理远程分流 (Remote Filters / filter_remote)
        # 兼容两种写法：标准的 filter_remote 和 旧版的 remote_filters
        remote_conf = config.get('filter_remote') or config.get('remote_filters')

        download_stats = {"success": 0, "failed": 0}
        if remote_conf:
            logger.info("☁️ [Step] 处理远程引用 (Remote Filters)...")
            for item in remote_conf:
                # 必须是字典格式才能处理
                if not isinstance(item, dict):
                    continue

                source = item.get('source')
                if source == 'blackmatrix7':
                    name = item['name']
                    url = f"https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/{name}/{name}.list"
                else:
                    url = item.get('url')

                if url:
                    manager.add_remote_rule(url, item.get('tag', 'Remote'), policy_map.get(item.get('policy'), item.get('policy')))

        # 6. 第一次保存：输出合并后的原始配置文件
        print("-" * 50)
        logger.info(f"💾 [Step] 第一次保存: 生成原始配置文件 -> {os.path.basename(OUTPUT_FILE)}")
        manager.save(OUTPUT_FILE)

        # 7. 抓取远程文件，并修改内存中的链接配置
        # 优先从环境变量读取，读取不到使用代码中配置的值
        url_raw_prefix = os.environ.get('URL_RAW_PREFIX', URL_RAW_PREFIX)
        print("-" * 50)
        download_stats = localize_remote_rules(manager, url_raw_prefix)

        # 8. 第二次保存：输出替换为你个人仓库直链的新配置文件
        print("-" * 50)
        logger.info(f"💾 [Step] 第二次保存: 生成本地化后的全新配置文件 -> {os.path.basename(LOCALIZED_OUTPUT_FILE)}")
        manager.save(LOCALIZED_OUTPUT_FILE)

        # 检查文件变化 (配置文件 + 下载的规则目录)
        logger.info("🔍 [Check] 检查配置文件和规则是否有变化...")
        changed_files = []
        # 检查输出配置文件
        for f in [OUTPUT_FILE, LOCALIZED_OUTPUT_FILE]:
            if check_file_changed(f):
                changed_files.append(f)

        # 检查规则目录中的变化
        import subprocess
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain", "rules/filter_remote/", "rules/rewrite_remote/"],
                capture_output=True,
                text=True
            )
            output = result.stdout.strip()
            if output:
                # 有变化，添加目录
                changed_files.append(os.path.join(RULES_DIR, "filter_remote"))
                changed_files.append(os.path.join(RULES_DIR, "rewrite_remote"))
        except Exception as e:
            logger.debug(f"⚠️ 检查规则目录变化失败: {e}")

        if changed_files:
            changed_names = [os.path.basename(f) for f in changed_files]
            logger.info(f"📢 检测到有文件变化: {', '.join(changed_names)}")
        else:
            logger.info("✓ 无文件变化")

        logger.info("✨ === Build Complete ===")

        # Telegram 通知 - 构建成功
        if bot_token and chat_id:
            stats = {
                "download_success": download_stats["success"],
                "download_failed": download_stats["failed"],
                "rules_added": manager.stats["rules_added"]
            }
            message = build_notification_message(True, stats, changed_files)
            send_telegram_message(bot_token, chat_id, message)

        # 返回成功退出码
        sys.exit(0)

    except Exception as e:
        # 构建失败，发送 Telegram 通知
        logger.error(f"❌ 构建失败: {e}")
        if bot_token and chat_id:
            from datetime import datetime
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            github_repo = os.environ.get('GITHUB_REPOSITORY', '')

            message = (
                f"❌ <b>Quantumult X 配置构建失败</b>\n\n"
                f"⏰ <b>失败时间:</b> {now}\n"
            )
            if github_repo:
                repo_url = f"https://github.com/{github_repo}"
                message += f"📦 <b>仓库:</b> <a href=\"{repo_url}\">{github_repo}</a>\n"

            message += (
                f"\n⚠️ <b>错误信息:</b>\n"
                f"<code>{str(e)}</code>\n\n"
                f"请前往 GitHub Action 查看完整日志\n\n"
                f"#QXConfig #BuildFailed"
            )
            send_telegram_message(bot_token, chat_id, message)

        # 返回失败退出码
        sys.exit(1)

def localize_remote_rules(manager, github_prefix):
    """抓取远程链接并保存到本地，替换为自己的仓库链接"""
    logger.info("🌐 [Localize] 开始抓取并本地化远程规则链接...")
    sections_to_process = ["filter_remote", "rewrite_remote"]
    download_stats = {"success": 0, "failed": 0}

    for sec in sections_to_process:
        if sec not in manager.sections:
            continue

        new_lines = []
        sec_dir = os.path.join(RULES_DIR, sec)
        if not os.path.exists(sec_dir):
            os.makedirs(sec_dir)

        for line in manager.sections[sec]:
            if not line or line.startswith("#") or line.startswith(";"):
                new_lines.append(line)
                continue

            # 正则匹配提取 URL 和后面的参数(如 tag=xxx)
            match = re.match(r'^(https?://[^,]+)(.*)$', line.strip())
            if match:
                original_url = match.group(1)
                rest_of_line = match.group(2)

                # 提取文件名
                file_name = original_url.split('/')[-1]
                if "?" in file_name: file_name = file_name.split("?")[0]
                if not file_name: file_name = "unknown.txt"

                local_path = os.path.join(sec_dir, file_name)

                logger.info(f"⬇️ 正在下载: {file_name}")
                logger.info(f"   🔗 源地址: {original_url}")
                logger.info(f"   📁 保存至: {local_path}")

                try:
                    # 模拟 QX 客户端的 UA，使用 requests 统一 HTTP 客户端
                    headers = {'User-Agent': 'Quantumult X/1.0.31'}
                    response = requests.get(original_url, headers=headers, timeout=15)
                    response.raise_for_status()
                    content = response.content
                    with open(local_path, 'wb') as f:
                        f.write(content)
                    size_kb = len(content) / 1024
                    logger.info(f"   ✅ 下载成功! 文件大小: {size_kb:.2f} KB")

                    # 替换为自己的 GitHub 链接
                    new_url = f"{github_prefix}/{sec}/{file_name}"
                    new_lines.append(f"{new_url}{rest_of_line}")
                    # 间隔1秒避免风控
                    download_stats["success"] += 1
                    time.sleep(1)
                except Exception as e:
                    logger.error(f"  ❌ 下载失败 {original_url}: {e}")
                    new_lines.append(line) # 下载失败则保留原链接，防止丢失
                    # 即使失败也等待1秒，避免频繁请求
                    download_stats["failed"] += 1
                    time.sleep(1)
            else:
                new_lines.append(line)

        # 更新内存中的配置列表
        manager.sections[sec] = new_lines

    logger.info(f"📊 [Localize] 本地化完成: {download_stats['success']} 成功, {download_stats['failed']} 失败")
    return download_stats

if __name__ == "__main__":
    main()