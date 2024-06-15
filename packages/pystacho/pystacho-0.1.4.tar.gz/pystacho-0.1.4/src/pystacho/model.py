import inflect
import copy
from pystacho.database import Database
from pystacho.relation import Relation
from pystacho.helper import Helper

class Model(Database):
    DEFAULT_ID_FIELD = 'id'

    def __init__(self, **kwargs):
        super().__init__()

        self._attributes = {}
        self._setup_attributes(**kwargs)

    def __getattr__(self, name):
        if name in self._attributes:
            return self._attributes[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith('_') or name.startswith('__'):
            super().__setattr__(name, value)
        else:
            if '_attributes' not in self.__dict__:
                super().__setattr__('_attributes', {})

            self._attributes[name] = value

    def __repr__(self):
        return f'{self.__class__.__name__}({self._attributes})'

    def _class_name(self):
        return self.__class__.__name__

    def _plural_class_name(self):
        class_name = self._class_name()
        return self._inflector.plural(class_name)

    def _table_name(self):
        return self._plural_class_name().lower()

    def _id(self):
        return self.DEFAULT_ID_FIELD

    def _id_value(self):
        if self._id() in self._attributes.keys():
            return self._attributes[self._id()]
        else:
            return None

    def _setup_attributes(self, **kwargs):
        self._inflector = inflect.engine()
        for key, value in kwargs.items():
            self._attributes[key] = value

    @staticmethod
    def _base_query_params(new_params):
        updated_params = {
            'select': '*',
            'where': [],
            'group': '',
            'having': '',
            'order': [],
        }
        updated_params.update(new_params)

        return updated_params

    def save(self):
        if self._id_value():
            sql_query, attribute_values = self.update_sql(self)
        else:
            sql_query, attribute_values = self.insert_sql(self)

        try:
            data = self.execute_query(sql_query, attribute_values)
            record_id = data['last_record_id']
            if record_id is not None:
                self._attributes[self._id()] = record_id

            return True
        except:
            return False

    def update(self, **kwargs):
        self._setup_attributes(**kwargs)
        return self.save()

    def delete(self):
        if self._id_value():
            sql_query, attribute_values = self.delete_sql(self)
        else:
            return None

        try:
            self.execute_query(sql_query, attribute_values)
            return True
        except:
            return False

    @classmethod
    def create(cls, **kwargs):
        model_class = cls(**kwargs)

        if model_class.save():
            return model_class
        else:
            return None
                
    @classmethod
    def find(cls, value):
        model_class = cls()

        sql_query, query_values = model_class.find_sql(model_class, value)
        data = model_class.execute_query(sql_query, query_values)

        if data['results'][0]:
            model_class._attributes = dict(zip(data['fields'], data['results'][0]))
        else:
            return None

        return model_class

    @classmethod
    def find_by(cls, **kwargs):
        model_class = cls()

        sql_query, query_values = model_class.find_by_sql(model_class, **kwargs)
        data = model_class.execute_query(sql_query, query_values)
        if data['results'][0]:
            model_class._attributes = dict(zip(data['fields'], data['results'][0]))
        else:
            return None

        return model_class

    @classmethod
    def find_or_create_by(cls, **kwargs):
        pass

    @classmethod
    def find_or_initialize_by(cls, **kwargs):
        pass

    @classmethod
    def where(cls, *args, **kwargs):
        return Relation(cls(), Model._base_query_params({'where': [Helper.process_user_arguments(*args, **kwargs)]}))

    @classmethod
    def select(cls, fields):
        return Relation(cls(), Model._base_query_params({'select': fields}))

    @classmethod
    def order(cls, *args, **kwargs):
        return Relation(cls(), Model._base_query_params({'order': [Helper.process_user_arguments(*args, **kwargs)]}))

    @classmethod
    def all(cls):
        return Relation(cls(), {})

    @classmethod
    def limit(cls, limit, offset=0):
        return Relation(cls(), Model._base_query_params({'limit': limit, 'offset': offset}))

    @classmethod
    def last(cls, limit=1):
        return Relation(cls()).last(limit)

    @classmethod
    def first(cls, limit=1):
        return Relation(cls()).first(limit)

    @classmethod
    def count(cls):
        return Relation(cls(), Model._base_query_params({'select': 'count(*)'})).count()

    @classmethod
    def ids(cls):
        return Relation(cls(), Model._base_query_params({'select': 'id'})).ids()
