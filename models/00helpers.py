# -*- coding: utf-8 -*-

def ChecaFichaValida(ficha):
    import re
    if not ficha:
        raise HTTP(404)
    if re.match('db.ficha_([a-z]+|_+[a-z]+)|db.retorno', ficha):
        return True
    return False
