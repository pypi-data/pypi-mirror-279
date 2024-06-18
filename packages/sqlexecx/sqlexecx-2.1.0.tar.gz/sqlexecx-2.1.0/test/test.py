from typing import Collection, Sequence, Union

t = ('1', '2')
print(isinstance(t, Collection), isinstance(t, Sequence))
# True True
l = ['1', '2']
print(isinstance(l, Collection), isinstance(l, Sequence))
# True True
s = set(l)
print(isinstance(s, Collection), isinstance(s, Sequence))
# True False
s = 'hello'
print(isinstance(s, Collection), isinstance(s, Sequence))
# True True
print('='*50)


def get_dialect_str(src: Union[str, Collection[str]]):
    return src.strip() if isinstance(src, str) else ','.join([s.strip() for s in src])


def _dialect_str(src: str):
    assert isinstance(src, str), 'source must be a string.'
    if ',' in src:
        return ','.join(['`{}`'.format(s.strip()) for s in src.split(',')])
    elif '(' in src:
        return src.strip()
    else:
        return '`{}`'.format(src.strip())


def get_mysql_dialect_str(src: Union[str, Collection[str]]):
    assert src, 'src string is required.'
    if isinstance(src, str):
        return _dialect_str(src)
    return ','.join([_dialect_str(arg) for arg in src])


if __name__ == '__main__':
    # names = 'person'
    # names = ['id', 'name, age']
    # print(get_dialect_str(names))
    # print(get_mysql_dialect_str(names))

    sql = """
    SELECT id, strftime('%Y-%m-%d %H:%M:%S' , create_time, 'localtime')
      FROM history where user_id = ? and query_type = ? and name like 'lisi%' and name like '%zhangsan' order by id desc
    """.strip()
    
    # import re
    # # NAMED_REGEX = r':[a-z|A-Z|\d][\w|\d]*'
    # NAMED_REGEX = r"like\s+'[\w|\d|%]*'"
    # pattern = re.compile(NAMED_REGEX, re.I)
    # for r in re.finditer(pattern, sql):
    #     old = r.group()
    #     new = old.replace('%', '%%').replace('%%%%', '%%')
    #     print(old, new)
    #     sql = sql.replace(old, new, 1)
        # print(r)
        # print(r.span())
        # print(r.group())
    # print(re.search(pattern, sql))
    # print(sql)

    # from sqlexecx import Engine, Dialect
    # Dialect.init(Engine.MYSQL)
    # print(Dialect.before_execute(sql))
    
    import sqlexecx as db
    db.init('/Users/summy/project/python/streamlit_clip_annoy/data/db.sqlite3', show_sql=True)
    print(db.table('history').columns("id, strftime('%Y-%m-%d %H:%M:%S', create_time, 'localtime') as create_time").query())
    