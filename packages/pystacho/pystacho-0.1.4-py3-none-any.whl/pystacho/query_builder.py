class QueryBuilder:
    def __init__(self, adapter):
        self._adapter = adapter

    def execute_query(self, query, values, only_first_result=True):
        return self._adapter.execute_query(query, values, only_first_result)

    # - - - - - - - - - - - - - - - - - -
    # Methods for Model
    # - - - - - - - - - - - - - - - - - -
    def insert_sql(self, record):
        return self._adapter.insert_sql(record)

    def update_sql(self, record):
        return self._adapter.update_sql(record)

    def delete_sql(self, record):
        return self._adapter.delete_sql(record)

    def find_sql(self, model_class, value):
        return self._adapter.find_sql(model_class, value)

    def find_by_sql(self, model_class, **kwargs):
        return self._adapter.find_by_sql(model_class, **kwargs)

    # - - - - - - - - - - - - - - - - - -
    # Methods for Relation
    # - - - - - - - - - - - - - - - - - -
    def _make_sql(self, relation):
        query = self._adapter.make_select_sql(relation)
        query += self._adapter.make_from_sql(relation)
        where_query, query_values = self._adapter.make_where_sql(relation)
        query += where_query
        query += self._adapter.make_group_sql(relation)
        query += self._adapter.make_having_sql(relation)
        query += self._adapter.make_order_sql(relation)
        query += self._adapter.make_limit_sql(relation)
        query += self._adapter.make_offset_sql(relation)

        return query, query_values


