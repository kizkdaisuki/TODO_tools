#!/bin/bash

# 安装 Python 包
pip3 install -e . --break-system-packages

# 添加到系统路径
chmod +x todo
sudo ln -sf $(pwd)/todo /usr/local/bin/todo