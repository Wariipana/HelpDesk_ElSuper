import pymysql


def obtenerconexion():
    try:
        connection = pymysql.connect(
            host='trolley.proxy.rlwy.net',
            port=23707,
            user='root',
            password='hkgInrsJKwLolWdhqHOnoPtLGIpQpVMe',
            database='railway',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        return None
