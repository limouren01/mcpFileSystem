from resources.mysql import create_connection, close_connection

def update_data(query: str, params: tuple) -> bool:
    """
    执行SQL更新语句。
    
    :param query: SQL更新语句
    :param params: 更新参数
    :return: 操作是否成功
    """
    connection = create_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        return True
    except Exception as e:
        print(f"更新数据时出错: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)