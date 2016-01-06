# -*- coding: utf-8 -*-

def index():
    import sys
    from datetime import datetime
    NOW = datetime.now().strftime(format='%Y%m%d%-H%-M%-S%f')
    FILE = '/home/marcelotheodoro/teste/csv/{0}.csv'.format(NOW)
    erro = False
    try:
        db.export_to_csv_file(open(FILE, 'wb'))
    except:
        e = sys.exc_info()
        erro = True
    return locals()
