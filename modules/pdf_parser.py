#!/usr/bin/env python3
"""
PDF解析模块
使用MinerU将PDF转换为Markdown，并提取图表
"""
import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple


def parse_pdf_to_markdown(pdf_path: str, output_dir: str) -> Dict:
    """
    使用MinerU解析PDF为Markdown
    
    Args:
        pdf_path: PDF文件路径
        output_dir: 输出目录
    
    Returns:
        {
            "markdown": "完整的markdown文本",
            "markdown_path": "markdown文件路径",
            "figures": [...],  # 图表路径列表
            "tables": [...],   # 表格路径列表
            "content_list": [...] # MinerU的原始内容列表
        }
    
    Raises:
        FileNotFoundError: PDF文件不存在
        RuntimeError: MinerU解析失败
    """
    from magic_pdf.data.data_reader_writer import FileBasedDataWriter
    from magic_pdf.pipe.UNIPipe import UNIPipe
    
    # 检查PDF文件
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 创建子目录
    figures_dir = output_path / "figures"
    tables_dir = output_path / "tables"
    tmp_dir = output_path / "tmp"
    
    figures_dir.mkdir(exist_ok=True)
    tables_dir.mkdir(exist_ok=True)
    tmp_dir.mkdir(exist_ok=True)
    
    print(f"📄 解析PDF: {pdf_path}")
    print(f"📁 输出目录: {output_dir}")
    
    # 读取PDF
    try:
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
    except Exception as e:
        raise RuntimeError(f"读取PDF失败: {e}")
    
    # 初始化MinerU
    image_writer = FileBasedDataWriter(str(tmp_dir))
    
    try:
        pipe = UNIPipe(
            pdf_bytes,
            {'_pdf_type': '', 'model_list': []},
            image_writer
        )
        
        # 执行解析
        print("  🔄 分类页面...")
        pipe.pipe_classify()
        
        print("  🔄 分析结构...")
        pipe.pipe_analyze()
        
        print("  🔄 解析内容...")
        pipe.pipe_parse()
        
        print("  🔄 生成Markdown...")
        content_list = pipe.pipe_mk_uni_format(str(tmp_dir), drop_mode='none')
        
    except Exception as e:
        raise RuntimeError(f"MinerU解析失败: {e}")
    
    # 保存content_list
    content_list_path = output_path / "content_list.json"
    with open(content_list_path, 'w', encoding='utf-8') as f:
        json.dump(content_list, f, ensure_ascii=False, indent=2)
    
    # 提取图表和markdown文本
    figure_paths = []
    table_paths = []
    markdown_parts = []
    
    page_counter = {"image": {}, "table": {}}
    
    for content in content_list:
        content_type = content.get('type', '')
        page_idx = content.get('page_idx', 0)
        
        if content_type == 'text':
            # 文本内容
            text = content.get('text', '').strip()
            if text:
                markdown_parts.append(text)
        
        elif content_type == 'image':
            # 图片
            img_path = content.get('img_path', '').strip()
            if img_path:
                page_counter["image"][page_idx] = page_counter["image"].get(page_idx, 0) + 1
                current_count = page_counter["image"][page_idx]
                
                filename = os.path.basename(img_path)
                src_path = tmp_dir / filename
                dest_path = figures_dir / f"figure_p{page_idx}_{current_count}.jpg"
                
                if src_path.exists():
                    shutil.move(str(src_path), str(dest_path))
                    figure_paths.append(str(dest_path))
                    markdown_parts.append(f"\n![Figure {page_idx}-{current_count}]({dest_path})\n")
        
        elif content_type == 'table':
            # 表格
            img_path = content.get('img_path', '').strip()
            if img_path:
                page_counter["table"][page_idx] = page_counter["table"].get(page_idx, 0) + 1
                current_count = page_counter["table"][page_idx]
                
                filename = os.path.basename(img_path)
                src_path = tmp_dir / filename
                dest_path = tables_dir / f"table_p{page_idx}_{current_count}.jpg"
                
                if src_path.exists():
                    shutil.move(str(src_path), str(dest_path))
                    table_paths.append(str(dest_path))
                    markdown_parts.append(f"\n![Table {page_idx}-{current_count}]({dest_path})\n")
    
    # 合并markdown
    markdown_text = "\n\n".join(markdown_parts)
    
    # 保存markdown文件
    markdown_path = output_path / "paper.md"
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(markdown_text)
    
    # 清理临时目录
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    
    print(f"  ✅ 解析完成！")
    print(f"     - Markdown: {markdown_path}")
    print(f"     - 图片数: {len(figure_paths)}")
    print(f"     - 表格数: {len(table_paths)}")
    
    return {
        "markdown": markdown_text,
        "markdown_path": str(markdown_path),
        "figures": figure_paths,
        "tables": table_paths,
        "content_list": content_list,
        "stats": {
            "total_pages": len(set(c.get('page_idx', 0) for c in content_list)),
            "figure_count": len(figure_paths),
            "table_count": len(table_paths),
            "text_blocks": len([c for c in content_list if c.get('type') == 'text'])
        }
    }


def get_markdown_preview(markdown_text: str, max_chars: int = 1000) -> str:
    """
    获取Markdown文本的预览
    
    Args:
        markdown_text: 完整的markdown文本
        max_chars: 最大字符数
    
    Returns:
        预览文本
    """
    if len(markdown_text) <= max_chars:
        return markdown_text
    
    return markdown_text[:max_chars] + "\n\n... (内容已截断) ..."


# 测试代码
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python pdf_parser.py <pdf_path> [output_dir]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output"
    
    print("=" * 60)
    print("PDF解析测试")
    print("=" * 60)
    
    try:
        result = parse_pdf_to_markdown(pdf_path, output_dir)
        
        print("\n" + "=" * 60)
        print("解析结果")
        print("=" * 60)
        print(f"总页数: {result['stats']['total_pages']}")
        print(f"文本块数: {result['stats']['text_blocks']}")
        print(f"图片数: {result['stats']['figure_count']}")
        print(f"表格数: {result['stats']['table_count']}")
        print(f"\nMarkdown文件: {result['markdown_path']}")
        
        print("\n内容预览:")
        print("-" * 60)
        print(get_markdown_preview(result['markdown'], 500))
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
