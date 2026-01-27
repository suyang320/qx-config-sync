import requests
import re
import os
import logging
import time
from collections import OrderedDict

# 全局日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger("QX-Core")

class QXConfigManager:
    def __init__(self):
        self.sections = OrderedDict()

        # 定义标准顺序
        standard_order = [
            "general", "dns", "policy",
            "server_local", "server_remote",
            "filter_local", "filter_remote",
            "rewrite_local", "rewrite_remote",
            "task_local", "http_backend", "mitm"
        ]

        self.sections["header"] = []
        for sec in standard_order:
            self.sections[sec] = []

        self.current_section = "header"

        # 统计数据
        self.stats = {"files_read": 0, "rules_added": 0, "rules_removed": 0, "remote_refs": 0}

        # 自动定位项目根目录
        current_file_path = os.path.abspath(__file__)
        self.project_root = os.path.dirname(os.path.dirname(current_file_path))
        logger.info(f"📂 [Init] 项目根目录锁定: {self.project_root}")

    def load_from_url(self, url):
        start_time = time.time()
        logger.info(f"📥 [Base] 开始下载底包: {url}")
        try:
            headers = {'User-Agent': 'QuantumultX-Builder/5.0'}
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            resp.encoding = 'utf-8' # 强制 UTF-8

            size_kb = len(resp.content) / 1024
            self._parse(resp.text)
            elapsed = (time.time() - start_time) * 1000
            logger.info(f"✅ [Base] 下载成功 | 耗时: {elapsed:.2f}ms | 大小: {size_kb:.2f}KB")
        except Exception as e:
            logger.error(f"❌ [Base] 下载失败: {e}")
            # 不抛出异常，允许无底包运行

    def _parse(self, content):
        lines = content.splitlines()
        section_pattern = re.compile(r'^\[(.*?)\]')
        counts = {}

        for line in lines:
            line = line.strip()
            match = section_pattern.match(line)
            if match:
                self.current_section = match.group(1)
                if self.current_section not in self.sections:
                    self.sections[self.current_section] = []
                counts[self.current_section] = counts.get(self.current_section, 0)
            else:
                self.sections[self.current_section].append(line)
                if self.current_section in counts: counts[self.current_section] += 1

        # 打印简要结构
        active_secs = [k for k, v in counts.items() if v > 0]
        logger.info(f"📊 [Parse] 解析段落: {', '.join(active_secs[:5])}...")

    def load_rules_from_file(self, relative_path):
        """读取文件，返回列表"""
        abs_path = os.path.join(self.project_root, relative_path)

        if not os.path.exists(abs_path):
            # 只有当文件不是示例文件时才警告
            if "my_custom" not in relative_path:
                logger.warning(f"⚠️ [Local] 文件未找到: {abs_path}")
            return []

        logger.info(f"📖 [Local] 读取文件: {relative_path}")
        rules = []
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                # MITM 特殊处理
                if "," in content and "\n" not in content and len(content) > 50:
                    self.stats["files_read"] += 1
                    return [content]

                for line in content.splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or line.startswith(";"): continue
                    rules.append(line)

            self.stats["files_read"] += 1
            logger.info(f"   └── ✅ 成功加载: {len(rules)} 条有效规则")
            return rules
        except Exception as e:
            logger.error(f"❌ [Local] 读取失败: {e}")
            return []

    def patch_section(self, section, keywords, strategy="blacklist"):
        if section not in self.sections: return
        original = self.sections[section]
        new_lines = []
        removed_count = 0

        if not keywords: keywords = []

        if strategy == "blacklist":
            for line in original:
                if not any(k in line for k in keywords): new_lines.append(line)
                else: removed_count += 1
        elif strategy == "whitelist":
            for line in original:
                if any(k in line for k in keywords): new_lines.append(line)
                else: removed_count += 1

        self.sections[section] = new_lines
        self.stats["rules_removed"] += removed_count
        if removed_count > 0:
            logger.info(f"✂️ [Patch] [{section}] 移除 {removed_count} 条规则")

    def set_kv(self, section, key, value):
        if section not in self.sections: self.sections[section] = []
        new_lines = []
        updated = False
        target = [f"{key}=", f"{key} ="]

        for line in self.sections[section]:
            if any(line.strip().startswith(x) for x in target):
                # 【修改】针对 hostname 特殊处理：追加而不是覆盖
                if key == "hostname":
                    # 提取原有值
                    original_val = line.split("=", 1)[1].strip()
                    # 避免重复追加
                    if value not in original_val:
                        new_val = f"{original_val}, {value}"
                        new_lines.append(f"{key}={new_val}")
                        logger.info(f"🔗 [MITM] 追加 hostname: ... + {value}")
                    else:
                        new_lines.append(line)
                else:
                    # 其他 KV 保持覆盖逻辑
                    new_lines.append(f"{key}={value}")
                    logger.info(f"⚙️ [{section}] 更新: {key} = ...")
                updated = True
            else:
                new_lines.append(line)
        if not updated:
            new_lines.append(f"{key}={value}")
            logger.info(f"⚙️ [{section}] 新增: {key} = ...")
        self.sections[section] = new_lines

    def add_list_item(self, section, item, position="end"):
        if section not in self.sections: self.sections[section] = []
        if item in self.sections[section]: return
        if position == "start": self.sections[section].insert(0, item)
        else: self.sections[section].append(item)
        self.stats["rules_added"] += 1

    def add_remote_rule(self, url, tag, policy):
        line = f"{url}, tag={tag}, force-policy={policy}, update-interval=86400, opt-parser=true, enabled=true"
        # 【修改】改为插入到头部 (start)，确保优先级高于底包
        self.add_list_item("filter_remote", line, position="start")
        self.stats["remote_refs"] += 1
        logger.info(f"☁️ [Remote] 引用: {tag} -> {policy} (Top Priority)")

    def save(self, filename):
        logger.info(f"💾 [Save] 正在写入文件...")
        try:
            total_lines = 0
            with open(filename, 'w', encoding='utf-8') as f:
                for section, lines in self.sections.items():
                    if lines or section in ["general", "dns", "policy", "filter_local"]:
                        if section != "header":
                            f.write(f"\n[{section}]\n")
                            total_lines += 1
                        for line in lines:
                            if line:
                                f.write(f"{line}\n")
                                total_lines += 1

            size_kb = os.path.getsize(filename) / 1024
            logger.info(f"✅ [Save] 生成成功: {filename}")
            logger.info(f"📊 [Stats] 大小: {size_kb:.2f}KB | 总行数: {total_lines}")
            logger.info(f"📈 [Summary] 读文件: {self.stats['files_read']} | 注入: {self.stats['rules_added']} | 删除: {self.stats['rules_removed']} | 远程: {self.stats['remote_refs']}")
        except Exception as e:
            logger.error(f"❌ [Save] 保存失败: {e}")