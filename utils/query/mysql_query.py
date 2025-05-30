from resources.mysql import create_connection, close_connection

def execute_query(query, params=None):
    """
    执行SQL查询并返回结果。
    
    :param query: SQL查询语句
    :param params: 查询参数（可选）
    :return: 查询结果或空列表
    """
    connection = create_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"执行查询时出错: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        close_connection(connection)