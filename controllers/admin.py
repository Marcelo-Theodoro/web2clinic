# -*- coding: utf-8 -*-


@auth.requires_login()
def index():
    return locals()


@auth.requires_login()
def medicamentos():
    grid = SQLFORM.grid(db.lista_medicamentos,
                        fields=[db.lista_medicamentos.nome,
                                db.lista_medicamentos.texto,
                                db.lista_medicamentos.fichas],
                        editable=False,
                        csv=False,
                        paginate=10)
    return locals()


@auth.requires_login()
def exames():
    grid = SQLFORM.grid(db.lista_exames,
                        fields=[db.lista_exames.nome,
                                db.lista_exames.fichas],
                        editable=False,
                        csv=False,
                        paginate=10)
    return locals()
