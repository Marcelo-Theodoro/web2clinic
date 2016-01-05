# -*- coding: utf-8 -*-

@auth.requires_login()
def gerar_exame():
    id_consulta = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    consulta = db(db.consultas.id == id_consulta).select().first()
    if not consulta:
        raise HTTP(404)
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    if not paciente:
        raise HTTP(404)
    lista_exames = db(db.lista_exames).select()
    for exame in lista_exames:
        if exame.fichas:
            exame.fichas = exame.fichas.replace('|', ' ')
        else:
            exame.fichas = ''
    form = SQLFORM(db.exames)
    form.vars.id_paciente = paciente.id
    form.vars.id_consulta = consulta.id
    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='exame', f='exame', args=id),
                 client_side=True)
    return locals()


@auth.requires_login()
def exame():
    id_exame = request.args(0) or redirect(URL(c='consulta',
                                                    f='todas_consultas'))
    exame = db(db.exames.id == id_exame).select().first()
    if not exame:
        raise HTTP(404)
    paciente = db(db.pacientes.id == exame.id_paciente).select().first()
    if not paciente:
        raise HTTP(404)
    return locals()


@auth.requires_login()
def exames():
    id_paciente = request.args(0)
    if id_paciente:
        paciente = db(db.pacientes.id == id_paciente).select().first()
        if not paciente:
            raise HTTP(404)
    links = [lambda row: A(SPAN('Visualizar',
                                _class='icon magnifier icon-zoom-in\
                                        glyphicon glyphicon-zoom-in'),
                           _class='button btn btn-default',
                           _href=URL(c='exame', f='exame',
                                     args=[row.id]))]
    db.exames.id_paciente.readable = True
    haders = {'exames.id_paciente': 'Paciente',
              'exames.data_criacao': 'Data de criação'}
    grid = SQLFORM.grid(db.exames.id_paciente == paciente.id
                        if id_paciente else db.exames,
                        fields=[db.exames.id_paciente,
                                db.exames.data_criacao],
                        args=request.args[:1],
                        csv=False,
                        user_signature=False,
                        headers=haders,
                        details=False,
                        links=links,
                        editable=False,
                        deletable=False,
                        create=False,
                        paginate=10)
    return locals()
