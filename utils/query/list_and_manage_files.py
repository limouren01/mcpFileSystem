import os
from config.config import is_path_allowed

# 修改后的函数定义
def list_and_manage_files(folder_path: str, recursive: bool = True, allowed_read_dir: str = "") -> dict:
    """列出并管理文件（严格路径检查）"""
    abs_folder = os.path.abspath(folder_path)
    
    if not is_path_allowed(abs_folder, allowed_read_dir):
        return {"success": False, "message": "路径越权访问"}

    if not os.path.exists(abs_folder):
        return {"success": False, "message": "指定的文件夹不存在"}

    result = []
    try:
        if recursive:
            for root, dirs, files in os.walk(abs_folder, followlinks=False):
                # 过滤非法路径（二次校验）
                valid_items = []
                for name in dirs + files:
                    item_path = os.path.join(root, name)
                    if is_path_allowed(item_path, allowed_read_dir):
                        valid_items.append(item_path)
                    else:
                        print(f"[WARNING] 忽略越权路径: {item_path}")
                result.extend(valid_items)
        else:
            for name in os.listdir(abs_folder):
                item_path = os.path.join(abs_folder, name)
                if is_path_allowed(item_path, allowed_read_dir):
                    result.append(item_path)
                else:
                    print(f"[WARNING] 忽略越权路径: {item_path}")

        return {
            "success": True,
            "files": result,
            "message": f"成功列出{'所有' if recursive else '顶级'}{len(result)}个合法文件/文件夹"
        }
    except FileNotFoundError:
        return {"success": False, "message": "指定的文件夹不存在"}
    except PermissionError:
        return {"success": False, "message": "权限不足"}
    except Exception as e:
        return {"success": False, "message": f"目录遍历失败: {str(e)}"}