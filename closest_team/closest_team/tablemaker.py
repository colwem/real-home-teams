

class Table():

    def __init__(self, name):
        self.name = name
        self.columns = {}

    def column_for(self, name):
        if self.columns.has_key(name):
            return self.columns[name]
        self.columns[name] = Column(name)
        return self.columns[name]

    def add_primary_key(self, auto_increment=True, fmt="{name}_id"):
        pk = Column(fmt.format(name=self.name))
        pk.auto_increment = auto_increment
        pk.primary_key = True
        pk.length = 11
        self.columns[pk.name] = pk
        self.primary_key = pk

    def process(self):
        _max = max([c.count for c in self.columns.values()])
        for c in self.columns.values():
            if c.count < _max:
                c.null = True

    def to_definition(self):
        self.process()
        max_name_length = max([len(k) for k in self.columns.keys()])
        cols = self.columns.values()
        cols.sort(key=lambda x: x.name)
        s = 'CREATE TABLE `{s.name}` (\n'.format(s=self)
        s += ',\n'.join([c.to_definition(max_name_length) for c in cols])
        s += ')'
        return s


class Column():

    def __init__(self, name):
        self.name = name
        self.null = False
        self.auto_increment = False
        self.default = False
        self.length = 0
        self.float_fail = 0
        self.int_fail = 0
        self.float_success = 0
        self.int_success = 0
        self.count = 0
        self.primary_key = False

    def add_example(self, val):
        self.count += 1
        _len = len(val)

        self.set_max_len(_len)

        if not _len:
            self.null = True
            return

        if self.converts(float, val):
            self.float_success += 1
        else:
            self.float_fail += 1

        if self.converts(int, val):
            self.int_success += 1
        else:
            self.int_fail += 1

    def set_max_len(self, val):
        if val > self.length:
            self.length = val

    def converts(self, fun, val):
        try:
            fun(val)
            return True
        except ValueError:
            return False

    def process(self):
        if self.int_fail > 0 and self.float_fail > 0:
            self.field_type = 'VARCHAR'
        elif self.int_fail > 0:
            self.field_type = 'FLOAT'
        else:
            self.field_type = 'INTEGER'

    def to_definition(self, fill):
        self.process()
        name_fmt = '{' + 'name:<{fill}'.format(fill=fill) + '}'
        fmt = ' {field_type}({length})'
        if self.field_type is 'INTEGER':
            fmt = ' {field_type}'
        elif self.field_type is 'FLOAT':
            fmt = ' {field_type}'
        fmt = name_fmt + fmt
        s = fmt.format(name='`' + self.name + '`',
                       field_type=self.field_type,
                       length=self.length)
        if self.auto_increment:
            s += " AUTO_INCREMENT"
        if self.primary_key:
            s += " PRIMARY KEY"
        elif not self.null:
            s += " NOT NULL"
        elif not self.default:
            s += " DEFAULT NULL"
        return s
