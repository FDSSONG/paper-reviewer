#!/usr/bin/env python3
"""
元数据提取模块 - 类封装版本
从 Markdown 文本中提取标题、作者、摘要、章节结构等元数据
"""
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from literature_review.logger import get_logger

logger = get_logger("metadata_extractor")


class MetadataExtractor:
    """元数据提取器类"""
    
    def __init__(self):
        """初始化提取器"""
        pass
    
    def extract_from_content_list(self, content_list_path: str) -> Dict:
        """
        从 MinerU 的 content_list_v2.json 提取标题和作者
        
        MinerU 输出的 JSON 结构清晰：
        - 第一个 type="title" 就是论文标题
        - 标题和 Abstract 之间的 type="paragraph" 包含作者信息
        
        Args:
            content_list_path: content_list_v2.json 文件路径
        
        Returns:
            {"title": "...", "authors": ["...", ...]} 或空字典
        """
        path = Path(content_list_path)
        if not path.exists():
            return {}
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                pages = json.load(f)
        except (json.JSONDecodeError, Exception):
            return {}
        
        # 展平所有页面的元素
        elements = []
        for page in pages:
            if isinstance(page, list):
                elements.extend(page)
        
        if not elements:
            return {}
        
        # 1) 提取标题：第一个 type="title" 的元素
        title = None
        title_idx = -1
        for i, elem in enumerate(elements):
            if elem.get('type') == 'title':
                title_parts = elem.get('content', {}).get('title_content', [])
                title_text = ''.join(
                    p.get('content', '') for p in title_parts 
                    if p.get('type') == 'text'
                ).strip()
                if title_text and len(title_text) > 10:
                    title = title_text
                    title_idx = i
                    break
        
        if title is None:
            return {}
        
        # 2) 提取作者：标题之后、下一个 title（通常是 Abstract）之前的 paragraph
        author_text_parts = []
        for elem in elements[title_idx + 1:]:
            if elem.get('type') == 'title':
                # 遇到 Abstract 或章节标题，停止
                break
            if elem.get('type') == 'paragraph':
                parts = elem.get('content', {}).get('paragraph_content', [])
                text = ''.join(
                    p.get('content', '') for p in parts 
                    if p.get('type') == 'text'
                ).strip()
                if text:
                    author_text_parts.append(text)
        
        # 解析作者名（第一个 paragraph 通常是作者行）
        authors = []
        if author_text_parts:
            author_line = author_text_parts[0]
            authors = self._parse_author_line(author_line)
        
        result = {}
        if title:
            result['title'] = title
        if authors:
            result['authors'] = authors
        
        return result
    
    def _parse_author_line(self, text: str) -> List[str]:
        """
        从作者行文本中提取作者名
        处理各种格式：上标数字、符号、Fellow/IEEE 等
        """
        # 去掉常见噪音
        cleaned = text
        # 去掉上标数字和符号 (1, 2, *, †, ‡, ∗)
        cleaned = re.sub(r'[0-9]+[∗\*†‡·,]?\s*', '', cleaned)
        cleaned = re.sub(r'[∗\*†‡·]+', '', cleaned)
        # 去掉 Fellow/Member/IEEE 等
        cleaned = re.sub(r',?\s*(Fellow|Senior Member|Member|Student Member),?\s*(IEEE)?', '', cleaned)
        # 去掉邮箱
        cleaned = re.sub(r'\S+@\S+', '', cleaned)
        
        # 按 'and' 和 ',' 分割
        cleaned = cleaned.replace(' and ', ',')
        parts = [p.strip() for p in cleaned.split(',')]
        
        # 过滤有效作者名（至少 2 个字符，看起来像人名）
        authors = []
        for part in parts:
            part = part.strip()
            if not part or len(part) < 2:
                continue
            # 跳过机构名（包含 University/Laboratory/Institute 等）
            if re.search(r'(University|Laboratory|Institute|Department|School|College)', part, re.IGNORECASE):
                continue
            # 跳过注释行（Equal Contribution, Correspondence 等）
            if re.search(r'(Equal|Contribution|Correspondence|Advising)', part, re.IGNORECASE):
                continue
            authors.append(part)
        
        return authors[:20]
    
    def extract_title(self, markdown_text: str) -> Optional[str]:
        """
        从 Markdown 中提取论文标题
        通常是第一个一级标题或最开始的大标题文本
        """
        lines = markdown_text.split('\n')
        
        # 查找第一个非空行（通常是标题）
        for line in lines[:20]:  # 只检查前20行
            line = line.strip()
            if not line:
                continue
            
            # 清理标题
            title = line.lstrip('#').strip()
            
            # 如果标题太短或包含特殊字符，跳过
            if len(title) > 10 and not title.startswith('http'):
                return title
        
        return None
    
    def extract_authors(self, markdown_text: str) -> List[str]:
        """
        从 Markdown 中提取作者列表
        """
        lines = markdown_text.split('\n')
        authors = []
        
        # 策略1：在标题后的前几行寻找作者
        # MinerU 格式：标题后直接是作者行
        title_found = False
        for i, line in enumerate(lines[:30]):
            line = line.strip()
            
            # 跳过标题行
            if line.startswith('#'):
                title_found = True
                continue
            
            # 标题后的第一个非空行可能是作者
            if title_found and line and not line.startswith('#'):
                # 检查是否包含人名模式
                # 模式1: "Name1, Name2, and Name3" 或 "Name1 and Name2"
                if ' and ' in line or ',' in line:
                    # 分离作者（按逗号或 and 分割）
                    author_text = line
                    # 移除职称等后缀（例如 ", Fellow, IEEE"）
                    author_text = re.sub(r',\s*(Fellow|Member|Senior Member|Prof\.|Dr\.)[^,]*$', '', author_text)
                    
                    # 按 'and' 和 ',' 分割
                    author_text = author_text.replace(' and ', ',')
                    potential_authors = [a.strip() for a in author_text.split(',')]
                    
                    # 过滤有效的作者名（至少包含2个单词）
                    for author in potential_authors:
                        if len(author.split()) >= 2:
                            # 移除职称
                            author = re.sub(r'\s*(Fellow|Member|Senior Member|Prof\.|Dr\.)\s+.*$', '', author)
                            author = re.sub(r',.*$', '', author).strip()
                            if author and len(author.split()) >= 2:
                                authors.append(author)
                    
                    if authors:
                        return authors[:20]
        
        # 策略2：查找包含作者的行（原有逻辑作为备选）
        for i, line in enumerate(lines[:50]):
            line = line.strip()
            
            # 查找包含作者的行（通常包含多个名字，可能用逗号分隔）
            # 特征：大写字母开头的名字，可能包含逗号或 and
            if re.search(r'[A-Z][a-z]+\s+[A-Z][a-z]+', line):
                # 可能是作者行
                # 分离作者名字
                potential_authors = re.findall(
                    r'[A-Z][a-z]+(?:\s+[A-Z]\.?\s*)?[A-Z][a-z]+',
                    line
                )
                if potential_authors and len(potential_authors) <= 15:  # 合理作者数量
                    authors.extend(potential_authors)
                    if len(authors) >= 3:  # 找到足够作者后停止
                        break
        
        return authors[:20]  # 最多返回20个作者
    
    def extract_abstract(self, markdown_text: str) -> Optional[str]:
        """
        从 Markdown 中提取摘要
        """
        # 策略1：查找 Markdown 标题格式的 Abstract (# Abstract, ## Abstract, etc.)
        abstract_pattern = r'(?i)#+\s*abstract\s*\n+(.*?)(?=\n#+|\Z)'
        match = re.search(abstract_pattern, markdown_text, re.DOTALL)
        
        if match:
            abstract = match.group(1).strip()
            # 清理多余的空白
            abstract = re.sub(r'\n+', ' ', abstract)
            abstract = re.sub(r'\s+', ' ', abstract)
            return abstract
        
        # 策略2：查找非标题格式的 Abstract（例如 "Abstract—" 或 "Abstract:"）
        abstract_pattern2 = r'(?i)abstract\s*[—:]\s*(.*?)(?=\n\n[A-Z]|\n#+|\Z)'
        match = re.search(abstract_pattern2, markdown_text, re.DOTALL)
        
        if match:
            abstract = match.group(1).strip()
            # 清理多余的空白
            abstract = re.sub(r'\n+', ' ', abstract)
            abstract = re.sub(r'\s+', ' ', abstract)
            # 移除 "Index Terms" 等后续内容
            abstract = re.split(r'(?i)index\s+terms', abstract)[0].strip()
            return abstract
        
        return None
    
    def extract_sections(self, markdown_text: str) -> List[Dict[str, any]]:
        """
        从 Markdown 中提取章节结构
        
        Returns:
            [
                {"title": "Introduction", "level": 1, "content": "..."},
                {"title": "Methods", "level": 1, "content": "..."},
                ...
            ]
        """
        sections = []
        
        # 匹配章节标题（# 开头）
        lines = markdown_text.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            # 检查是否是标题行
            heading_match = re.match(r'^(#+)\s+(.+)$', line)
            
            if heading_match:
                # 保存上一个章节
                if current_section:
                    current_section['content'] = '\n'.join(section_content).strip()
                    sections.append(current_section)
                
                # 开始新章节
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()
                
                current_section = {
                    "title": title,
                    "level": level,
                    "content": ""
                }
                section_content = []
            else:
                # 添加到当前章节内容
                if current_section:
                    section_content.append(line)
        
        # 保存最后一个章节
        if current_section:
            current_section['content'] = '\n'.join(section_content).strip()
            sections.append(current_section)
        
        return sections
    
    def validate_metadata(self, metadata: Dict) -> Tuple[bool, List[str]]:
        """
        验证元数据的完整性
        
        Returns:
            (is_valid, missing_fields)
        """
        required_fields = ['title', 'authors', 'sections']
        missing_fields = []
        
        for field in required_fields:
            if field not in metadata or not metadata[field]:
                missing_fields.append(field)
        
        # 验证章节结构
        if 'sections' in metadata and metadata['sections']:
            # 检查是否有常见章节
            section_titles = [s['title'].lower() for s in metadata['sections']]
            common_sections = ['introduction', 'method', 'result', 'conclusion']
            
            has_common_section = any(
                any(common in title for common in common_sections)
                for title in section_titles
            )
            
            if not has_common_section:
                missing_fields.append('standard_sections')
        
        is_valid = len(missing_fields) == 0
        return is_valid, missing_fields
    
    def extract_metadata(self, markdown_text: str) -> Dict:
        """
        从 Markdown 提取所有元数据
        
        Returns:
            {
                "title": "论文标题",
                "authors": ["作者1", "作者2"],
                "abstract": "摘要内容",
                "sections": [...],
                "validation": {
                    "is_valid": True,
                    "missing_fields": []
                }
            }
        """
        logger.info("📋 提取元数据...")
        
        metadata = {
            "title": self.extract_title(markdown_text),
            "authors": self.extract_authors(markdown_text),
            "abstract": self.extract_abstract(markdown_text),
            "sections": self.extract_sections(markdown_text)
        }
        
        # 验证
        is_valid, missing_fields = self.validate_metadata(metadata)
        metadata['validation'] = {
            "is_valid": is_valid,
            "missing_fields": missing_fields
        }
        
        # 打印提取结果
        logger.info(f"✅ 标题: {metadata['title'][:50] if metadata['title'] else '未找到'}...")
        logger.info(f"✅ 作者数: {len(metadata['authors'])}")
        logger.info(f"✅ 摘要: {'已提取' if metadata['abstract'] else '未找到'}")
        logger.info(f"✅ 章节数: {len(metadata['sections'])}")
        
        if not is_valid:
            logger.warning(f"缺少字段: {', '.join(missing_fields)}")
        else:
            logger.info("✅ 元数据验证通过")
        
        return metadata


# 为了向后兼容，保留原有的函数接口
def extract_metadata(markdown_text: str) -> Dict:
    """向后兼容的函数接口"""
    extractor = MetadataExtractor()
    return extractor.extract_metadata(markdown_text)


# 测试代码
if __name__ == "__main__":
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("用法: python metadata_extractor.py <markdown_file>")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        
        extractor = MetadataExtractor()
        metadata = extractor.extract_metadata(markdown_text)
        
        print("\n" + "=" * 60)
        print("提取的元数据")
        print("=" * 60)
        print(json.dumps(
            {k: v for k, v in metadata.items() if k != 'sections'},
            ensure_ascii=False,
            indent=2
        ))
        
        print(f"\n章节列表:")
        for i, section in enumerate(metadata['sections'][:10], 1):
            print(f"  {i}. {'  ' * (section['level']-1)}{section['title']}")
        
        if len(metadata['sections']) > 10:
            print(f"  ... 还有 {len(metadata['sections']) - 10} 个章节")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
