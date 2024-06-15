from mysql.connector import pooling
from contextlib import contextmanager
import time
from pystacho.logger import Logger


class Mysql:
    ENGINE_NAME = 'MySql'
    WRAP_CHAR = '`'

    def __init__(self, config):
        self._config = config

    def connection_pool(self):
        return pooling.MySQLConnectionPool(
            pool_name="pystacho_pool",
            pool_size=self._config["pool_size"],
            pool_reset_session=True,
            host=self._config["host"],
            port=self._config["port"],
            user=self._config["user"],
            password=self._config["password"],
            database=self._config["name"]
        )

    @contextmanager
    def database_connection(self):
        connection = self.connection_pool().get_connection()
        try:
            yield connection
        finally:
            connection.close()

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # Creator methods -
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    def wrap_items(self, item, table_name=None):
        wrapped_table_name = ''
        if table_name:
            wrapped_table_name = f"{self.WRAP_CHAR}{table_name}{self.WRAP_CHAR}."

        return f"{wrapped_table_name}{self.WRAP_CHAR}{item}{self.WRAP_CHAR}"

    def query_requires_commit(self, query):
        if query.strip().lower().startswith('insert'):
            return True
        elif query.strip().lower().startswith('update'):
            return True
        elif query.strip().lower().startswith('delete'):
            return True
        else:
            return False

    def query_inserts_record(self, query):
        if query.strip().lower().startswith('insert'):
            return True

        return False

    def execute_query(self, query, values, only_first_result=True):
        with self.database_connection() as connection:
            with connection.cursor() as cursor:
                data = {
                    'results': None,
                    'fields': None,
                    'last_record_id': None,
                }
                start_time = time.time() * 1000
                cursor.execute(query, values)
                if self.query_requires_commit(query):
                    connection.commit()

                end_time = time.time() * 1000
                duration = end_time - start_time
                data['duration'] = duration
                if cursor.description:
                    data['fields'] = [field[0] for field in cursor.description]

                Logger.log_sql(query, values, duration, self.ENGINE_NAME)

                if self.query_inserts_record(query):
                    data['last_record_id'] = cursor.lastrowid

                if only_first_result:
                    data['results'] = [cursor.fetchone()]
                else:
                    data['results'] = cursor.fetchall()

                return data

    # - - - - - - - - - - - - - - - - - -
    # Methods for Model
    # - - - - - - - - - - - - - - - - - -
    def insert_sql(self, record):
        columns = ', '.join([self.wrap_items(field, record._table_name()) for field in record._attributes.keys()])
        values = ', '.join(['%s'] * len(record._attributes))
        sql = f"INSERT INTO {self.wrap_items(record._table_name())} ({columns}) VALUES ({values})"

        return sql, list(record._attributes.values())

    def update_sql(self, record):
        where_clause = f'{self.wrap_items(record._id(), record._table_name())} = {record._id_value()}'
        set_clause = ', '.join([f"{self.wrap_items(key, record._table_name())} = %s" for key in record._attributes.keys()])
        sql = f"UPDATE {self.wrap_items(record._table_name())} SET {set_clause} WHERE {where_clause};"

        return sql, list(record._attributes.values())

    def delete_sql(self, record):
        where_clause = f'{self.wrap_items(record._id(), record._table_name())} = %s'
        sql = f"DELETE FROM {self.wrap_items(record._table_name())} WHERE {where_clause};"

        return sql, list([record._id_value()])

    def find_sql(self, model_class, value):
        return (f"SELECT * FROM {self.wrap_items(model_class._table_name())} " +
                f"WHERE {self.wrap_items(model_class._id(), model_class._table_name())} = %s", (value,))

    def find_by_sql(self, model_class, **kwargs):
        conditions = []
        values = []
        for key, value in kwargs.items():
            conditions.append(f"{self.wrap_items(key, model_class._table_name())} = %s")
            values.append(value)

        where_clause = " AND ".join(conditions)
        sql_query = f"SELECT * FROM {self.wrap_items(model_class._table_name())} WHERE {where_clause}"

        return sql_query, values

    # - - - - - - - - - - - - - - - - - -
    # Methods for Relation
    # - - - - - - - - - - - - - - - - - -
    def make_select_sql(self, relation):
        return f"SELECT {relation.query.get('select', '*')}"

    def make_from_sql(self, relation):
        return f" FROM {relation.model._table_name()}"

    def make_where_sql(self, relation):
        query_values = []
        conditions = relation.query.get('where', [])

        if not conditions:
            return '', []

        sql_query = ' WHERE ('

        for index, condition in enumerate(conditions):
            conditions = []

            if index > 0:
                sql_query += " AND ("

            for key, value in condition.items():
                if isinstance(value, str) or isinstance(value, int):
                    conditions.append(f"{key} = %s")
                    query_values.append(value)
                elif isinstance(value, list):
                    conditions.append(key)
                    query_values += value

            where_clause = " AND ".join(conditions)
            sql_query += where_clause + ")"

        return sql_query, query_values

    def make_group_sql(self, relation):
        if not relation.query['group']:
            return ''

        return f" GROUP BY {relation.query['group']} "

    def make_having_sql(self, relation):
        if not relation.query['having']:
            return ''

        return f" HAVING {relation.query['having']}"

    def make_order_sql(self, relation):
        query_order_fields = relation.query.get('order', [])
        if not query_order_fields:
            return ''

        sql_query = ' ORDER BY '

        order_fields = []
        for index, condition in enumerate(query_order_fields):
            for key, value in condition.items():
                if isinstance(value, str) or isinstance(value, int):
                    order_fields.append(f"{key} {value}")
                elif isinstance(value, list):
                    order_fields.append(key)
                else:
                    order_fields.append(key)

            order_clause = ", ".join(order_fields)
            sql_query += order_clause

        return sql_query

    def make_limit_sql(self, relation):
        if 'limit' not in relation.query:
            return ''

        return f" LIMIT {relation.query['limit']}"

    def make_offset_sql(self, relation):
        if 'offset' not in relation.query:
            return ''

        return f" OFFSET {relation.query['offset']}"
