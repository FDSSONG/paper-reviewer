"""
API 配置模块 - 支持中转站 API
这个文件用于统一配置 Gemini API，支持官方 API 和中转站 API
"""

import os
import google.generativeai as genai

def configure_gemini_api():
    """
    配置 Gemini API
    
    支持两种模式：
    1. 官方 API：只需设置 GEMINI_API_KEY
    2. 中转站 API：设置 GEMINI_API_KEY 和 GEMINI_BASE_URL
    
    环境变量：
    - GEMINI_API_KEY: API 密钥（必需）
    - GEMINI_BASE_URL: 中转站 API 地址（可选，如果不设置则使用官方 API）
    
    示例：
    # 使用官方 API
    export GEMINI_API_KEY="your-official-key"
    
    # 使用中转站 API
    export GEMINI_API_KEY="sk-cCWinKy0Gix1aFdSXDMGs8v6wiET53yNDqDG8GTDkoouHKMb"
    export GEMINI_BASE_URL="https://www.packyapi.com/v1"
    """
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "❌ 未设置 GEMINI_API_KEY 环境变量\n"
            "请运行: export GEMINI_API_KEY='your-api-key'"
        )
    
    base_url = os.getenv("GEMINI_BASE_URL")
    
    if base_url:
        # 使用中转站 API
        print(f"✅ 使用中转站 API: {base_url}")
        print(f"   API Key: {api_key[:10]}...")
        
        # 配置中转站
        # 注意：google-generativeai SDK 可能不直接支持修改 base_url
        # 这里提供一个解决方案
        try:
            # 方法1：尝试通过 genai.configure 配置（如果 SDK 支持）
            genai.configure(
                api_key=api_key,
                transport='rest',  # 使用 REST 传输
                client_options={
                    "api_endpoint": base_url
                }
            )
        except Exception as e:
            print(f"⚠️  警告: 标准配置失败，尝试手动配置: {e}")
            # 方法2：手动配置（如果 SDK 不支持，需要修改底层实现）
            genai.configure(api_key=api_key)
            
            # 如果 SDK 不支持自定义 base_url，你可能需要：
            # 1. Fork google-generativeai 项目并修改
            # 2. 使用其他兼容的 SDK
            # 3. 联系中转站提供商确认兼容性
            
            print("⚠️  请注意：google-generativeai SDK 可能不支持自定义 base_url")
            print("   如果遇到问题，请参考下面的替代方案")
    else:
        # 使用官方 API
        print(f"✅ 使用 Google 官方 API")
        print(f"   API Key: {api_key[:10]}...")
        genai.configure(api_key=api_key)
    
    return True


def get_api_config_info():
    """获取当前 API 配置信息"""
    return {
        "api_key": os.getenv("GEMINI_API_KEY"),
        "base_url": os.getenv("GEMINI_BASE_URL"),
        "is_relay": bool(os.getenv("GEMINI_BASE_URL")),
    }


# 在模块导入时自动配置
try:
    configure_gemini_api()
except Exception as e:
    print(f"⚠️  API 配置失败: {e}")
    print("   请确保已正确设置环境变量")
