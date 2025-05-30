import argparse
import os
import sys
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

def get_exe_dir():
    # 判断是否打包环境
    if getattr(sys, 'frozen', False):
        # sys.executable是exe的绝对路径
        return os.path.dirname(sys.executable)
    else:
        # 开发环境下使用当前文件的目录
        return os.path.dirname(os.path.abspath(__file__))

# 动态构建.env文件的绝对路径
env_path = os.path.join(get_exe_dir(), '.env')

load_dotenv(dotenv_path=env_path)  # 加载.env文件


from plugins.register_all_plugins import register_all_plugins

# ========================
# 从 config 模块导入最终配置
# ========================
from config.config import WRITE_ENABLED, ALLOWED_WRITE_DIR, ALLOWED_READ_DIR

# ========================
# MCP 工具定义（直接使用 config 中的变量）
# ========================
mcp = FastMCP()

register_all_plugins(mcp)


# ========================
# 主程序入口（已移除 init_config）
# ========================
if __name__ == "__main__":
    # 打印配置信息（验证用）
    print(f"[INFO] 写入功能已 {'启用' if WRITE_ENABLED else '禁用'}")
    print(f"[INFO] 允许读/写真实路径: {ALLOWED_WRITE_DIR}")
    # 切换默认工作目录到 rootdir (ALLOWED_WRITE_DIR)
    try:
        os.chdir(ALLOWED_WRITE_DIR)
        print(f"[INFO] 已切换默认工作目录至: {os.getcwd()}")
    except Exception as e:
        print(f"[ERROR] 无法切换工作目录至 {ALLOWED_WRITE_DIR}: {str(e)}")
        exit(1)
    print(f"[INFO] 启动 MCP 服务器...")
    try:
        mcp.run(transport='stdio')
        # mcp.run(transport='sse')
    except Exception as e:
        print(f"[ERROR] 启动失败: {str(e)}")