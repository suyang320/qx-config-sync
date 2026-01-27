import yaml
import os
import sys
import logging

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
RULES_DIR = os.path.join(BASE_DIR, "rules")

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

def main():
    logger.info("🚀 === QX Builder V5.1 (Fixed) Started ===")
    check_environment()

    if not os.path.exists(CONFIG_PATH):
        logger.error(f"❌ 找不到配置文件: {CONFIG_PATH}")
        return

    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"❌ 读取 config.yaml 失败: {e}")
        return

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

    # 6. 保存
    print("-" * 50)
    manager.save(OUTPUT_FILE)
    logger.info("✨ === Build Complete ===")

if __name__ == "__main__":
    main()