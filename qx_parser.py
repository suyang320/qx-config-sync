# qx_parser.py
import requests
import re
from collections import OrderedDict

class QXConfigManager:
    def __init__(self):
        # 使用 OrderedDict 保证写入文件时顺序不乱 (Header -> General -> DNS -> Policy...)
        self.sections = OrderedDict()
        self.current_section = "header"
        self.sections["header"] = []

    def load_from_url(self, url):
        """从 URL 下载原始配置"""
        print(f"📥 正在下载基准配置: {url} ...")
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            self._parse(resp.text)
            print("✅ 下载并解析成功")
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            raise e

    def _parse(self, content):
        """解析文本为字典结构"""
        lines = content.splitlines()
        section_pattern = re.compile(r'^\[(.*?)\]') # 匹配 [section]

        for line in lines:
            line = line.strip()
            match = section_pattern.match(line)
            if match:
                self.current_section = match.group(1)
                if self.current_section not in self.sections:
                    self.sections[self.current_section] = []
            else:
                self.sections[self.current_section].append(line)

    def add_rule(self, section, rule, position="end"):
        """
        添加规则
        position="start": 插在最前面 (用于内网直连等高优先级规则)
        position="end": 插在最后面
        """
        if section not in self.sections:
            self.sections[section] = []

        # 简单去重
        if rule in self.sections[section]:
            return

        if position == "start":
            self.sections[section].insert(0, rule)
        else:
            self.sections[section].append(rule)
        print(f"➕ [{section}] 添加规则: {rule}")

    def remove_rule_by_keyword(self, section, keyword):
        """移除包含关键词的规则"""
        if section in self.sections:
            original_count = len(self.sections[section])
            self.sections[section] = [line for line in self.sections[section] if keyword not in line]
            removed = original_count - len(self.sections[section])
            if removed > 0:
                print(f"✂️ [{section}] 移除了 {removed} 条包含 '{keyword}' 的规则")

    def add_blackmatrix_remote(self, name, policy, tag=None):
        """
        便捷添加 Blackmatrix7 的远程引用
        """
        if not tag:
            tag = name
        # 构造 URLn
        url = f"https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/{name}/{name}.list"
        # 构造配置行
        line = f"{url}, tag={tag}, force-policy={policy}, update-interval=86400, opt-parser=true, enabled=true"
        self.add_rule("filter_remote", line, position="end")

    def save(self, filename):
        """生成最终文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            for section, lines in self.sections.items():
                if section != "header":
                    f.write(f"\n[{section}]\n")
                for line in lines:
                    if line:
                        f.write(f"{line}\n")
        print(f"💾 配置文件已生成: {filename}")