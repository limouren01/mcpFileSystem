import os
from config.config import is_path_allowed, WRITE_ENABLED, ALLOWED_WRITE_DIR

def rename_folder(old_name: str, new_name: str, allowed_write_dir: str) -> dict:
    """重命名文件夹（严格路径校验）"""
    if not WRITE_ENABLED:
        return {"success": False, "message": "写入功能未启用"}

    old_abs_path = os.path.abspath(old_name)
    
    # 确保 new_name 是绝对路径
    if not os.path.isabs(new_name):
        new_name = os.path.join(os.path.dirname(old_abs_path), new_name)
    new_abs_path = os.path.abspath(new_name)

    # 校验原路径和目标路径是否都在允许范围内
    if not is_path_allowed(old_abs_path, allowed_write_dir) or not is_path_allowed(new_abs_path, allowed_write_dir):
        return {"success": False, "message": "路径越权访问"}

    if not os.path.isdir(old_abs_path):
        return {"success": False, "message": "指定的旧文件夹不存在"}

    try:
        print(f"[DEBUG] 尝试重命名文件夹从: {old_abs_path} 到: {new_abs_path}")  # 调试信息
        os.rename(old_abs_path, new_abs_path)
        if os.path.exists(new_abs_path) and not os.path.exists(old_abs_path):
            print(f"[DEBUG] 文件夹已成功重命名为: {new_abs_path}")  # 调试信息
            return {"success": True, "message": "文件夹重命名成功"}
        else:
            print(f"[DEBUG] 文件夹重命名失败")  # 调试信息
            return {"success": False, "message": "文件夹重命名失败"}
    except Exception as e:
        print(f"[ERROR] 重命名文件夹时出错: {e}")  # 调试信息
        return {"success": False, "message": f"重命名文件夹失败: {str(e)}"}