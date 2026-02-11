#!/bin/bash
# 修复 Pydantic 版本冲突 - 安装 magic-pdf 兼容版本
# magic-pdf 0.10.5 要求: pydantic<2.8.0,>=2.7.2

echo "=========================================="
echo "Pydantic 版本修复 (针对 magic-pdf)"
echo "=========================================="
echo ""

# 激活 conda 环境
source ~/anaconda3/etc/profile.d/conda.sh
conda activate paperreviewer

echo "[1/4] 卸载不兼容的版本..."
pip uninstall -y pydantic pydantic-core

echo ""
echo "[2/4] 安装 magic-pdf 兼容版本..."
echo "  要求: pydantic>=2.7.2,<2.8.0"
# 安装 pydantic 2.7.4 和对应的 pydantic-core
pip install "pydantic==2.7.4"

echo ""
echo "[3/4] 验证版本..."
pip show pydantic | grep -E "(Name|Version)"
pip show pydantic-core | grep -E "(Name|Version)"

echo ""
echo "[4/4] 测试导入..."
python -c "
try:
    from pydantic import BaseModel
    print('✅ Pydantic 导入成功')
    
    # 测试 magic-pdf 导入
    from magic_pdf.data.data_reader_writer import FileBasedDataWriter
    print('✅ magic-pdf 导入成功')
    
    print('')
    print('✅✅✅ 所有测试通过！')
except ImportError as e:
    print(f'❌ 导入失败: {e}')
    import traceback
    traceback.print_exc()
    exit(1)
"

echo ""
echo "=========================================="
echo "修复完成！可以运行 test_stage1.py 了"
echo "=========================================="
