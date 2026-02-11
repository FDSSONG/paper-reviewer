#!/usr/bin/env python3
"""
DeepSeek API 适配器
用于火山引擎ARK平台的DeepSeek v3模型调用
"""
import os
import requests
import json
from typing import Dict, List, Optional, Union


class DeepSeekAPI:
    """DeepSeek API封装类"""
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 model: Optional[str] = None):
        """
        初始化DeepSeek API
        
        Args:
            api_key: API密钥，默认从环境变量读取
            base_url: API基础URL，默认从环境变量读取
            model: 模型名称，默认从环境变量读取
        """
        self.api_key = api_key or os.getenv(
            "DEEPSEEK_API_KEY", 
            "2257021f-e909-4938-9460-45d66b42c5cf"
        )
        self.base_url = base_url or os.getenv(
            "DEEPSEEK_BASE_URL",
            "https://ark.cn-beijing.volces.com/api/v3/"
        )
        self.model = model or os.getenv(
            "DEEPSEEK_MODEL",
            "deepseek-v3-250324"
        )
        
        # 确保base_url以/结尾
        if not self.base_url.endswith('/'):
            self.base_url += '/'
    
    def chat(self,
             messages: List[Dict[str, str]],
             model: Optional[str] = None,
             temperature: float = 1.0,
             max_tokens: Optional[int] = None,
             response_format: Optional[Dict] = None,
             timeout: int = 60) -> str:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表，格式：[{"role": "user", "content": "..."}]
            model: 模型名称，默认使用初始化时的模型
            temperature: 温度参数
            max_tokens: 最大token数
            response_format: 响应格式，如 {"type": "json_object"}
            timeout: 超时时间（秒）
        
        Returns:
            模型的回复内容
        
        Raises:
            requests.RequestException: 请求失败
            ValueError: 响应格式错误
        """
        url = f"{self.base_url}chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            data["max_tokens"] = max_tokens
        
        if response_format:
            data["response_format"] = response_format
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=timeout
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"API请求失败: {e}")
        except (KeyError, IndexError) as e:
            raise ValueError(f"响应格式错误: {e}")
    
    def chat_json(self,
                  messages: List[Dict[str, str]],
                  **kwargs) -> Dict:
        """
        发送聊天请求，返回JSON格式
        
        Args:
            messages: 消息列表
            **kwargs: 其他参数传递给chat()
        
        Returns:
            解析后的JSON对象
        """
        # 强制使用JSON模式
        kwargs['response_format'] = {"type": "json_object"}
        
        response = self.chat(messages, **kwargs)
        
        # 尝试直接解析
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # 如果失败，尝试提取markdown代码块中的JSON
        import re
        
        # 匹配 ```json ... ``` 或 ``` ... ```
        patterns = [
            r'```json\s*\n(.*?)\n```',
            r'```\s*\n(.*?)\n```',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    continue
        
        # 都失败了，抛出错误
        raise ValueError(f"返回内容不是有效的JSON，且无法从代码块中提取\n内容: {response}")
    
    def simple_ask(self, question: str, **kwargs) -> str:
        """
        简单问答接口
        
        Args:
            question: 问题
            **kwargs: 其他参数传递给chat()
        
        Returns:
            模型回复
        """
        messages = [{"role": "user", "content": question}]
        return self.chat(messages, **kwargs)
    
    def simple_ask_json(self, question: str, **kwargs) -> Dict:
        """
        简单问答接口（JSON返回）
        
        Args:
            question: 问题
            **kwargs: 其他参数传递给chat_json()
        
        Returns:
            解析后的JSON对象
        """
        messages = [{"role": "user", "content": question}]
        return self.chat_json(messages, **kwargs)


# 全局单例
_api_instance = None

def get_api() -> DeepSeekAPI:
    """获取全局API实例"""
    global _api_instance
    if _api_instance is None:
        _api_instance = DeepSeekAPI()
    return _api_instance


# 便捷函数
def chat(messages: List[Dict[str, str]], **kwargs) -> str:
    """全局聊天函数"""
    return get_api().chat(messages, **kwargs)


def chat_json(messages: List[Dict[str, str]], **kwargs) -> Dict:
    """全局聊天函数（JSON返回）"""
    return get_api().chat_json(messages, **kwargs)


def ask(question: str, **kwargs) -> str:
    """全局问答函数"""
    return get_api().simple_ask(question, **kwargs)


def ask_json(question: str, **kwargs) -> Dict:
    """全局问答函数（JSON返回）"""
    return get_api().simple_ask_json(question, **kwargs)


# 测试代码
if __name__ == "__main__":
    print("=" * 60)
    print("DeepSeek API 测试")
    print("=" * 60)
    
    api = DeepSeekAPI()
    
    # 测试1：简单对话
    print("\n测试1: 简单对话")
    print("-" * 60)
    response = api.simple_ask("你好！请用一句话介绍你自己。")
    print(f"回复: {response}")
    
    # 测试2：JSON模式
    print("\n测试2: JSON模式")
    print("-" * 60)
    response = api.simple_ask_json(
        '请以JSON格式返回：{"name": "DeepSeek", "version": "v3", "capability": "对话和编程"}'
    )
    print(f"回复 (JSON): {json.dumps(response, ensure_ascii=False, indent=2)}")
    
    # 测试3：多轮对话
    print("\n测试3: 多轮对话")
    print("-" * 60)
    messages = [
        {"role": "user", "content": "我想学Python"},
        {"role": "assistant", "content": "很好！Python是一门很适合初学者的编程语言。"},
        {"role": "user", "content": "请给我推荐3本入门书籍"}
    ]
    response = api.chat(messages)
    print(f"回复: {response}")
    
    print("\n" + "=" * 60)
    print("✅ 所有测试完成！")
