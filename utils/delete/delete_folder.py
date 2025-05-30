import os
import shutil
from config.config import is_path_allowed, WRITE_ENABLED, ALLOWED_WRITE_DIR

def delete_folder(folder_path: str, allowed_write_dir: str) -> dict:
    """删除文件夹及其内容（严格路径校验）"""
    if not WRITE_ENABLED:
        return {"success": False, "message": "写入功能未启用"}

    abs_path = os.path.abspath(folder_path)
    if not is_path_allowed(abs_path, allowed_write_dir):
        return {"success": False, "message": "路径越权访问"}

    if not os.path.isdir(abs_path):
        return {"success": False, "message": "指定的文件夹不存在"}

    try:
        shutil.rmtree(abs_path)
        return {"success": True, "message": "文件夹删除成功"}
    except Exception as e:
        return {"success": False, "message": f"删除文件夹失败: {str(e)}"}