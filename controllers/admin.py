# -*- coding: utf-8 -*-


@auth.requires_login()
def index():
    return locals()


@auth.requires_login()
def cadastrar_medicamento():
    form = SQLFORM(db.lista_medicamentos)
    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='admin', f='ver_medicamento', args=id), client_side=True)
    return locals()


@auth.requires_login()
def editar_medicamento():
    id_medicamento = request.args(0) or redirect(URL(c='admin',
                                                     f='medicamentos'))
    medicamento = db(db.lista_medicamentos.id == id_medicamento).select().first()
    if not medicamento:
        raise HTTP(404)
    if medicamento.fichas:
        medicamento.fichas = medicamento.fichas.split('|')
    else:
        medicamento.fichas = []
    db.lista_medicamentos.id.readable = False
    form = SQLFORM(db.lista_medicamentos, record=medicamento)
    form.vars.fichas = [i for i in medicamento.fichas]
    if form.process().accepted:
        id = medicamento.id
        redirect(URL(c='admin', f='ver_medicamento', args=id), client_side=True)
    return locals()


@auth.requires_login()
def ver_medicamento():
    id_medicamento = request.args(0) or redirect(URL(c='admin',
                                                     f='medicamentos'))
    medicamentos = db(db.lista_medicamentos.id == id_medicamento).select()
    if not medicamentos:
        raise HTTP(404)
    for medicamento in medicamentos:
        if medicamento.fichas:
            if len(filter(None, medicamento.fichas.split('|'))) == 9:
                medicamento.fichas = 'Todas as fichas'
            else:
                medicamento.fichas = medicamento.fichas.replace('|', ' ')
        else:
            medicamento.fichas = 'Todas as fichas'

    return locals()



@auth.requires_login()
def medicamentos():
    links = [lambda row: A(SPAN('Visualizar',
                                _class='icon magnifier icon-zoom-in\
                                        glyphicon glyphicon-zoom-in'),
                           _class='button btn btn-default',
                           _href=URL(c='admin', f='ver_medicamento',
                                     args=row.id)),
             lambda row: A(SPAN('Editar',
                                _class='icon pen icon-pencil\
                                        glyphicon glyphicon-pencil'),
                           _class='button btn btn-default',
                           _href=URL(c='admin', f='editar_medicamento',
                                     args=row.id))]

    grid = SQLFORM.grid(db.lista_medicamentos,
                        fields=[db.lista_medicamentos.nome,
                                db.lista_medicamentos.texto],
                        links=links,
                        editable=False,
                        csv=False,
                        create=False,
                        details=False,
                        paginate=10)
    return locals()


@auth.requires_login()
def cadastrar_exame():
    form = SQLFORM(db.lista_exames)
    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='admin', f='ver_exame', args=id), client_side=True)
    return locals()


@auth.requires_login()
def editar_exame():
    id_exame = request.args(0) or redirect(URL(c='admin',
                                               f='exames'))
    exame = db(db.lista_exames.id == id_exame).select().first()
    if not exame:
        raise HTTP(404)
    if exame.fichas:
        exame.fichas = exame.fichas.split('|')
    else:
        exame.fichas = []
    db.lista_exames.id.readable = False
    form = SQLFORM(db.lista_exames, record=exame)
    form.vars.fichas = [i for i in exame.fichas]
    if form.process().accepted:
        id = exame.id
        redirect(URL(c='admin', f='ver_exame', args=id), client_side=True)
    return locals()


@auth.requires_login()
def ver_exame():
    id_exame = request.args(0) or redirect(URL(c='admin',
                                               f='exames'))
    exame = db(db.lista_exames.id == id_exame).select()
    if not exame:
        raise HTTP(404)
    return locals()



@auth.requires_login()
def exames():
    links = [lambda row: A(SPAN('Visualizar',
                                _class='icon magnifier icon-zoom-in\
                                        glyphicon glyphicon-zoom-in'),
                           _class='button btn btn-default',
                           _href=URL(c='admin', f='ver_exame',
                                     args=row.id)),
             lambda row: A(SPAN('Editar',
                                _class='icon pen icon-pencil\
                                        glyphicon glyphicon-pencil'),
                           _class='button btn btn-default',
                           _href=URL(c='admin', f='editar_exame',
                                     args=row.id))]

    grid = SQLFORM.grid(db.lista_exames,
                        fields=[db.lista_exames.nome],
                        links=links,
                        editable=False,
                        csv=False,
                        create=False,
                        details=False,
                        paginate=10)
    return locals()
