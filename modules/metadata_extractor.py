#!/usr/bin/env python3
"""
元数据提取模块
使用DeepSeek从论文Markdown中提取元数据
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deepseek_api import DeepSeekAPI
from typing import Dict, List, Optional
import json


def extract_metadata(markdown_text: str, 
                     max_length: int = 20000) -> Dict:
    """
    从Markdown文本中提取论文元数据
    
    Args:
        markdown_text: 论文的Markdown文本
        max_length: 最大处理长度（字符数）
    
    Returns:
        {
            "title": "论文标题",
            "authors": ["作者1", "作者2"],
            "abstract": "摘要",
            "sections": [
                {"name": "Section名称", "level": 1, "content_preview": "前100字"},
                ...
            ],
            "keywords": ["关键词1", "关键词2"],
            "year": "发表年份"
        }
    """
    api = DeepSeekAPI()
    
    # 截断文本（保留开头部分，通常包含标题、作者、摘要）
    text_to_analyze = markdown_text[:max_length]
    
    prompt = f"""
你是一个学术论文分析专家。请从以下论文中提取元数据。

请以JSON格式返回，包含以下字段：
- title: 论文标题（字符串）
- authors: 作者列表（字符串数组）
- abstract: 摘要（字符串，提取完整摘要）
- sections: 章节列表（对象数组），每个对象包含：
  - name: 章节名称
  - level: 层级（1为一级标题，2为二级）
  - content_preview: 该章节的前100字
- keywords: 关键词列表（字符串数组，如果没有则为空数组）
- year: 发表年份（字符串，如果无法确定则为null）

注意：
1. 标题通常在论文开头，可能全大写或首字母大写
2. 作者通常在标题下方
3. 摘要通常有"Abstract"标题
4. 主要章节包括：Introduction, Related Work, Method/Methodology, Experiments/Results, Conclusion等
5. 如果某些字段无法提取，设为null或空数组

论文内容（已截取前{max_length}字符）：

{text_to_analyze}

请严格返回JSON格式。
"""
    
    print("🔍 正在提取元数据...")
    
    try:
        result = api.simple_ask_json(prompt, temperature=0.3)
        
        # 验证必需字段
        if not result.get('title'):
            print("⚠️  警告: 未提取到标题")
        if not result.get('authors'):
            print("⚠️  警告: 未提取到作者")
        if not result.get('sections'):
            print("⚠️  警告: 未提取到章节结构")
        
        print(f"  ✅ 元数据提取完成")
        print(f"     - 标题: {result.get('title', 'N/A')[:50]}...")
        print(f"     - 作者数: {len(result.get('authors', []))}")
        print(f"     - 章节数: {len(result.get('sections', []))}")
        
        return result
        
    except Exception as e:
        print(f"❌ 元数据提取失败: {e}")
        raise


def extract_detailed_sections(markdown_text: str,
                              section_names: Optional[List[str]] = None) -> Dict[str, str]:
    """
    提取特定章节的详细内容
    
    Args:
        markdown_text: 论文Markdown文本
        section_names: 要提取的章节名称列表，默认为常见章节
    
    Returns:
        {
            "Introduction": "完整内容...",
            "Method": "完整内容...",
            ...
        }
    """
    if section_names is None:
        section_names = [
            "Introduction",
            "Related Work",
            "Method", "Methodology",
            "Experiments", "Results",
            "Conclusion",
            "Discussion"
        ]
    
    api = DeepSeekAPI()
    
    # 由于文本可能很长，这里使用简单的文本分割方法
    # 实际应用中可能需要更复杂的章节识别
    
    sections_content = {}
    
    for section_name in section_names:
        prompt = f"""
请从以下论文中提取"{section_name}"章节的完整内容。

如果找到该章节，请返回JSON格式：
{{"section_name": "{section_name}", "content": "完整内容", "found": true}}

如果未找到该章节，请返回：
{{"section_name": "{section_name}", "content": "", "found": false}}

论文内容：
{markdown_text[:30000]}  # 限制长度

请严格返回JSON格式。
"""
        
        try:
            result = api.simple_ask_json(prompt, temperature=0.1)
            if result.get('found'):
                sections_content[section_name] = result.get('content', '')
        except:
            continue
    
    return sections_content


# 测试代码
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python metadata_extractor.py <markdown_file>")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    
    print("=" * 60)
    print("元数据提取测试")
    print("=" * 60)
    
    # 读取markdown
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        sys.exit(1)
    
    # 提取元数据
    try:
        metadata = extract_metadata(markdown_text)
        
        print("\n" + "=" * 60)
        print("提取结果")
        print("=" * 60)
        print(json.dumps(metadata, ensure_ascii=False, indent=2))
        
        # 保存结果
        output_file = markdown_file.replace('.md', '_metadata.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 结果已保存至: {output_file}")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
