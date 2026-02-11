#!/usr/bin/env python3
"""
测试中转站 API 是否支持 OpenAI 格式
"""
import requests
import os

def test_openai_format():
    """测试中转站是否支持 OpenAI API 格式"""
    
    api_key = os.getenv("GEMINI_API_KEY", "sk-cCWinKy0Gix1aFdSXDMGs8v6wiET53yNDqDG8GTDkoouHKMb")
    base_url = os.getenv("GEMINI_BASE_URL", "https://www.packyapi.com/v1")
    
    print("=" * 60)
    print("测试中转站 API 兼容性")
    print("=" * 60)
    print(f"Base URL: {base_url}")
    print(f"API Key: {api_key[:15]}...")
    print()
    
    # 测试1: OpenAI chat completions 格式
    print("[测试1] OpenAI Chat Completions 格式")
    print("-" * 60)
    
    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemini-3-pro-preview",
        "messages": [
            {"role": "user", "content": "Hello! Please respond with 'API test successful'"}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 成功！支持 OpenAI 格式")
            print(f"响应: {response.json()}")
            return True
        else:
            print(f"❌ 失败")
            print(f"响应: {response.text[:500]}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def test_alternative_endpoints():
    """测试其他可能的端点"""
    
    api_key = os.getenv("GEMINI_API_KEY", "sk-cCWinKy0Gix1aFdSXDMGs8v6wiET53yNDqDG8GTDkoouHKMb")
    base_url = os.getenv("GEMINI_BASE_URL", "https://www.packyapi.com/v1")
    
    print()
    print("[测试2] 其他可能的端点")
    print("-" * 60)
    
    # 尝试不同的端点
    endpoints = [
        "/v1/chat/completions",
        "/v1beta/chat/completions",
        "/completions",
        "/generate",
    ]
    
    for endpoint in endpoints:
        url = base_url.rstrip('/') + endpoint
        print(f"\n尝试: {url}")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gemini-3-pro-preview",
            "messages": [{"role": "user", "content": "test"}]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                print(f"  ✅ 成功！状态码: {response.status_code}")
                return True
            else:
                print(f"  ❌ 状态码: {response.status_code}")
        except Exception as e:
            print(f"  ❌ 错误: {str(e)[:100]}")
    
    return False

def main():
    """主函数"""
    
    print()
    result1 = test_openai_format()
    result2 = test_alternative_endpoints()
    
    print()
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    
    if result1 or result2:
        print("✅ 中转站支持某种 API 格式！")
        print()
        print("下一步：")
        print("  1. 记录可用的端点和格式")
        print("  2. 我可以帮你修改代码适配这个格式")
    else:
        print("❌ 所有测试都失败了")
        print()
        print("建议：")
        print("  1. 查看中转站文档，确认正确的 API 格式")
        print("  2. 联系中转站客服")
        print("  3. 或使用 Google 官方 API key")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
