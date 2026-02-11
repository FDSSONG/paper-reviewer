"""
验证 config_api 集成是否成功
"""
import os
import sys

def test_config_api_import():
    """测试 config_api 是否能正确导入"""
    print("=" * 60)
    print("📦 测试 1: 验证 config_api 导入")
    print("=" * 60)
    
    try:
        import config_api
        print("✅ config_api 模块导入成功")
        
        # 检查配置信息
        config_info = config_api.get_api_config_info()
        print(f"\n当前配置:")
        print(f"  - API Key: {config_info['api_key'][:10] if config_info['api_key'] else 'None'}...")
        print(f"  - Base URL: {config_info['base_url'] or '(使用官方 API)'}")
        print(f"  - 是否使用中转站: {'是' if config_info['is_relay'] else '否'}")
        
        return True
    except Exception as e:
        print(f"❌ config_api 导入失败: {e}")
        return False


def test_pipeline_imports():
    """测试 pipeline 文件是否能正确导入"""
    print("\n" + "=" * 60)
    print("📦 测试 2: 验证 pipeline 模块导入")
    print("=" * 60)
    
    pipeline_modules = [
        "pipeline.extract_essentials",
        "pipeline.extract_sections",
        "pipeline.extract_references",
        "pipeline.extract_affiliation",
        "pipeline.extract_category",
        "pipeline.extract_section_details",
        "pipeline.crop_gemini",
        "pipeline.crop_doublecheck",
        "pipeline.enrich_desc",
        "pipeline.reformat_tables",
        "pipeline.write_script",
    ]
    
    success_count = 0
    fail_count = 0
    
    for module_name in pipeline_modules:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name}")
            success_count += 1
        except Exception as e:
            print(f"  ❌ {module_name}: {e}")
            fail_count += 1
    
    print(f"\n总计: {success_count} 成功, {fail_count} 失败")
    return fail_count == 0


def test_genai_configured():
    """测试 genai 是否已配置"""
    print("\n" + "=" * 60)
    print("📦 测试 3: 验证 Gemini API 配置")
    print("=" * 60)
    
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            print(f"✅ GEMINI_API_KEY 已设置: {api_key[:10]}...")
        else:
            print("⚠️  GEMINI_API_KEY 未设置")
            print("   请运行: export GEMINI_API_KEY='your-api-key'")
        
        base_url = os.getenv("GEMINI_BASE_URL")
        if base_url:
            print(f"✅ GEMINI_BASE_URL 已设置: {base_url}")
            print("   将尝试使用中转站 API")
        else:
            print("ℹ️  GEMINI_BASE_URL 未设置，使用官方 API")
        
        return bool(api_key)
    except Exception as e:
        print(f"❌ genai 配置检查失败: {e}")
        return False


def main():
    """主测试函数"""
    print("\n🔍 Paper Reviewer - config_api 集成验证\n")
    
    # 切换到项目目录
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    sys.path.insert(0, project_dir)
    
    # 运行测试
    test1 = test_config_api_import()
    test2 = test_pipeline_imports()
    test3 = test_genai_configured()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    if test1 and test2 and test3:
        print("✅ 所有测试通过！config_api 已成功集成")
        print("\n下一步:")
        print("  1. 设置环境变量: export GEMINI_API_KEY='your-key'")
        print("  2. (可选) 设置中转站: export GEMINI_BASE_URL='https://...'")
        print("  3. 运行项目: python collect.py --arxiv-id 'xxx' --stop-at-no-html")
    elif test1 and test2:
        print("⚠️  config_api 已集成，但需要设置 API 密钥")
        print("\n请运行:")
        print("  export GEMINI_API_KEY='your-api-key'")
    else:
        print("❌ 存在问题，请检查错误信息")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
