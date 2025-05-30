# config.py
# 配置管理模块，用于保存全局设置和提供路径访问校验功能

# config/config.py（修改后）

import os
from typing import Optional, Union
from .args_parser import parse_args  # 使用相对导入

# 初始值（会被后续解析覆盖）
WRITE_ENABLED: bool = False
ALLOWED_WRITE_DIR: str = ""
ALLOWED_READ_DIR: str = ""

# 解析命令行参数并更新配置
try:
    _args = parse_args()
    WRITE_ENABLED = _args['WRITE_ENABLED']
    ALLOWED_WRITE_DIR = _args['ALLOWED_WRITE_DIR']
    ALLOWED_READ_DIR = _args['ALLOWED_READ_DIR']
except Exception as e:
    print(f"[FATAL] 配置初始化失败: {str(e)}")
    exit(1)
def is_path_allowed(target_path: str, allowed_dir: str) -> bool:
    """
    检查目标路径是否在允许的目录范围内（严格校验，已解析符号链接）。

    参数:
        target_path (str): 要检查的目标路径（例如用户请求的文件路径）
        allowed_dir (str): 允许的操作根目录（由命令行参数指定）

    返回:
        bool: 如果目标路径在允许的目录范围内，返回 True；否则返回 False
    """
    try:
        # 获取目标路径和允许目录的真实绝对路径（消除 .、.. 和符号链接）
        target_real = os.path.realpath(os.path.abspath(target_path))
        allowed_real = os.path.realpath(allowed_dir)

        # 判断目标路径是否在允许目录下
        return os.path.commonpath([target_real, allowed_real]) == allowed_real
    except (ValueError, FileNotFoundError):
        # 如果任意路径无效或无法访问，视为非法路径
        return False