import os
from config.config import is_path_allowed, WRITE_ENABLED, ALLOWED_WRITE_DIR
def create_folder(folder_path: str, allowed_write_dir: str = ALLOWED_WRITE_DIR) -> dict:
    """创建文件夹（严格路径校验）"""
    if not WRITE_ENABLED:
        return {"success": False, "message": "写入功能未启用"}

    abs_path = os.path.abspath(folder_path)
    if not is_path_allowed(abs_path, allowed_write_dir):
        return {"success": False, "message": "路径越权访问"}

    try:
        os.makedirs(abs_path, exist_ok=True)
        print(f"[DEBUG] 尝试创建文件夹: {abs_path}")  # 调试信息
        if os.path.exists(abs_path):
            print(f"[DEBUG] 文件夹已成功创建: {abs_path}")  # 调试信息
        else:
            print(f"[DEBUG] 文件夹创建失败: {abs_path}")  # 调试信息
        return {"success": True, "message": "文件夹创建成功"}
    except Exception as e:
        print(f"[ERROR] 创建文件夹时出错: {e}")  # 调试信息
        return {"success": False, "message": f"创建文件夹失败: {str(e)}"}