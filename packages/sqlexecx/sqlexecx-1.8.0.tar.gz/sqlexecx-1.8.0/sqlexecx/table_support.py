from typing import Union, List, Tuple, Sequence

from .dialect import Dialect
from .constant import LIMIT_1


def get_table_select_sql(table_name: str, where: str, order_by: str, limit: Union[int, Tuple[int], List[int]], *columns):
	columns = Dialect.get_dialect_str(columns) if columns else Dialect.get_table_columns(table_name)
	table_name = Dialect.get_dialect_str(table_name)
	if where:
		sql = 'SELECT {} FROM {} {}'.format(columns, table_name, where)
	else:
		sql = 'SELECT {} FROM {}'.format(columns, table_name)
	
	if order_by:
		sql = sql + ' ORDER BY {}'.format(order_by)
	
	if limit:
		if isinstance(limit, int):
			return sql + ' LIMIT ?'
		elif isinstance(limit, (Tuple, List)) and len(limit) == 2:
			return Dialect.limit_offset_sql(sql)
		else:
			raise ValueError("The type of the parameter 'limit' must be 'int' or tuple, list, and it length is 2.")
	
	return sql


def get_condition_arg(k: str, v: object):
	if k.endswith("__eq"):
		return "{} = ?".format(Dialect.get_dialect_str(k[:-4])), v
	if k.endswith("__ne"):
		return "{} != ?".format(Dialect.get_dialect_str(k[:-4])), v
	if k.endswith("__gt"):
		return "{} > ?".format(Dialect.get_dialect_str(k[:-4])), v
	if k.endswith("__lt"):
		return "{} < ?".format(Dialect.get_dialect_str(k[:-4])), v
	if k.endswith("__ge"):
		return "{} >= ?".format(Dialect.get_dialect_str(k[:-4])), v
	if k.endswith("__gte"):
		return "{} >= ?".format(Dialect.get_dialect_str(k[:-5])), v
	if k.endswith("__le"):
		return "{} <= ?".format(Dialect.get_dialect_str(k[:-4])), v
	if k.endswith("__lte"):
		return "{} <= ?".format(Dialect.get_dialect_str(k[:-5])), v
	if k.endswith("__isnull"):
		return "{} is {}".format(Dialect.get_dialect_str(k[:-8]), 'null' if v else 'not null'), None
	if k.endswith("__in") and isinstance(v, Sequence) and not isinstance(v, str):
		return "{} in({})".format(Dialect.get_dialect_str(k[:-4]), ','.join(['?' for _ in v])), v
	if k.endswith("__in"):
		return "{} in({})".format(Dialect.get_dialect_str(k[:-4]), '?'), v
	if k.endswith("__not_in") and isinstance(v, Sequence) and not isinstance(v, str):
		return "{} not in({})".format(Dialect.get_dialect_str(k[:-8]), ','.join(['?' for _ in v])), v
	if k.endswith("__not_in"):
		return "{} not in({})".format(Dialect.get_dialect_str(k[:-8]), '?'), v
	if k.endswith("__like"):
		return "{} like ?".format(Dialect.get_dialect_str(k[:-6])), '%{}%'.format(v)
	if k.endswith("__startswith"):
		return "{} like ?".format(Dialect.get_dialect_str(k[:-12])), '{}%'.format(v)
	if k.endswith("__endswith"):
		return "{} like ?".format(Dialect.get_dialect_str(k[:-10])), '%{}'.format(v)
	if k.endswith("__contains"):
		return "{} like ?".format(Dialect.get_dialect_str(k[:-10])), '%{}%'.format(v)
	if k.endswith("__range") and isinstance(v, Sequence) and 2 == len(v) and not isinstance(v, str):
		col = k[:-7]
		return "{} >= ? and {} <= ?".format(Dialect.get_dialect_str(col), Dialect.get_dialect_str(col)), v
	if k.endswith("__between") and isinstance(v, Sequence) and 2 == len(v) and not isinstance(v, str):
		return "{} between ? and ?".format(Dialect.get_dialect_str(k[:-9])), v
	if k.endswith("__range") or k.endswith("__between"):
		return ValueError("Must is instance of Sequence with length 2 when use range or between statement")
	
	return "{} = ?".format(Dialect.get_dialect_str(k)), v


def get_where_arg_limit(**kwargs):
	where, args, limit = '', [], 0
	if 'limit' in kwargs:
		limit = kwargs.pop('limit')
	
	if kwargs:
		conditions, tmp_args = zip(*[get_condition_arg(k, v) for k, v in kwargs.items()])
		tmp_args = [arg for arg in tmp_args if arg is not None]
		
		for arg in tmp_args:
			if arg is not None:
				if isinstance(arg, Sequence) and not isinstance(arg, str):
					args.extend(arg)
				else:
					args.append(arg)
		where = 'WHERE {}'.format(' and '.join(conditions))
	
	return where, args, limit


class WhereBase:

	def __init__(self, _exec, table_name: str, order_by: str, **kwargs):
		self.exec = _exec
		self.table = table_name
		self._order_by = order_by
		self.where_condition = kwargs
		self._limit = None
	
	def select(self, *columns) -> List[Tuple]:
		"""
		Select data from table and return list results(tuple).

		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').where(name='张三', age=20).select('id', 'name', 'age')
		[(3, '张三', 20)]
		"""
		sql, args = self.get_select_sql_args(*columns)
		return self.exec.do_select(sql, *args)
	
	def query(self, *columns) -> List[dict]:
		"""
		Select data from table and return list results(tuple).

		Examples
		--------
		>>> import sqlexecx as db
		>>> db.table('person').where(name='张三', age=20).query('id', 'name', 'age')
		[{'id': 3, 'name': '张三', 'age': 20}]
		"""
		sql, args = self.get_select_sql_args(*columns)
		return self.exec.do_query(sql, *args)
	
	def get_select_sql_args(self, *columns):
		where, args, limit = get_where_arg_limit(**self.where_condition)
		limit = self._limit or limit
		sql = get_table_select_sql(self.table, where, self._order_by, limit, *columns)
		if limit:
			if isinstance(limit, int):
				args = [*args, limit]
			else:
				args = [*args, *limit]
		return sql, args
	
	def get_select_one_sql_args(self, *columns):
		where, args, _ = get_where_arg_limit(**self.where_condition)
		sql = get_table_select_sql(self.table, where, self._order_by, LIMIT_1, *columns)
		return sql, args
