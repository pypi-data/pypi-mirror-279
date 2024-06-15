from typing import Tuple, List, Union
from .table_support import get_table_select_sql
from .table_support import WhereBase
from .table_limit_exec import LimitExec, ColumnLimitExec, WhereLimitExec, ColumnWhereLimitExec


class OrderByExec:
	
	def __init__(self, _exec, table_name: str, order_by: str):
		self.exec = _exec
		self.table = table_name
		self.order_by = order_by

	def select(self, *columns) -> List[Tuple]:
		"""
		Select data from table and return list results(tuple).
		
		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').order_by('id DESC, name ASC').select('id', 'name', 'age')
		[(3, '张三', 20)]
		"""
		sql = get_table_select_sql(self.table, None, self.order_by, None, *columns)
		return self.exec.do_select(sql)
	
	def query(self, *columns) -> List[dict]:
		"""
		Select data from table and return list results(dict).
		
		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').order_by('id DESC, name ASC').query('id', 'name', 'age')
		[{'id': 3, 'name': '张三', 'age': 20}]
		"""
		sql = get_table_select_sql(self.table, None, self.order_by, None, *columns)
		return self.exec.do_query(sql)

	def limit(self, limit: Union[int, Tuple[int], List[int]] = 10) -> LimitExec:
		"""
		Get a LimitExec instance
		
		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').order_by('id DESC, name ASC').limit(10)
		LimitExec()
		"""
		return LimitExec(self.exec, self.table, self.order_by, limit)


class ColumnOrderByExec:
	
	def __init__(self, order_by_exec, *columns):
		self.order_by_exec = order_by_exec
		self.columns = columns

	def select(self) -> List[Tuple]:
		"""
		Select data from table and return list results(tuple).
	
		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').columns('id', 'name', 'age').select()
		[(3, '张三', 20)]
		"""
		return self.order_by_exec.select(*self.columns)

	def query(self) -> List[dict]:
		"""
		Select data from table and return list results(dict).
		
		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').columns('id', 'name', 'age').query()
		[{'id': 3, 'name': '张三', 'age': 20}]
		"""
		return self.order_by_exec.query(*self.columns)

	def limit(self, limit: Union[int, Tuple[int], List[int]] = 10) -> ColumnLimitExec:
		"""
		Get a ColumnLimitExec instance
		
		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').columns('id', 'name', 'age').order_by('id DESC, name ASC').limit(10)
		ColumnLimitExec()
		"""
		return ColumnLimitExec(
			LimitExec(self.order_by_exec.exec, self.order_by_exec.table, self.order_by_exec.order_by, limit),
			*self.columns
		)


class WhereOrderByExec(WhereBase):
	
	def __init__(self, _exec, table_name: str, order_by: str, **kwargs):
		super().__init__(_exec, table_name, order_by, **kwargs)
	
	def limit(self, limit: Union[int, Tuple[int], List[int]] = 10) -> LimitExec:
		"""
		Get a WhereLimitExec instance

		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').where(name='张三', age=20).order_by('id DESC, name ASC').limit(10)
		WhereLimitExec()
		"""
		return WhereLimitExec(self.exec, self.table, self._order_by, limit, **self.where_condition)
	
	
class ColumnWhereOrderByExec:
	
	def __init__(self, where_order_by_exec, *columns):
		self.where_order_by_exec = where_order_by_exec
		self.columns = columns
	
	def select(self) -> List[Tuple]:
		"""
		Select data from table and return list results(tuple).

		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20).order_by('id DESC, name ASC').select()
		[(3, '张三', 20)]
		"""
		return self.where_order_by_exec.select(*self.columns)

	def query(self) -> List[dict]:
		"""
		Select data from table and return list results(dict).
		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20).order_by('id DESC, name ASC').query()
		[{'id': 3, 'name': '张三', 'age': 20}]
		"""
		return self.where_order_by_exec.query(*self.columns)

	def limit(self, limit: Union[int, Tuple[int], List[int]] = 10) -> ColumnWhereLimitExec:
		"""
		Get a ColumnWhereLimitExec instance
		
		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20).order_by('id DESC, name ASC').limit(10)
		ColumnWhereLimitExec()
		"""
		return ColumnWhereLimitExec(
			WhereLimitExec(self.where_order_by_exec.exec, self.where_order_by_exec.table, self.where_order_by_exec._order_by, limit),
			*self.columns
		)
