#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 切换到项目目录
cd "$SCRIPT_DIR"

echo "开始更新 TODO Tools..."

# 拉取最新代码（如果是git仓库）
if [ -d .git ]; then
    echo "从git仓库更新代码..."
    git pull
fi

# 重新安装包
echo "重新安装包..."
pip3 install -e . --break-system-packages

# 更新系统链接
echo "更新系统链接..."
chmod +x todo
sudo ln -sf $(pwd)/todo /usr/local/bin/todo

echo "更新完成！"

# 显示当前版本
echo "当前版本信息："
todo --version || echo "版本信息不可用" 