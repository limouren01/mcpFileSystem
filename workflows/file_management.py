# utils/workflows/file_management.py

from utils.add.create_folder import create_folder
from utils.modify.file_operations import move_file
from utils.query.list_and_manage_files import list_and_manage_files
from prompts.organize_files import organize_files_prompt
from typing import Dict, Union, List

from config.config import ALLOWED_WRITE_DIR  # 导入允许写入的目录

def organize_files_by_type(
    source_dir: str = ".",
    target_dir: str = "organized",
    file_type: str = ".md"
) -> Dict[str, Union[bool, str, List[str]]]:
    """
    将指定目录中某一类型的文件移动到目标目录中。
    如果目标目录不存在，则自动创建。
    """

    results = {
        "success": True,
        "moved_files": [],
        "failed_files": [],
        "message": ""
    }

    try:
        # Step 1: 使用 prompt 获取用户确认
        print(organize_files_prompt(source_dir, target_dir, file_type))

        # Step 2: 列出所有文件（递归）
        list_result = list_and_manage_files(source_dir, recursive=True)
        if not list_result["success"]:
            results["success"] = False
            results["message"] = "无法列出文件：" + list_result["message"]
            return results

        all_files = list_result.get("files", [])
        filtered_files = [f for f in all_files if f.endswith(file_type)]

        if not filtered_files:
            results["message"] = f"没有找到任何 {file_type} 文件。"
            return results

        # Step 3: 创建目标文件夹（如果不存在）
        create_result = create_folder(target_dir)
        if not create_result["success"] and "已存在" not in create_result.get("message", ""):
            results["success"] = False
            results["message"] = "无法创建目标文件夹：" + create_result["message"]
            return results

        # Step 4: 移动每个文件
        for src_file in filtered_files:
            move_result = move_file(src_file, target_dir)
            if move_result["success"]:
                results["moved_files"].append(src_file)
            else:
                results["failed_files"].append(src_file)
                results["success"] = False

        # Step 5: 构造结果信息
        results["message"] = f"成功移动 {len(results['moved_files'])} 个 {file_type} 文件到 {target_dir}。"
        if results["failed_files"]:
            results["message"] += f"\n以下文件移动失败：{', '.join(results['failed_files'])}"

    except Exception as e:
        results["success"] = False
        results["message"] = f"发生错误：{str(e)}"

    return results