from typing import Tuple, List, Union
from .table_support import get_table_select_sql, WhereBase


class LimitExec:
	
	def __init__(self, _exec, table_name: str, order_by: str, limit: Union[int, Tuple[int], List[int]]):
		self.exec = _exec
		self.table = table_name
		self.order_by = order_by
		self.limit = limit
	
	def select(self, *columns) -> List[Tuple]:
		"""
		Select data from table and return list results(tuple).

		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').limit(1).select('id', 'name', 'age')
		[(3, '张三', 20)]
		"""
		sql = get_table_select_sql(self.table, None, self.order_by, self.limit, *columns)
		if isinstance(self.limit, int):
			return self.exec.do_select(sql, self.limit)
		return self.exec.do_select(sql, *self.limit)
	
	def query(self, *columns) -> List[Tuple]:
		"""
		Select data from table and return list results(dict).

		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').limit(1).query('id', 'name', 'age')
		[{'id': 3, 'name': '张三', 'age': 20}]
		"""
		sql = get_table_select_sql(self.table, None, self.order_by, self.limit, *columns)
		if isinstance(self.limit, int):
			return self.exec.do_query(sql, self.limit)
		else:
			return self.exec.do_query(sql, *self.limit)


class ColumnLimitExec:
	
	def __init__(self, limit_exec: LimitExec, *columns):
		self.limit_exec = limit_exec
		self.columns = columns
	
	def select(self) -> List[Tuple]:
		"""
		Select data from table and return list results(tuple).

		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').columns('id', 'name', 'age').limit(1).select()
		[(3, '张三', 20)]
		"""
		return self.limit_exec.select(*self.columns)
	
	def query(self) -> List[Tuple]:
		"""
		Select data from table and return list results(dict).

		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').columns('id', 'name', 'age').limit(1).query()
		[{'id': 3, 'name': '张三', 'age': 20}]
		"""
		return self.limit_exec.query(*self.columns)
	
	
class WhereLimitExec(WhereBase):

	def __init__(self, _exec, table_name: str, order_by: str, limit: Union[int, Tuple[int], List[int]], **kwargs):
		super().__init__(_exec, table_name, order_by, **kwargs)
		self._limit = limit
		
		
class ColumnWhereLimitExec:
	
	def __init__(self, where_limit_exec, *columns):
		self.where_limit_exec = where_limit_exec
		self.columns = columns
	
	def select(self) -> List[Tuple]:
		"""
		Select data from table and return list results(tuple).

		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20).limit(1).select()
		[(3, '张三', 20)]
		"""
		return self.where_limit_exec.select(*self.columns)

	def query(self) -> List[dict]:
		"""
		Select data from table and return list results(dict).
		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20).limit(1).query()
		[{'id': 3, 'name': '张三', 'age': 20}]
		"""
		return self.where_limit_exec.query(*self.columns)
