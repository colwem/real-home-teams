import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from models_two import database, PlayerSeasons
from itertools import izip_longest


def load_json(fn='playerseasons.json'):
    with open(fn, 'r') as fd:
        for jsonline in fd:
            yield json.loads(jsonline)


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def insert_objs(db, model, objs):
    with db.transaction():
        rows = []
        for row in objs:
            if row:
                for k, v in row.items():
                    if 'rushing_and_receiving' in k:
                        old_k = k
                        k = k.replace('rushing_and_receiving', 'receiving_and_rushing')
                        row[k] = row[old_k]
                        del row[old_k]
                    if not v:
                        del row[k]
            try:
                model.insert(**row).execute()
            except Exception, e:
                import pdb; pdb.set_trace()


def to_s(cols):
    s = ''
    l = cols.keys()
    l.sort()
    for k in l:
        s += k + '\n'
        for k, v in cols[k].items():
            s += "\t{}: {}\n".format(k, v)

    return s


def main():
    import sys

    fn = sys.argv[1]
    insert_objs(database, PlayerSeasons, load_json(fn))

    # table = Table('player_seasons')
    # for d in load_json(fn=fn):
        # for k, v in d.items():
            # col = table.column_for(k)
            # col.add_example(v)

    # table.add_primary_key()
    # print table.to_definition()

if __name__ == '__main__':
    main()
