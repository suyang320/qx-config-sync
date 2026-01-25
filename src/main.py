# src/main.py

import yaml
import os
from qx_core import QXConfigManager

# 定义路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "profiles", "config.yaml")
OUTPUT_FILE = os.path.join(BASE_DIR, "MyQuantumultX.conf")

def main():
    print("🚀 === QX 配置构建器启动 ===")

    # 1. 读取 YAML 配置文件
    print(f"📂 读取配置: {CONFIG_PATH}")
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("❌ 错误: 找不到 config.yaml，请检查路径")
        return

    manager = QXConfigManager()

    # 2. 下载并加载底包
    # 从 yaml 的 base 节点读取 url
    manager.load_from_url(config['base']['url'])

    # ==========================================
    # 3. 执行补丁清洗 (Sanitizer) - 核心功能
    # ==========================================
    if 'patches' in config:
        print("\n🧹 === 执行规则清洗 ===")
        for section, rules in config['patches'].items():
            strategy = rules.get('strategy', 'blacklist') # 默认为黑名单
            keywords = rules.get('keywords', [])
            # 调用 core 的清洗方法
            manager.patch_section(section, keywords, strategy)
        print("=== 清洗结束 ===\n")

    # 4. 覆写通用设置 [general]
    # 例如：修复 GeoIP 源，修改测速地址
    if 'general' in config:
        for k, v in config['general'].items():
            manager.set_general(k, v)
            print(f"⚙️  [General] 设置: {k}={v}")

    # 5. 追加 DNS [dns]
    if 'dns' in config:
        for line in config['dns']:
            manager.add_list_item("dns", line, position="end")

    # 6. 追加自定义策略组 [policy]
    if 'custom_policies' in config:
        for line in config['custom_policies']:
            manager.add_list_item("policy", line, position="end")

    # 7. 注入本地分流 [filter_local]
    if 'local_filters' in config:
        # 7.1 处理 Top 规则 (高优先级，如内网直连)
        # 这里的规则会插到 filter_local 的最前面
        for rule in config['local_filters'].get('top', []):
            # 策略映射：把 yaml 里的 key (如 my_home) 替换成真实的策略名
            for map_k, map_v in config['policy_map'].items():
                # 简单字符串替换，把 ", my_home," 换成 ", 🏠 家庭网络,"
                rule = rule.replace(f", {map_k},", f", {map_v},")
            manager.add_list_item("filter_local", rule, position="start")

        # 7.2 处理 Bottom 规则 (低优先级，如 GeoIP)
        for rule in config['local_filters'].get('bottom', []):
            manager.add_list_item("filter_local", rule, position="end")

    # 8. 注入远程分流 [filter_remote]
    # 这里处理 Blackmatrix7 或其他源的引用
    if 'remote_filters' in config:
        for item in config['remote_filters']:
            # 8.1 确定 URL
            if item.get('source') == 'blackmatrix7':
                name = item['name']
                # 自动拼接 Blackmatrix7 的 GitHub 路径
                url = f"https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/{name}/{name}.list"
            else:
                # 如果不是内置源，直接用 yaml 里写的 url
                url = item['url']

            # 8.2 确定策略
            raw_policy = item['policy']
            # 从映射表中查找真实策略名，找不到就用原名
            final_policy = config['policy_map'].get(raw_policy, raw_policy)

            manager.add_remote_rule(url, item['tag'], final_policy)
            print(f"☁️  [Remote] 添加引用: {item['tag']} -> {final_policy}")

    # 9. 保存文件
    print("-" * 30)
    manager.save(OUTPUT_FILE)
    print("✨ === 构建完成 ===")

if __name__ == "__main__":
    main()