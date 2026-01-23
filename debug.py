from qx_parser import QXConfigManager

# 墨鱼最新配置地址
URL = "https://ddgksf2013.top/Profile/QuantumultX.conf"

def inspect_policy_names():
    manager = QXConfigManager()
    manager.load_from_url(URL)

    print("\n" + "="*40)
    print("🕵️‍♂️  探测到的策略组名称 (请复制这些名字)")
    print("="*40)

    # 打印 [policy] 段落下的所有 key
    # 墨鱼的格式通常是: static=🚀 节点选择, ...
    if "policy" in manager.sections:
        for line in manager.sections["policy"]:
            # 提取等号左边的名字，或者 parse 具体的 pattern
            # 简单粗暴提取：通常紧跟在 static=, available=, round-robin= 后面
            # 示例: static=🚀 节点选择, ...
            parts = line.split(',')
            for part in parts:
                if "=" in part and ("static" in part or "available" in part or "round-robin" in part):
                    # 提取策略组名
                    policy_name = part.split('=')[1].strip()
                    print(f"👉 {policy_name}")
                    break
    else:
        print("❌ 未找到 [policy] 段落，可能是下载内容为空或解析失败")
    print("="*40 + "\n")

if __name__ == "__main__":
    inspect_policy_names()