# -*- coding: utf-8 -*-


def cadastrar():
    form = SQLFORM(db.pacientes)
    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='paciente', f='paciente', args=id), client_side=True)
    return locals()


def paciente():
    id_paciente = request.args(0) or redirect(URL(c='paciente',
                                                    f='pacientes'),
                                              client_side=True)
    paciente = db(db.pacientes.id == id_paciente).select().first()
    if paciente.nascimento:
        paciente.nascimento = paciente.nascimento.strftime('%d-%m-%Y')
    return locals()


def editar_cadastro():
    id_paciente = request.args(0) or redirect(URL(c='paciente',
                                                  f='pacientes'),
                                              client_side=True)
    paciente = db(db.pacientes.id == id_paciente).select().first()
    db.pacientes.id.readable = False
    form = SQLFORM(db.pacientes, paciente, upload=URL('download'), formstyle='bootstrap3_stacked')
    if form.process().accepted:
        redirect(URL(c='paciente', f='paciente', args=id_paciente),
                 client_side=True)
    return locals()


def pacientes():
    links = [lambda row: A(SPAN('Visualizar',
                                _class='icon magnifier icon-zoom-in\
                                        glyphicon glyphicon-zoom-in'),
                           _class='button btn btn-default',
                           _href=URL(c='paciente', f='paciente',
                                     args=[row.id])),
             lambda row: A(SPAN('Editar',
                                _class='icon pen icon-pencil\
                                        glyphicon glyphicon-pencil'),
                           _class='button btn btn-default',
                           _href=URL(c='paciente', f='editar_cadastro',
                                     args=[row.id]))]
    grid = SQLFORM.grid(db.pacientes,
                        fields=[db.pacientes.nome, db.pacientes.nascimento,
                                db.pacientes.sexo],
                        csv=False, links=links, details=False, create=False,
                        editable=False, deletable=True)
    return locals()

