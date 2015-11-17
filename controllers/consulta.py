# -*- coding: utf-8 -*-

def consulta():
    tipo_consulta = request.args(0) or redirect(URL(c='consulta',
                                                    f='todas_consultas'))
    # TODO: gambiarra.start()
    if request.vars['agendamento'] == 'True':
        id_agendamento = request.args(1) or redirect(URL(c='consulta',
                                                         f='todas_consultas'))
        agendamento = db(db.agendamentos.id == id_agendamento).select().first()
        id_paciente = agendamento.id_paciente
        paciente = db(db.pacientes.id == id_paciente).select().first()
        paciente.nascimento = paciente.nascimento.strftime('%d-%m-%Y')
    elif request.vars['agendamento'] == 'False':
        id_paciente = request.args(1) or redirect(URL(c='consulta',
                                                      f='todas_consultas'))
        paciente = db(db.pacientes.id == id_paciente).select().first()
    else:
        raise HTTP(404)
    # TODO: gambiarra.stop()
    try:
        tipo_consulta = [i for i in tipos_consultas
                         if i['form'] == tipo_consulta][0]
    except IndexError:
        raise HTTP(404)
    form = SQLFORM(tipo_consulta['base'], formstyle='bootstrap3_stacked')
    response.view = tipo_consulta['view_form']
    form.vars.id_paciente = paciente.id
    if form.process().accepted:
        id_form = form.vars.id
        id_insert = db.consultas.insert(id_paciente=paciente.id,
                                        dia = request.now,
                                        hora_inicio=request.now,
                                        hora_fim=request.now,
                                        tipo_consulta=tipo_consulta['form'],
                                        id_form=id_form)
        if not id_insert:
            raise HTTP(500)
        redirect(URL(c='consulta', f='ver_consulta', args=id_insert),
                 client_side=True)
    return locals()


def consultas():
    id_paciente = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    paciente = db(db.pacientes.id == id_paciente).select().first()
    consultas = db(db.consultas.id_paciente == id_paciente).select()
    for consulta in consultas:
        consulta.tipo_consulta = [i['label'] for i in tipos_consultas
                                  if consulta.tipo_consulta == i['form']][0]
    return locals()


def nova_consulta():
    links = [lambda row: A('Iniciar consulta', _class='button btn\
                                                       btn-default',
                           _href=URL(c='consulta', f='consultar',
                                     args=[row.id]))]
    grid = SQLFORM.grid(db.pacientes,
                        fields=[db.pacientes.nome, db.pacientes.cpf],
                        links=links, csv=False, editable=False,
                        deletable=False, details=False, create=False)
    return locals()


def consultar():
    id_paciente = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    paciente = db(db.pacientes.id == id_paciente).select().first()
    form = SQLFORM.factory(Field('tipo_consulta',
                                 requires=IS_IN_SET([i['label'] for i in
                                                    tipos_consultas])),
                                 formstyle='bootstrap3_stacked')
    if form.process().accepted:
        tipo_consulta = form.vars.tipo_consulta
        tipo_consulta_form = [i['form'] for i in tipos_consultas
                              if tipo_consulta == i['label']][0]
        redirect(URL(c='consulta', f='consulta',
                 args=[tipo_consulta_form, id_paciente],
                 vars=dict(agendamento=False)), client_side=True)
    return locals()


def todas_consultas():
    links = [lambda row: A('Ver consulta', _class='button btn btn-default',
                           _href=URL(c='consulta', f='ver_consulta',
                                     args=[row.id]))]
    haders = {'consultas.id_paciente': 'Paciente'}
    db.consultas.id_paciente.readable = True
    db.consultas.tipo_consulta.represent = lambda value, row: '{0}'.\
                                           format([i['label']
                                                   for i in tipos_consultas
                                                   if value == i['form']][0])
    form = SQLFORM.grid(db.consultas,
                        fields=[db.consultas.id_paciente,
                                db.consultas.tipo_consulta,
                                db.consultas.hora_fim],
                        csv=False, editable=False, deletable=False,
                        details=False, create=False, links=links,
                        headers=haders)
    return locals()


def ver_consulta():
    id_consulta = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    consulta = db(db.consultas.id == id_consulta).select().first()
    consulta.tipo_consulta = [i['label'] for i in tipos_consultas
                              if consulta.tipo_consulta == i['form']][0]
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    return locals()


def editar_consulta():
    id_consulta = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    return locals()

def apagar_consulta():
    id_consulta = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    consulta = db(db.consultas.id == id_consulta).select().first()
    if not consulta:
        raise HTTP(404)
    form = SQLFORM.factory()
    if form.process().accepted:
        db(db.consultas.id == consulta.id).delete()
        redirect(URL(c='consulta', f='todas_consultas'))
    return locals()



