# src/qx_core.py

import requests
import re
from collections import OrderedDict

class QXConfigManager:
    def __init__(self):
        # 使用 OrderedDict 保证写入文件时，配置段落的顺序（General -> DNS -> Policy...）不乱
        self.sections = OrderedDict()
        # 记录当前解析到的段落名
        self.current_section = "header"
        # 初始化头部段落
        self.sections["header"] = []

    def load_from_url(self, url):
        """
        从 URL 下载原始配置内容
        """
        print(f"📥 [Core] 正在下载底包: {url} ...")
        try:
            # 设置超时时间，防止网络卡死
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            # 开始解析文本
            self._parse(resp.text)
            print("✅ [Core] 下载并解析成功")
        except Exception as e:
            print(f"❌ [Core] 下载失败: {e}")
            raise e

    def _parse(self, content):
        """
        核心解析逻辑：利用正则将文本拆解为 Key-Value 结构的字典
        """
        lines = content.splitlines()
        # 正则匹配 [section_name]，例如 [general], [filter_local]
        section_pattern = re.compile(r'^\[(.*?)\]')

        for line in lines:
            line = line.strip()
            match = section_pattern.match(line)

            if match:
                # 如果匹配到 [xxx]，切换当前上下文到该段落
                self.current_section = match.group(1)
                if self.current_section not in self.sections:
                    self.sections[self.current_section] = []
            else:
                # 否则，将该行内容追加到当前段落的列表中
                self.sections[self.current_section].append(line)

    def patch_section(self, section, keywords, strategy="blacklist"):
        """
        【清洗器】对指定段落进行黑/白名单过滤
        :param section: 段落名 (如 rewrite_remote)
        :param keywords: 关键词列表
        :param strategy: 'blacklist' (删除含关键词的行) / 'whitelist' (只留含关键词的行)
        """
        if section not in self.sections:
            print(f"⚠️ [Core] 警告: 底包中不存在 [{section}] 段落，跳过清洗")
            return

        original_lines = self.sections[section]
        new_lines = []
        count_before = len(original_lines)

        if strategy == "blacklist":
            # 黑名单模式：只要行内包含任意一个关键词，就过滤掉
            for line in original_lines:
                # 逻辑：如果这一行 不包含 关键词列表中的 任何一个
                if not any(k in line for k in keywords):
                    new_lines.append(line)

        elif strategy == "whitelist":
            # 白名单模式：只有行内包含关键词，才保留
            for line in original_lines:
                if any(k in line for k in keywords):
                    new_lines.append(line)

        # 更新段落内容
        self.sections[section] = new_lines
        count_after = len(new_lines)
        print(f"✂️ [Core] [{section}] 清洗完成 ({strategy}): 移除 {count_before - count_after} 条，剩余 {count_after} 条")

    def set_general(self, key, value):
        """
        修改或添加 [general] 下的配置 (如 GeoIP 源)
        """
        if "general" not in self.sections:
            self.sections["general"] = []

        new_lines = []
        updated = False

        # 遍历查找是否存在该 Key
        for line in self.sections["general"]:
            # 兼容 key=value 和 key = value 两种写法
            if line.strip().startswith(f"{key}=") or line.strip().startswith(f"{key} ="):
                new_lines.append(f"{key}={value}")
                updated = True
            else:
                new_lines.append(line)

        # 如果没找到，追加到末尾
        if not updated:
            new_lines.append(f"{key}={value}")

        self.sections["general"] = new_lines

    def add_list_item(self, section, item, position="end"):
        """
        向列表型段落 (如 filter_local) 添加规则
        :param position: 'start' 插到最前 (高优先级), 'end' 插到最后 (兜底)
        """
        if section not in self.sections:
            self.sections[section] = []

        # 简单去重：如果完全一样就不加了
        if item in self.sections[section]:
            return

        if position == "start":
            self.sections[section].insert(0, item)
        else:
            self.sections[section].append(item)

    def add_remote_rule(self, url, tag, policy, enabled=True):
        """
        生成 QX 标准的远程引用字符串
        """
        # opt-parser=true 是关键，让 QX 能够解析非标准 list
        line = f"{url}, tag={tag}, force-policy={policy}, update-interval=86400, opt-parser=true, enabled={str(enabled).lower()}"
        self.add_list_item("filter_remote", line, position="end")

    def save(self, filename):
        """
        将内存中的配置写入文件
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for section, lines in self.sections.items():
                    # 头部段落不需要写 [header] 标签
                    if section != "header":
                        f.write(f"\n[{section}]\n")
                    for line in lines:
                        # 忽略空行，或者你可以选择保留
                        if line:
                            f.write(f"{line}\n")
            print(f"💾 [Core] 配置文件已生成: {filename}")
        except Exception as e:
            print(f"❌ [Core] 保存文件失败: {e}")