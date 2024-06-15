import relationalai as rai

def main():
    """
    This example shows how to issue SQL queries directly
    using the same connection that PyRel uses.
    """
    model = rai.Model("Example")

    # one-line example:
    print(model.resources._exec("select 1 + 1;").fetch_pandas_all())

    # accessing the connection object directly:
    conn = model.resources._conn
    with conn.cursor() as cursor:
        cursor.execute("select 2 + 2;")
        print(cursor.fetch_pandas_all())

main()
