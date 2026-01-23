# main.py
from qx_parser import QXConfigManager

# 墨鱼的源链接
BASE_URL = "https://ddgksf2013.top/Profile/QuantumultX.conf"
OUTPUT_FILE = "MyQuantumultX.conf"

# === 策略组常量定义 (适配墨鱼配置) ===
# 提示：如果生成后发现规则不生效，请检查 .conf 文件里的 [policy] 段落，确认这些中文名是否一致
PROXY_GROUP = "国外流量"       # 主力代理
DIRECT_GROUP = "国内网站"      # 直连
MEDIA_GROUP = "港台番剧"       # 流媒体
AD_GROUP = "广告拦截"          # 去广告/拒绝
APPLE_GROUP = "苹果服务"       # Apple 服务

def main():
    manager = QXConfigManager()

    # 1. 下载墨鱼配置
    manager.load_from_url(BASE_URL)

    # ==========================================
    # Part A: 个人内网与开发环境 (优先级最高)
    # ==========================================
    # 这些规则必须插入到最前面 (position="start")，否则会被墨鱼的 GeoIP 规则抢占

    local_rules = [
        # --- 你的 Mac Mini / Docker / NAS ---
        f"ip-cidr, 192.168.0.0/16, {DIRECT_GROUP}, tag=局域网",
        f"host-suffix, local, {DIRECT_GROUP}, tag=本地服务",

        # --- 你的个人网站 ---
        f"host-suffix, suversal.com, {DIRECT_GROUP}, tag=我的网站",

        # --- 开发工具加速 (例如 Maven 中央仓库走代理) ---
        f"host-suffix, maven.org, {PROXY_GROUP}, tag=Maven加速",
    ]

    for rule in local_rules:
        manager.add_rule("filter_local", rule, position="start")

    # ==========================================
    # Part B: 引用 Blackmatrix7 规则库 (Remote)
    # ==========================================
    # 语法: add_blackmatrix_remote(规则名, 策略组, 标签)

    # 1. AI 生产力 -> 走 "国外流量"
    manager.add_blackmatrix_remote("OpenAI", PROXY_GROUP, tag="ChatGPT")
    manager.add_blackmatrix_remote("Gemini", PROXY_GROUP, tag="Gemini")
    manager.add_blackmatrix_remote("GitHub", PROXY_GROUP, tag="GitHub")

    # 2. 媒体服务 -> 走 "港台番剧" (墨鱼专门优化的线路)
    manager.add_blackmatrix_remote("YouTube", MEDIA_GROUP, tag="YouTube")
    manager.add_blackmatrix_remote("Netflix", MEDIA_GROUP, tag="Netflix")

    # 3. 隐私与广告 -> 走 "广告拦截"
    manager.add_blackmatrix_remote("Advertising", AD_GROUP, tag="全球去广告")
    manager.add_blackmatrix_remote("Privacy", AD_GROUP, tag="隐私防护")

    # 4. 国内兜底 -> 走 "国内网站"
    manager.add_blackmatrix_remote("ChinaMax", DIRECT_GROUP, tag="国内直连")

    # ==========================================
    # Part C: (可选) 修改默认图标或策略
    # ==========================================
    # 如果你想把整个配置文件的头像改成你自己的
    # manager.replace_content("img-url=http.*?config.png", "img-url=https://你的图片地址.png")

    # ==========================================
    # Part D: 保存
    # ==========================================
    manager.save(OUTPUT_FILE)

if __name__ == "__main__":
    main()