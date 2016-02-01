# -*- coding: utf-8 -*-

@auth.requires_login()
def gerar_atestado():
    id_consulta = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    consulta = db(db.consultas.id == id_consulta).select().first()
    if not consulta:
        raise HTTP(404)
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    form = SQLFORM(db.atestados)
    texto_atestado = '''
    Atesto para os devidos fins que {0} esteve sob meus cuidados, no dia {1} devendo:
    ( ) Retornar ao trabalho
    \n\n
    ( ) Permanecer afastada no dia de hoje
    \n\n
    ( ) Permanecer afastada do dia __/__/_____ ao dia __/__/_____
    \n\n
    CID:
    '''.format(paciente.nome, request.now.strftime('%d/%m/%Y'))
    form.vars.atestado = texto_atestado
    form.vars.id_paciente = paciente.id
    form.vars.id_consulta = consulta.id
    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='atestado', f='atestado', args=id), client_side=True)
    return locals()


@auth.requires_login()
def atestado():
    id_atestado = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    atestado = db(db.atestados.id == id_atestado).select().first()
    paciente = db(db.pacientes.id == atestado.id_paciente).select()
    return locals()


@auth.requires_login()
def atestados():
    id_paciente = request.args(0)
    if id_paciente:
        paciente = db(db.pacientes.id == id_paciente).select().first()
        if not paciente:
            raise HTTP(404)
    db.atestados.id_paciente.readable = True
    haders = {'atestados.id_paciente': 'Paciente'}
    links = [lambda row: A(SPAN('Visualizar',
                                _class='icon magnifier icon-zoom-in\
                                        glyphicon glyphicon-zoom-in'),
                           _class='button btn btn-default',
                           _href=URL(c='atestado', f='atestado.html',
                                     args=[row.id]))]
    grid = SQLFORM.grid(db.atestados.id_paciente == paciente.id
                        if id_paciente else db.atestados,
                        fields=[db.atestados.id_paciente,
                                db.atestados.data_criacao],
                        args=request.args[:1],
                        csv=False,
                        user_signature=False,
                        headers=haders,
                        details=False,
                        links=links,
                        editable=False,
                        deletable=False,
                        create=False,
                        searchable=False,
                        paginate=10)
    return locals()
