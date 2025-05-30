#导入设置
from typing import Dict, Union
from config.config import ALLOWED_READ_DIR, ALLOWED_WRITE_DIR
# 导入提示函数
from prompts.organize_files import organize_files_prompt


def register_prompt_plugins(mcp):
    """
    实际执行提示插件注册逻辑。
    """
    @mcp.prompt()
    def greeting_prompt(name: str) -> str:
        """
        生成个性化的问候语。
        
        参数:
            name (str): 用户的名字。
            
        返回:
            str: 个性化问候语。
        """
        return f"你好，{name}！欢迎来到我们的服务。请问有什么可以帮助您的吗？"

    # 注册提示函数
    @mcp.prompt()
    def organize_files_workflow_prompt(
        source_dir: str = ".",
        target_dir: str = "organized",
        file_type: str = ".md"
    ) -> str:
        """
        生成一个关于文件整理流程的提示信息。
        
        参数:
            source_dir (str): 源目录路径。
            target_dir (str): 目标目录路径。
            file_type (str): 文件类型过滤器。
            
        返回:
            str: 用户友好的提示文本，用于前端显示并获取用户确认。
        """
        return organize_files_prompt(source_dir, target_dir, file_type)