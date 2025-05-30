# config/args_parser.py（修改后）

import os
from dotenv import load_dotenv

def parse_args():
    """
    解析环境变量，以获取服务端运行所需的配置。
    
    """
    # load_dotenv() # 加载 .env 文件中的环境变量
    print(os.getenv('MCP_ALLOWWRITE'))
    write_enabled = os.getenv('MCP_ALLOWWRITE', 'false').lower() == 'true'
    print(f"write_enabled: {write_enabled}")
    rootdir_abs = os.path.abspath(os.getenv('MCP_ROOTDIR', '/'))
    
    allowed_write_dir = os.path.realpath(rootdir_abs)

    if not os.path.isdir(allowed_write_dir):
        raise ValueError(f"指定的路径不是一个有效目录: {allowed_write_dir}")

    # 直接返回解析结果，不依赖外部配置
    return {
        'WRITE_ENABLED': write_enabled,
        'ALLOWED_WRITE_DIR': allowed_write_dir,
        'ALLOWED_READ_DIR': allowed_write_dir
    }