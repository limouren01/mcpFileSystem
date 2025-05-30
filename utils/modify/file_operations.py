# utils/modify/file_operations.py

import os
import shutil
from config.config import is_path_allowed, WRITE_ENABLED, ALLOWED_WRITE_DIR

def move_file(src_path: str, dest_dir: str) -> dict:
    """将指定的文件或文件夹移动到目标目录"""
    if not WRITE_ENABLED:
        return {"success": False, "message": "写入功能未启用"}

    src_abs_path = os.path.abspath(src_path)
    dest_abs_dir = os.path.abspath(dest_dir)

    # 确保源路径和目标目录在允许的范围内
    if not is_path_allowed(src_abs_path, ALLOWED_WRITE_DIR) or not is_path_allowed(dest_abs_dir, ALLOWED_WRITE_DIR):
        return {"success": False, "message": "路径越权访问"}

    if not os.path.exists(src_abs_path):
        return {"success": False, "message": "指定的源路径不存在"}

    if not os.path.isdir(dest_abs_dir):
        return {"success": False, "message": "指定的目标文件夹不存在"}

    try:
        dest_full_path = os.path.join(dest_abs_dir, os.path.basename(src_abs_path))
        print(f"[DEBUG] 尝试将内容从 {src_abs_path} 移动到 {dest_full_path}")
        shutil.move(src_abs_path, dest_full_path)

        if os.path.exists(dest_full_path) and not os.path.exists(src_abs_path):
            print(f"[DEBUG] 内容已成功移动到 {dest_full_path}")
            return {"success": True, "message": "内容移动成功"}
        else:
            print(f"[DEBUG] 内容移动失败")
            return {"success": False, "message": "内容移动失败"}
    except Exception as e:
        print(f"[ERROR] 移动内容时出错: {e}")
        return {"success": False, "message": f"移动内容失败: {str(e)}"}