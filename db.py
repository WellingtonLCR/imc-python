import mysql.connector

from mysql.connector import Error, pooling

DB_PARAMS = {
    'host':'localhost',
    'user': 'root',
    'password': '',
    'database':'bd_imc',
    'charset': 'utf8mb4',
    'timezone':'-03:00',
    'usepure': 'True'
    'connect_timeout': 10
}

_pool = pool.MysqConnectionPool(
    pool_name = 'imc_pool',
    pool_size = 5,
    **DB_PARAMS
)