#!/bin/bash
# 完整修复脚本：Pydantic + Numpy + doclayout-yolo

echo "=========================================="
echo "完整依赖修复脚本"
echo "=========================================="
echo ""

# 激活 conda 环境
source ~/anaconda3/etc/profile.d/conda.sh
conda activate paperreviewer

echo "[1/6] 安装 numpy 兼容版本..."
echo "  magic-pdf 要求: numpy<2.0.0,>=1.21.6"
pip install "numpy<2.0.0,>=1.21.6"

echo ""
echo "[2/6] 安装 doclayout-yolo..."
pip install doclayout-yolo

echo ""
echo "[3/6] 验证关键包版本..."
echo "---"
pip show numpy | grep -E "(Name|Version)"
pip show pydantic | grep -E "(Name|Version)"
pip show pydantic-core | grep -E "(Name|Version)"
pip show doclayout-yolo | grep -E "(Name|Version)" || echo "  (未安装 doclayout-yolo)"

echo ""
echo "[4/6] 检查依赖冲突..."
pip check | head -20

echo ""
echo "[5/6] 测试导入..."
python -c "
import sys
success_count = 0
total_tests = 5

print('测试 1/5: numpy...')
try:
    import numpy as np
    print(f'  ✅ numpy {np.__version__}')
    success_count += 1
except ImportError as e:
    print(f'  ❌ {e}')

print('测试 2/5: pydantic...')
try:
    from pydantic import BaseModel
    import pydantic
    print(f'  ✅ pydantic {pydantic.__version__}')
    success_count += 1
except ImportError as e:
    print(f'  ❌ {e}')

print('测试 3/5: pydantic_core...')
try:
    import pydantic_core
    print(f'  ✅ pydantic_core {pydantic_core.__version__}')
    success_count += 1
except ImportError as e:
    print(f'  ❌ {e}')

print('测试 4/5: magic-pdf...')
try:
    from magic_pdf.data.data_reader_writer import FileBasedDataWriter
    from magic_pdf.pipe.UNIPipe import UNIPipe
    print('  ✅ magic-pdf 导入成功')
    success_count += 1
except ImportError as e:
    print(f'  ❌ {e}')
    import traceback
    traceback.print_exc()

print('测试 5/5: doclayout_yolo...')
try:
    from doclayout_yolo import YOLOv10
    print('  ✅ doclayout_yolo 导入成功')
    success_count += 1
except ImportError as e:
    print(f'  ❌ {e}')

print('')
print(f'{'=' * 40}')
print(f'测试结果: {success_count}/{total_tests} 通过')
print(f'{'=' * 40}')

if success_count == total_tests:
    print('✅✅✅ 所有测试通过！')
    sys.exit(0)
else:
    print('❌ 部分测试失败，请检查错误信息')
    sys.exit(1)
"

RESULT=$?

echo ""
echo "[6/6] 总结"
if [ $RESULT -eq 0 ]; then
    echo "=========================================="
    echo "✅ 修复成功！"
    echo "可以运行: python test_stage1.py"
    echo "=========================================="
else
    echo "=========================================="
    echo "⚠️  部分问题仍需解决"
    echo "请查看上方错误信息"
    echo "=========================================="
fi
