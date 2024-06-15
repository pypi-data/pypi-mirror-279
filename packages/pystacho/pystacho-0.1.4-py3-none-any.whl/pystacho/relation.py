import copy
from pystacho.helper import Helper


class Relation:
    def __init__(self, model, query=None):
        if model is not None:
            self.model = model

        self.query = query or {
            'select': '*',
            'where': [],
            'group': '',
            'having': '',
            'order': [],
        }

        self.query_values = []
        self.query_sql = ''
        self.results = []

    # For len(results) support
    def __len__(self):
        self._run_engine()

        return len(self.results)

    # To support results[index]
    def __getitem__(self, index):
        self._run_engine()

        return self.results[index]

    # To support: for result in results: loop
    def __iter__(self):
        self._run_engine()

        return iter(self.results)

    def __repr__(self):
        self._run_engine()

        return f'{self.__class__.__name__}(results: {self.results})'

    def _run_engine(self, query_type='default'):
        self._make_sql()
        data = self._run_sql_query()
        self.results = []

        if query_type == 'default':
            self._wrap_default_data(data)
        elif query_type == 'count':
            self._wrap_count_data(data)
        elif query_type == 'ids':
            self._wrap_ids_data(data)
        elif query_type == 'individual':
            self._wrap_individual_data(data)

    def _run_sql_query(self):
        return self.model.execute_query(self.query_sql, self.query_values, False)

    def _wrap_default_data(self, data):
        if data:
            for item in data['results']:
                record = self.model.__class__()
                record._attributes = dict(zip(data['fields'], item))

                self.results.append(record)
        else:
            self.results = []

    def _wrap_individual_data(self, data):
        if data['results']:
            item = data['results'][0]
            record = self.model.__class__()
            record._attributes = dict(zip(data['fields'], item))

            self.results = record
        else:
            self.results = None

    def _wrap_count_data(self, data):
        if data:
            self.results = data['results'][0][0]
        else:
            self.results = 0

    def _wrap_ids_data(self, data):
        if data['results']:
            self.results = []
            for item in data['results']:
                self.results.append(item[0])
        else:
            self.results = []

    def _make_sql(self):
        self.query_sql, self.query_values = self.model._make_sql(self)

    def select(self, fields):
        new_query = copy.deepcopy(self.query)
        new_query['select'] = fields

        return Relation(self.model, new_query)

    def where(self, *args, **kwargs):
        new_query = copy.deepcopy(self.query)
        new_query.setdefault('where', []).append(Helper.process_user_arguments(*args, **kwargs))

        return Relation(self.model, new_query)

    def order(self, *args, **kwargs):
        new_query = copy.deepcopy(self.query)
        new_query['order'] = [Helper.process_user_arguments(*args, **kwargs)]

        return Relation(self.model, new_query)

    def limit(self, limit, offset=0):
        new_query = copy.deepcopy(self.query)
        new_query['limit'] = limit
        new_query['offset'] = offset

        return Relation(self.model, new_query)

    def offset(self, offset=0):
        new_query = copy.deepcopy(self.query)
        new_query['offset'] = offset

        return Relation(self.model, new_query)

    def last(self, limit=1):
        old_query = copy.deepcopy(self.query)
        self.query['limit'] = limit
        self.query['order'] = [{'id': 'desc'}]
        if limit == 1:
            self._run_engine('individual')
        else:
            self._run_engine()

        self.query = old_query

        return self.results

    def first(self, limit=1):
        old_query = copy.deepcopy(self.query)
        self.query['limit'] = limit
        self.query['order'] = [{'id': 'asc'}]
        if limit == 1:
            self._run_engine('individual')
        else:
            self._run_engine()

        self.query = old_query

        return self.results

    def count(self):
        old_select = self.query.get('select', '*')
        self.query['select'] = 'count(*)'

        self._run_engine('count')

        self.query['select'] = old_select

        return self.results

    def ids(self):
        old_select = self.query.get('select', '*')
        self.query['select'] = 'id'

        self._run_engine('ids')

        self.query['select'] = old_select

        return self.results

    def group(self, fields=''):
        new_query = copy.deepcopy(self.query)
        new_query['group'] = fields

        return Relation(self.model, new_query)

    def having(self, condition=''):
        new_query = copy.deepcopy(self.query)
        new_query['having'] = condition

        return Relation(self.model, new_query)

    # def delete_all(self):
    #     pass
    #
    # def update_all(self, **kwargs):
    #     pass
