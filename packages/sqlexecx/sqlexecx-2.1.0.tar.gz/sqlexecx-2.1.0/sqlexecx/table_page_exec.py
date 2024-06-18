from typing import Tuple, List
from .loader import Loader
from .dialect import Dialect
from .table_support import get_table_select_sql


class TablePageExec:

    def __init__(self, table_exec, page_num, page_size):
        self.table_exec = table_exec
        self.page_num = page_num
        self.page_size = page_size

    def select(self, *columns) -> List[Tuple]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').page(1, 10).select('id', 'name', 'age')
        [(3, '张三', 20)]
        """
        sql = get_table_select_sql(self.table_exec.table, None, None, 0, *columns)
        return self.table_exec.exec.do_select_page(sql, self.page_num, self.page_size)

    def query(self, *columns) -> List[dict]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').page(1, 10).query('id', 'name', 'age')
        [{'id': 3, 'name': '张三', 'age': 20}]
        """
        sql = get_table_select_sql(self.table_exec.table, None, None, None, *columns)
        return self.table_exec.exec.do_query_page(sql, self.page_num, self.page_size)

    def load(self, *columns) -> Loader:
        """
        Select page data from table and return a Loader instance

        :return: Loader

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').page(1, 10).load('id', 'name', 'age')
        Lodder()
        """
        sql = get_table_select_sql(self.table_exec.table, None, None, None, *columns)
        sql, args = Dialect.get_page_sql_args(sql, self.page_num, self.page_size)
        return self.table_exec.exec.do_load(sql, *args)


class ColumnPageExec:

    def __init__(self, table_page_exec: TablePageExec, *columns):
        self.table_page_exec = table_page_exec
        self.columns = columns

    def select(self) -> List[Tuple]:
        """
        Select data from table and return list results(tuple).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').page(1, 10).select()
        [(3, '张三', 20)]
        """
        return self.table_page_exec.select(*self.columns)

    def query(self) -> List[dict]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').page(1, 10).query()
        [{'id': 3, 'name': '张三', 'age': 20}]
        """
        return self.table_page_exec.query(*self.columns)

    def to_df(self):
        """
        Select from table and return pandas DataFrame instance.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').page(1, 10).to_df()
        """
        return self.table_page_exec.load(*self.columns).to_df()

    def to_csv(self, file_name: str, delimiter=',', header=True, encoding='utf-8'):
        """
        Select from table and sava as a csv file.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db..table('person').columns('id', 'name', 'age').page(1, 10).to_csv('test.csv')
        """
        self.table_page_exec.load(*self.columns).to_csv(file_name, delimiter, header, encoding)

    def to_json(self, file_name: str, encoding='utf-8'):
        """
        Select from table and sava as a json file.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db..table('person').columns('id', 'name', 'age').page(1, 10).to_json('test.json')
        """
        self.table_page_exec.load(*self.columns).to_json(file_name, encoding)


class WherePageExec:

    def __init__(self, where_exec, page_num, page_size):
        self.where_exec = where_exec
        self.page_num = page_num
        self.page_size = page_size

    def select(self, *columns) -> List[Tuple]:
        """
        Select data from table and return list results(tuple).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三', age=20).page(1, 10).select('id', 'name', 'age')
        [(3, '张三', 20)]
        """
        sql, args = self.where_exec.get_select_sql_args(*columns)
        return self.where_exec.exec.do_select_page(sql, self.page_num, self.page_size, *args)

    def query(self, *columns) -> List[dict]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三', age=20).page(1, 10).query('id', 'name', 'age')
        [{'id': 3, 'name': '张三', 'age': 20}]
        """
        sql, args = self.where_exec.get_select_sql_args(*columns)
        return self.where_exec.exec.do_query_page(sql, self.page_num, self.page_size, *args)

    def load(self, *columns) -> Loader:
        """
        Select page data from table and return a Loader instance

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三', age=20).page(1, 10).load('id', 'name', 'age')
        Loader()
        """
        sql, args = self.where_exec.get_select_sql_args(*columns)
        sql, args = Dialect.get_page_sql_args(sql, self.page_num, self.page_size, *args)
        return self.where_exec.exec.do_load(sql, *args)


class ColumnWherePageExec:

    def __init__(self, where_page_exec: WherePageExec, *columns):
        self.where_page_exec = where_page_exec
        self.columns = columns

    def select(self) -> List[Tuple]:
        """
        Select data from table and return list results(tuple).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20).page(1, 10).select()
        [(3, '张三', 20)]
        """
        return self.where_page_exec.select(*self.columns)

    def query(self) -> List[dict]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20).page(1, 10).query()
        [{'id': 3, 'name': '张三', 'age': 20}]
        """
        return self.where_page_exec.query(*self.columns)

    def to_df(self):
        """
        Select from table and return pandas DataFrame instance.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db..table('person').columns('id', 'name', 'age').where(name='张三', age=20).page(1, 10).to_df()
        """
        return self.where_page_exec.load(*self.columns).to_df()

    def to_csv(self, file_name: str, delimiter=',', header=True, encoding='utf-8'):
        """
        Select from table and sava as a csv file.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db..table('person').columns('id', 'name', 'age').where(name='张三', age=20).page(1, 10).to_csv('test.csv')
        """
        self.where_page_exec.load(*self.columns).to_csv(file_name, delimiter, header, encoding)

    def to_json(self, file_name: str, encoding='utf-8'):
        """
        Select from table and sava as a json file.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db..table('person').columns('id', 'name', 'age').where(name='张三', age=20).page(1, 10).to_json('test.json')
        """
        self.where_page_exec.load(*self.columns).to_json(file_name, encoding)
