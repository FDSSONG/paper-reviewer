#!/usr/bin/env python3
"""
测试火山引擎ARK平台 - 尝试不同的model参数
"""
import requests
import json

API_KEY = "2257021f-e909-4938-9460-45d66b42c5cf"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/"

def test_model(model_name):
    """测试指定的模型名称"""
    url = f"{BASE_URL}chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": "你好"}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {model_name}: 成功！")
            print(f"   回复: {result['choices'][0]['message']['content']}")
            return True
        elif response.status_code == 404:
            error_msg = response.json().get('error', {}).get('message', '')
            print(f"❌ {model_name}: 不存在")
            if "does not exist" in error_msg:
                print(f"   提示: 模型不存在或无权限")
        else:
            print(f"⚠️  {model_name}: HTTP {response.status_code}")
            print(f"   {response.text[:200]}")
        return False
    except Exception as e:
        print(f"❌ {model_name}: 错误 - {str(e)[:100]}")
        return False


def main():
    """测试不同的模型配置"""
    print("=" * 60)
    print("火山引擎ARK平台 - 模型测试")
    print("=" * 60)
    print()
    
    # 常见的模型名称和endpoint格式
    test_models = [
        # DeepSeek相关
        "deepseek-chat",
        "deepseek-v3",
        "deepseek",
        
        # 火山引擎endpoint格式（需要替换）
        # "ep-xxxxx-xxxxx",  # 你需要从控制台获取真实的endpoint ID
        
        # 其他可能的格式
        "doubao-pro-32k",
        "doubao-lite-32k"
    ]
    
    print("📝 说明：")
    print("火山引擎ARK平台使用 endpoint ID，格式通常是 'ep-xxxxx-xxxxx'")
    print("请从控制台获取你的DeepSeek endpoint ID")
    print()
    print("测试开始...")
    print("-" * 60)
    
    success_models = []
    for model in test_models:
        if test_model(model):
            success_models.append(model)
        print()
    
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    
    if success_models:
        print(f"\n✅ 可用的模型：")
        for model in success_models:
            print(f"  - {model}")
    else:
        print("\n❌ 没有找到可用的模型")
        print("\n💡 下一步操作：")
        print("1. 登录火山引擎控制台: https://console.volcengine.com/ark")
        print("2. 进入「推理接入点」页面")
        print("3. 找到你的 DeepSeek 接入点")
        print("4. 复制 endpoint ID（格式：ep-xxxxx-xxxxx）")
        print("5. 告诉我这个 endpoint ID，我会更新代码")


if __name__ == "__main__":
    main()
