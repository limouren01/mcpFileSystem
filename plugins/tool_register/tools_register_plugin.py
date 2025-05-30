#导入设置
from typing import Dict, Union, Optional
from config.config import ALLOWED_READ_DIR, ALLOWED_WRITE_DIR
# 导入工具函数
from utils.add.copy_file import batch_copy_files, copy_file
from utils.add.create_folder import create_folder
from utils.add.write_to_file import write_to_file, write_to_excel
from utils.delete.delete_file import delete_file
from utils.delete.delete_folder import delete_folder
from utils.modify.rename_folder import rename_folder
from utils.modify.file_operations import move_file
from utils.query.list_and_manage_files import list_and_manage_files
from utils.query.read_file import read_file
from utils.query.search_files import search_files
from utils.query.mysql_query import execute_query
from utils.add.mysql_add import insert_data
from utils.modify.mysql_modify import update_data
from utils.delete.mysql_delete import delete_data


def register_tool_plugins(mcp):
    @mcp.tool()
    def _copy_file(src_path: str, dest_path: str) -> Dict[str, Union[bool, str]]:
        """复制文件（双重路径校验）"""
        return copy_file(src_path, dest_path)

    @mcp.tool()
    def _batch_copy_files(src_dir: str, dest_dir: str, extensions: list = None, overwrite: bool = False) -> dict:
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
        return batch_copy_files(src_dir, dest_dir, extensions, overwrite)
    
    @mcp.tool()
    def _write_to_file(file_path: str, content: str) -> Dict[str, Union[bool, str]]:
        """写入内容到文件（双重路径校验）"""
        return write_to_file(file_path, content)
    
    @mcp.tool()
    def _write_to_excel(file_path: str, data: list, sheet_name: str = "Sheet1") -> Dict[str, Union[bool, str]]:
        """写入数据到Excel文件（双重路径校验）"""
        return write_to_excel(file_path, data, sheet_name)
    

    @mcp.tool()
    def _create_folder(folder_path: str) -> Dict[str, Union[bool, str]]:
        """创建文件夹（双重路径校验）
        本工具为文件创建工具，请谨慎使用
        """
        return create_folder(folder_path, ALLOWED_WRITE_DIR)

    @mcp.tool()
    def _delete_file(file_path: str) -> Dict[str, Union[bool, str]]:
        """删除文件（双重路径校验）
        本工具为文件删除工具，请谨慎使用
        """
        return delete_file(file_path, ALLOWED_WRITE_DIR)

    @mcp.tool()
    def _delete_folder(folder_path: str) -> Dict[str, Union[bool, str]]:
        """删除文件夹（双重路径校验）
        本工具为文件删除工具，请谨慎使用
        """
        return delete_folder(folder_path, ALLOWED_WRITE_DIR)

    @mcp.tool()
    def _rename_folder(old_name: str, new_name: str) -> Dict[str, Union[bool, str]]:
        """重命名文件夹（双重路径校验）"""
        return rename_folder(old_name, new_name, ALLOWED_WRITE_DIR)

    @mcp.tool()
    def _move_file(src_path: str, dest_dir: str) -> Dict[str, Union[bool, str]]:
        """移动文件（双重路径校验）"""
        return move_file(src_path, dest_dir)

    @mcp.tool()
    def _list_and_manage_files(folder_path: str, recursive: bool = True) -> Dict[str, Union[bool, str, list]]:
        """列出并管理文件（双重路径校验）"""
        return list_and_manage_files(folder_path, recursive, ALLOWED_READ_DIR)

    @mcp.tool()
    def _read_file(file_path: str) -> Dict[str, Union[bool, str, list]]:
        """读取文件内容（双重路径校验）"""
        return read_file(file_path, ALLOWED_READ_DIR)
    
    @mcp.tool()
    def _search_files(keyword: str, folder_path: str, recursive: bool = True) -> Dict[str, Union[bool, list, str]]:
        """安全搜索文件（双重路径校验）"""
        return search_files(keyword=keyword,folder_path=folder_path,allowed_read_dir=ALLOWED_READ_DIR,  recursive=recursive)
    
    @mcp.tool()
    def _execute_query(query: str, params: Optional[list] = None) -> Dict[str, Union[bool, list, str]]:
        """执行SQL查询并返回结果（双重路径校验）"""
        return execute_query(query, params)
    
    @mcp.tool()
    def _insert_data(query: str, params: tuple) -> bool:
        """
        执行SQL插入语句。
        注意连接的是mysql数据库，占位符为%s，而不是?
        :param query: SQL插入语句
        :param params: 插入参数
        :return: 操作是否成功
        """
        return insert_data(query, params)
    
    @mcp.tool()
    def _update_data(query: str, params: tuple) -> bool:
        """
        执行SQL更新语句。
        注意连接的是mysql数据库，占位符为%s，而不是?
        :param query: SQL更新语句
        :param params: 更新参数
        :return: 操作是否成功
        """
        return update_data(query, params)

    @mcp.tool()
    def _delete_data(query: str, params: tuple) -> bool:
        """
        执行SQL删除语句。
        注意连接的是mysql数据库，占位符为%s，而不是?
        :param query: SQL删除语句
        :param params: 删除参数
        :return: 操作是否成功
        """
        return delete_data(query, params)
