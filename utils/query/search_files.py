import os
from config.config import is_path_allowed, ALLOWED_READ_DIR

def search_files(keyword: str, folder_path: str, allowed_read_dir: str ,recursive: bool = True) -> dict:
    """安全搜索文件（双重路径校验）"""
    abs_folder = os.path.abspath(folder_path)
    if not is_path_allowed(abs_folder, allowed_read_dir):
        return {"success": False, "message": "搜索路径越权"}

    if not os.path.exists(abs_folder):
        return {"success": False, "message": "指定的文件夹不存在"}

    keyword = keyword.lower()
    result = []
    try:
        if recursive:
            for root, dirs, files in os.walk(abs_folder, followlinks=False):
                for name in dirs + files:
                    full_path = os.path.join(root, name)
                    # 路径合法性校验
                    if is_path_allowed(full_path, allowed_read_dir) and keyword in name.lower():
                        result.append(full_path)
        else:
            for name in os.listdir(abs_folder):
                full_path = os.path.join(abs_folder, name)
                if is_path_allowed(full_path, allowed_read_dir) and keyword in name.lower():
                    result.append(full_path)

        return {
            "success": True,
            "matches": result,
            "message": f"共找到 {len(result)} 个合法匹配项"
        }
    except Exception as e:
        return {"success": False, "message": f"搜索异常: {str(e)}"}