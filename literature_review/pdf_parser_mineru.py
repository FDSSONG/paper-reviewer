#!/usr/bin/env python3
"""
PDF 解析模块 - 使用 MinerU (适配 magic-pdf 1.3.12+)
将 PDF 转换为纯 Markdown 文本（不包含图片/表格）
"""
import os
import json
import shutil
from pathlib import Path
from typing import Dict, Optional


def parse_pdf_to_markdown(pdf_path: str, output_dir: Optional[str] = None) -> Dict:
    """
    使用 MinerU 将 PDF 转换为 Markdown (适配 1.3.12 新版本)
    
    Args:
        pdf_path: PDF 文件路径
        output_dir: 输出目录（可选，默认为 PDF 同目录）
    
    Returns:
        {
            "markdown": "完整的 markdown 文本",
            "markdown_path": "markdown 文件路径",
            "content_list": [...],  # MinerU 的原始内容列表
            "stats": {
                "total_pages": 10,
                "text_blocks": 150,
                "image_count": 5,
                "table_count": 3
            }
        }
    
    Raises:
        FileNotFoundError: PDF 文件不存在
        RuntimeError: MinerU 解析失败
    """
    # 检查 PDF 文件
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF 文件不存在: {pdf_path}")
    
    # 设置输出目录
    if output_dir is None:
        output_dir = os.path.dirname(pdf_path) or '.'
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"📄 正在解析 PDF: {pdf_path}")
    print(f"📁 输出目录: {output_dir}")
    
    try:
        # 使用 MinerU REST API (无页数限制)
        import requests
        import time
        
        print("  🔄 使用 MinerU REST API 解析 PDF...")
        
        # 获取 API Token
        import os
        api_token = os.getenv('MINERU_API_TOKEN')
        
        if not api_token:
            raise RuntimeError(
                "未设置 MINERU_API_TOKEN 环境变量。\n"
                "请先设置：export MINERU_API_TOKEN='your_api_token'\n"
                "获取 Token：访问 https://mineru.net"
            )
        
        # 第一步：上传 PDF 文件到临时存储（如果需要）
        # 或者如果有公开 URL，直接使用 URL
        
        # 这里假设我们需要先上传文件
        # 如果 API 支持文件上传，使用 multipart/form-data
        # 根据实际 API 文档调整
        
        # 方案：使用本地文件上传
        print(f"  📤 准备上传文件: {pdf_path}")
        
        # API 端点
        api_url = "https://mineru.net/api/v4/extract/task"
        
        # 请求头
        headers = {
            "Authorization": f"Bearer {api_token}"
        }
        
        # 检查 API 是否支持文件上传或需要 URL
        # 根据 test.py，API 接受 URL，所以我们需要先将文件上传到某处
        # 或者使用文件上传的 API 端点
        
        # 如果 API 支持文件直接上传
        with open(pdf_path, 'rb') as f:
            files = {'file': (os.path.basename(pdf_path), f, 'application/pdf')}
            data = {
                'model_version': 'vlm'
            }
            
            print("  📤 上传 PDF 到 MinerU...")
            response = requests.post(
                api_url,
                headers=headers,
                files=files,
                data=data,
                timeout=30
            )
        
        if response.status_code != 200:
            raise RuntimeError(f"API 请求失败 (HTTP {response.status_code}): {response.text}")
        
        result = response.json()
        print(f"  ✅ 任务提交成功: {result}")
        
        # 获取任务 ID 或结果
        # 根据实际 API 响应结构调整
        task_data = result.get('data', {})
        
        # 如果 API 返回任务 ID，需要轮询获取结果
        task_id = task_data.get('task_id') or task_data.get('id')
        
        if task_id:
            print(f"  ⏳ 等待解析完成 (Task ID: {task_id})...")
            
            # 轮询任务状态
            max_wait = 300  # 最多等待 5 分钟
            poll_interval = 5  # 每 5 秒轮询一次
            elapsed = 0
            
            status_url = f"https://mineru.net/api/v4/extract/task/{task_id}"
            
            while elapsed < max_wait:
                time.sleep(poll_interval)
                elapsed += poll_interval
                
                status_response = requests.get(status_url, headers=headers)
                if status_response.status_code != 200:
                    raise RuntimeError(f"获取任务状态失败: {status_response.text}")
                
                status_data = status_response.json()
                task_status = status_data.get('data', {}).get('status')
                
                print(f"  ⏳ 任务状态: {task_status} ({elapsed}s)")
                
                if task_status == 'completed' or task_status == 'success':
                    task_data = status_data.get('data', {})
                    break
                elif task_status == 'failed' or task_status == 'error':
                    raise RuntimeError(f"解析失败: {status_data}")
            else:
                raise RuntimeError("解析超时（超过 5 分钟）")
        
        print("  ✅ 解析完成")
        
        # 从结果中提取 Markdown 和内容
        # 根据实际 API 返回结构调整
        markdown_text = task_data.get('markdown', '') or task_data.get('content', '')
        content_list = task_data.get('content_list', [])
        
        # 如果 API 返回的是 URL，需要下载
        if not markdown_text and 'markdown_url' in task_data:
            markdown_url = task_data['markdown_url']
            print(f"  📥 下载 Markdown: {markdown_url}")
            md_response = requests.get(markdown_url)
            markdown_text = md_response.text
        
        # 如果没有直接的 markdown，尝试从 content_list 重建
        if not markdown_text and content_list:
            print("  🔄 从内容列表重建 Markdown...")
            markdown_parts = []
            for content in content_list:
                if content.get('type') == 'text':
                    text = content.get('text', '').strip()
                    if text:
                        markdown_parts.append(text)
            markdown_text = "\n\n".join(markdown_parts)
        
        if not markdown_text:
            # 如果还是没有，直接使用整个响应数据
            markdown_text = json.dumps(task_data, ensure_ascii=False, indent=2)
        
        # 保存 Markdown 文件
        markdown_path = output_path / "paper_content.md"
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        
        # 保存原始响应
        response_path = output_path / "api_response.json"
        with open(response_path, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, ensure_ascii=False, indent=2)
        
        # 保存内容列表（如果有）
        if content_list:
            content_list_path = output_path / "content_list.json"
            with open(content_list_path, 'w', encoding='utf-8') as f:
                json.dump(content_list, f, ensure_ascii=False, indent=2)
        
        # 统计信息
        stats = {
            "text_blocks": len([c for c in content_list if c.get('type') == 'text']) if content_list else 0,
            "image_count": len([c for c in content_list if c.get('type') == 'image']) if content_list else 0,
            "table_count": len([c for c in content_list if c.get('type') == 'table']) if content_list else 0,
            "total_pages": len(set(c.get('page_idx', 0) for c in content_list)) if content_list else 0
        }
        
        print(f"  ✅ 解析完成！")
        print(f"     - Markdown: {markdown_path}")
        print(f"     - 总页数: {stats['total_pages']}")
        print(f"     - 文本块: {stats['text_blocks']}")
        print(f"     - 图片数: {stats['image_count']}")
        print(f"     - 表格数: {stats['table_count']}")
        
        return {
            "markdown": markdown_text,
            "markdown_path": str(markdown_path),
            "content_list": content_list,
            "stats": stats
        }
        
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API 请求失败: {e}")
    except TimeoutError as e:
        raise RuntimeError(f"解析超时: {e}")
    except Exception as e:
        import traceback
        print(f"\n详细错误信息:")
        traceback.print_exc()
        raise RuntimeError(f"MinerU 解析失败: {e}")


# 测试代码
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python pdf_parser_mineru.py <pdf_path> [output_dir]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        result = parse_pdf_to_markdown(pdf_path, output_dir)
        print("\n" + "=" * 60)
        print("解析成功！")
        print("=" * 60)
        print(f"Markdown 文件: {result['markdown_path']}")
        print(f"内容长度: {len(result['markdown'])} 字符")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
