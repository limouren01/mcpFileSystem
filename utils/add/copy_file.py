# utils/add/copy_file.py

import os
import shutil
from config.config import is_path_allowed, ALLOWED_READ_DIR, ALLOWED_WRITE_DIR

def copy_file(src_path: str, dest_path: str) -> dict:
    """
    复制文件从源路径到目标路径。
    
    参数:
        src_path (str): 源文件路径。
        dest_path (str): 目标文件路径。
        
    返回:
        dict: 包含操作结果的状态和消息。
    """
    abs_src_path = os.path.abspath(src_path)
    abs_dest_path = os.path.abspath(dest_path)

    # 检查源路径是否可读
    if not is_path_allowed(abs_src_path, ALLOWED_READ_DIR):
        return {"success": False, "message": f"无权读取源路径: {src_path}"}

    # 检查目标路径是否在允许写入范围内
    dest_dir = os.path.dirname(abs_dest_path)
    if not is_path_allowed(dest_dir, ALLOWED_WRITE_DIR):
        return {"success": False, "message": f"目标路径越权访问: {dest_path}"}

    # 确保源文件存在
    if not os.path.isfile(abs_src_path):
        return {"success": False, "message": f"源文件不存在: {src_path}"}

    try:
        # 使用 copy2 保留元数据
        shutil.copy2(abs_src_path, abs_dest_path)
        return {"success": True, "message": f"文件复制成功: {src_path} -> {dest_path}"}
    except Exception as e:
        return {"success": False, "message": f"复制文件失败: {str(e)}"}
    

def batch_copy_files(src_dir: str, dest_dir: str, extensions: list = None, overwrite: bool = False) -> dict:
    """
    批量复制符合特定扩展名的文件从源目录（含子目录）到目标目录，不保留源文件夹结构。
    
    参数:
        src_dir (str): 源目录路径。
        dest_dir (str): 目标目录路径。
        extensions (list): 要复制的文件扩展名列表（如 ['.txt', '.log']），若为 None 则复制所有文件。
        overwrite (bool): 是否覆盖已存在的文件，默认为 False。
        
    返回:
        dict: 包含操作结果统计信息。
    """
    success_count = 0
    failed_count = 0
    failed_files = []

    # 校验源目录是否存在
    if not os.path.isdir(src_dir):
        return {"success": False, "message": f"源目录不存在: {src_dir}"}

    # 确保目标目录存在
    os.makedirs(dest_dir, exist_ok=True)

    # 如果没有提供扩展名，则默认复制所有文件
    if extensions is None:
        extensions = []

    # 遍历源目录及其子目录中的所有文件
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_path = os.path.join(root, file)

            # 如果有指定扩展名，则进行过滤
            if extensions:
                _, ext = os.path.splitext(file)
                if ext.lower() not in [e.lower() for e in extensions]:
                    continue

            # 构造目标路径，直接放到目标目录下，不保留源文件夹结构
            dest_path = os.path.join(dest_dir, file)

            # 如果文件已经存在且不允许覆盖，则跳过
            if os.path.exists(dest_path) and not overwrite:
                continue

            # 调用已有的 copy_file 函数执行复制
            result = copy_file(src_path, dest_path)
            if result["success"]:
                success_count += 1
            else:
                failed_count += 1
                failed_files.append({"file": src_path, "reason": result["message"]})

    return {
        "success": True,
        "total_success": success_count,
        "total_failed": failed_count,
        "failed_files": failed_files,
        "message": f"共处理 {success_count + failed_count} 个文件，成功复制 {success_count} 个，失败 {failed_count} 个。"
    }