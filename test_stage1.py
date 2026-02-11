#!/usr/bin/env python3
"""
阶段1测试脚本：PDF解析 + 元数据提取 + 格式校验
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.pdf_parser import parse_pdf_to_markdown
from modules.metadata_extractor import extract_metadata
from modules.format_validator import validate_paper_format, print_validation_report
import json


def test_stage1_pipeline(pdf_path: str, output_dir: str = "./output"):
    """
    测试阶段1的完整流程
    
    Args:
        pdf_path: PDF文件路径
        output_dir: 输出目录
    """
    print("=" * 70)
    print("🚀 阶段1测试：PDF解析 + 元数据提取 + 格式校验")
    print("=" * 70)
    print(f"PDF文件: {pdf_path}")
    print(f"输出目录: {output_dir}")
    print()
    
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Step 1: PDF解析
    print("\n" + "=" * 70)
    print("📄 步骤1: PDF → Markdown")
    print("=" * 70)
    
    try:
        parse_result = parse_pdf_to_markdown(pdf_path, output_dir)
        
        print(f"\n✅ PDF解析成功！")
        print(f"   - Markdown文件: {parse_result['markdown_path']}")
        print(f"   - 总页数: {parse_result['stats']['total_pages']}")
        print(f"   - 文本块: {parse_result['stats']['text_blocks']}")
        print(f"   - 图片: {parse_result['stats']['figure_count']}")
        print(f"   - 表格: {parse_result['stats']['table_count']}")
        
    except Exception as e:
        print(f"\n❌ PDF解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 2: 元数据提取
    print("\n" + "=" * 70)
    print("🔍 步骤2: 元数据提取")
    print("=" * 70)
    
    try:
        metadata = extract_metadata(parse_result['markdown'])
        
        metadata_path = Path(output_dir) / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 元数据提取成功！")
        print(f"   - 标题: {metadata.get('title', 'N/A')}")
        print(f"   - 作者数: {len(metadata.get('authors', []))}")
        if metadata.get('authors'):
            print(f"   - 第一作者: {metadata['authors'][0]}")
        print(f"   - 摘要长度: {len(metadata.get('abstract', ''))} 字符")
        print(f"   - 章节数: {len(metadata.get('sections', []))}")
        print(f"   - 关键词: {', '.join(metadata.get('keywords', []))}")
        print(f"   - 保存至: {metadata_path}")
        
    except Exception as e:
        print(f"\n❌ 元数据提取失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 3: 格式校验
    print("\n" + "=" * 70)
    print("📋 步骤3: 格式校验")
    print("=" * 70)
    
    try:
        validation_result = validate_paper_format(metadata)
        
        validation_path = Path(output_dir) / "validation.json"
        with open(validation_path, 'w', encoding='utf-8') as f:
            json.dump(validation_result, f, ensure_ascii=False, indent=2)
        
        print()
        print_validation_report(validation_result)
        print(f"\n   - 保存至: {validation_path}")
        
    except Exception as e:
        print(f"\n❌ 格式校验失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 汇总
    print("\n" + "=" * 70)
    print("📊 测试汇总")
    print("=" * 70)
    print(f"✅ 所有步骤完成！")
    print(f"\n生成的文件：")
    print(f"  1. {parse_result['markdown_path']}")
    print(f"  2. {metadata_path}")
    print(f"  3. {validation_path}")
    print(f"  4. {Path(output_dir) / 'content_list.json'}")
    
    if parse_result['stats']['figure_count'] > 0:
        print(f"  5. {parse_result['stats']['figure_count']} 个图片文件")
    if parse_result['stats']['table_count'] > 0:
        print(f"  6. {parse_result['stats']['table_count']} 个表格文件")
    
    print(f"\n格式校验结果: ", end="")
    if validation_result['valid']:
        print(f"✅ 通过 (评分: {validation_result['score']}/100)")
    else:
        print(f"⚠️  未通过 (评分: {validation_result['score']}/100)")
        print(f"   问题数: {len(validation_result['issues'])}")
        print(f"   警告数: {len(validation_result['warnings'])}")
    
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("=" * 70)
        print("用法: python test_stage1.py <pdf_path> [output_dir]")
        print("=" * 70)
        print("\n示例:")
        print("  python test_stage1.py paper.pdf")
        print("  python test_stage1.py paper.pdf ./my_output")
        print()
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output_stage1"
    
    # 检查PDF文件
    if not os.path.exists(pdf_path):
        print(f"❌ 错误: PDF文件不存在: {pdf_path}")
        sys.exit(1)
    
    # 运行测试
    success = test_stage1_pipeline(pdf_path, output_dir)
    
    sys.exit(0 if success else 1)
