#!/usr/bin/env python3
"""
格式校验模块
验证论文格式的完整性和规范性
"""
from typing import Dict, List
import json


def validate_paper_format(metadata: Dict) -> Dict:
    """
    验证论文格式完整性
    
    Args:
        metadata: 从metadata_extractor提取的元数据
    
    Returns:
        {
            "valid": bool,  # 是否通过校验
            "score": float,  # 完整性评分 (0-100)
            "issues": [...],  # 严重问题列表
            "warnings": [...],  # 警告列表
            "suggestions": [...]  # 改进建议
        }
    """
    issues = []
    warnings = []
    suggestions = []
    score = 100.0
    
    # 1. 检查标题
    if not metadata.get('title'):
        issues.append("❌ 缺少论文标题")
        score -= 20
    elif len(metadata.get('title', '')) < 10:
        warnings.append("⚠️  标题过短（少于10字符）")
        score -= 5
    
    # 2. 检查作者
    authors = metadata.get('authors', [])
    if not authors:
        issues.append("❌ 缺少作者信息")
        score -= 15
    elif len(authors) > 20:
        warnings.append(f"⚠️  作者数量异常多（{len(authors)}人）")
        score -= 2
    
    # 3. 检查摘要
    abstract = metadata.get('abstract', '')
    if not abstract:
        issues.append("❌ 缺少摘要")
        score -= 20
    elif len(abstract) < 100:
        warnings.append("⚠️  摘要过短（少于100字符）")
        score -= 5
    elif len(abstract) > 3000:
        warnings.append("⚠️  摘要过长（超过3000字符）")
        score -= 3
    
    # 4. 检查章节结构
    sections = metadata.get('sections', [])
    if not sections:
        issues.append("❌ 未识别到章节结构")
        score -= 25
    else:
        # 提取章节名称（转小写）
        section_names = [s.get('name', '').lower() for s in sections]
        
        # 必需章节
        required_sections = {
            'introduction': ['introduction', 'intro'],
            'method': ['method', 'methodology', 'approach'],
            'results': ['results', 'experiments', 'experimental results', 'evaluation'],
            'conclusion': ['conclusion', 'conclusions', 'summary']
        }
        
        missing_sections = []
        for section_type, keywords in required_sections.items():
            found = any(
                any(keyword in name for keyword in keywords)
                for name in section_names
            )
            if not found:
                missing_sections.append(section_type.capitalize())
        
        if missing_sections:
            warnings.append(f"⚠️  缺少推荐章节: {', '.join(missing_sections)}")
            score -= len(missing_sections) * 3
        
        # 相关工作章节（可选但推荐）
        has_related_work = any(
            'related' in name or 'background' in name or 'literature' in name
            for name in section_names
        )
        if not has_related_work:
            suggestions.append("💡 建议添加 Related Work 或 Background 章节")
    
    # 5. 检查关键词
    keywords = metadata.get('keywords', [])
    if not keywords:
        warnings.append("⚠️  缺少关键词")
        score -= 3
    elif len(keywords) < 3:
        suggestions.append("💡 建议添加更多关键词（至少3-5个）")
    
    # 6. 检查发表年份
    if not metadata.get('year'):
        suggestions.append("💡 未识别到发表年份")
    
    # 确保分数不低于0
    score = max(0, score)
    
    # 判断是否通过
    valid = len(issues) == 0 and score >= 60
    
    return {
        "valid": valid,
        "score": round(score, 1),
        "issues": issues,
        "warnings": warnings,
        "suggestions": suggestions,
        "details": {
            "has_title": bool(metadata.get('title')),
            "has_authors": bool(metadata.get('authors')),
            "has_abstract": bool(metadata.get('abstract')),
            "section_count": len(sections),
            "keyword_count": len(keywords),
            "has_year": bool(metadata.get('year'))
        }
    }


def print_validation_report(validation_result: Dict):
    """
    打印格式化的校验报告
    
    Args:
        validation_result: validate_paper_format的返回结果
    """
    print("=" * 60)
    print("📋 论文格式校验报告")
    print("=" * 60)
    
    # 总体状态
    status = "✅ 通过" if validation_result['valid'] else "❌ 未通过"
    score = validation_result['score']
    print(f"\n状态: {status}")
    print(f"完整性评分: {score}/100")
    
    # 详细信息
    details = validation_result['details']
    print(f"\n详细信息:")
    print(f"  - 标题: {'✓' if details['has_title'] else '✗'}")
    print(f"  - 作者: {'✓' if details['has_authors'] else '✗'}")
    print(f"  - 摘要: {'✓' if details['has_abstract'] else '✗'}")
    print(f"  - 章节数: {details['section_count']}")
    print(f"  - 关键词数: {details['keyword_count']}")
    print(f"  - 年份: {'✓' if details['has_year'] else '✗'}")
    
    # 问题
    issues = validation_result['issues']
    if issues:
        print(f"\n严重问题 ({len(issues)}):")
        for issue in issues:
            print(f"  {issue}")
    
    # 警告
    warnings = validation_result['warnings']
    if warnings:
        print(f"\n警告 ({len(warnings)}):")
        for warning in warnings:
            print(f"  {warning}")
    
    # 建议
    suggestions = validation_result['suggestions']
    if suggestions:
        print(f"\n改进建议 ({len(suggestions)}):")
        for suggestion in suggestions:
            print(f"  {suggestion}")
    
    print("=" * 60)


# 测试代码
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python format_validator.py <metadata_json_file>")
        sys.exit(1)
    
    metadata_file = sys.argv[1]
    
    # 读取元数据
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    except Exception as e:
        print(f"❌ 读取元数据文件失败: {e}")
        sys.exit(1)
    
    # 执行校验
    validation_result = validate_paper_format(metadata)
    
    # 打印报告
    print_validation_report(validation_result)
    
    # 保存结果
    output_file = metadata_file.replace('.json', '_validation.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(validation_result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 校验结果已保存至: {output_file}")
