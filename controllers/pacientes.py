# -*- coding: utf-8 -*-


def buscar_paciente(id):
    paciente = db(db.pacientes.id == id).select().first()
    # paciente.nascimento = paciente.nascimento.strftime('%d-%m-%Y')
    return paciente


def buscar_agendamento(id):
    agendamento = db(db.agendamentos.id == id).select().first()
    # agendamento.dia = agendamento.dia.strftime('%d-%m-%Y')
    return agendamento


def buscar_consulta(id):
    consulta = db(db.consultas.id == id).select().first()
    return consulta


def buscar_consulta_paciente(id):
    consulta = db(db.consultas.id_paciente == id).select()
    return consulta


def buscar(base, id):
    bases = ['paciente',
            'agendamento',
            'consulta',
            'consulta_paciente']
    if base not in bases:
        raise HTTP(403)
    try:
        if base == 'paciente':
            dados = buscar_paciente(id)
        elif base == 'agendamento':
            dados = buscar_agendamento(id)
        elif base == 'consulta':
            dados = buscar_consulta(id)
        elif base == 'consulta_paciente':
            dados = buscar_consulta_paciente(id)
        else:
            raise HTTP(404)

        if not dados:
            raise HTTP(404)
    except ValueError:
        raise HTTP(404)
    return dados


def index():
    total_pacientes = db(db.pacientes).count()
    total_agendamentos = db(db.agendamentos).count()
    total_consultas = db(db.consultas).count()
    itens = [i['form'] for i in tipos_consultas]
    lista = []
    for item in itens:
        qtd_consultas = len(db(db.consultas.tipo_consulta == item).select())
        if qtd_consultas:
            label = [i['label'] for i in tipos_consultas
                     if item == i['form']][0]
            lista.append({'label': label, 'qtd': qtd_consultas})
    return locals()


def cadastrar():
    form = SQLFORM(db.pacientes)
    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='pacientes', f='paciente', args=id), client_side=True)
    return locals()


def paciente():
    id_paciente = request.args(0) or redirect(URL(c='pacientes',
                                                    f='pacientes'),
                                              client_side=True)
    paciente = buscar('paciente', id_paciente)
    paciente.nascimento = paciente.nascimento.strftime('%d-%m-%Y')
    return locals()


def editar_cadastro():
    id_paciente = request.args(0) or redirect(URL(c='pacientes',
                                                  f='pacientes'),
                                              client_side=True)
    paciente = buscar('paciente', id_paciente)
    db.pacientes.id.readable = False
    form = SQLFORM(db.pacientes, paciente, upload=URL('download'))
    if form.process().accepted:
        redirect(URL(c='pacientes', f='paciente', args=id_paciente),
                 client_side=True)
    return locals()


def pacientes():
    links = [lambda row: A(SPAN('Visualizar',
                                _class='icon magnifier icon-zoom-in\
                                        glyphicon glyphicon-zoom-in'),
                           _class='button btn btn-default',
                           _href=URL(c='pacientes', f='paciente',
                                     args=[row.id])),
             lambda row: A(SPAN('Editar',
                                _class='icon pen icon-pencil\
                                        glyphicon glyphicon-pencil'),
                           _class='button btn btn-default',
                           _href=URL(c='pacientes', f='editar_cadastro',
                                     args=[row.id]))]
    grid = SQLFORM.grid(db.pacientes,
                        fields=[db.pacientes.nome, db.pacientes.nascimento,
                                db.pacientes.sexo],
                        csv=False, links=links, details=False, create=False,
                        editable=False, deletable=True)
    return locals()


def novo_agendamento():
    links = [lambda row: A(SPAN('Agendar',
                                _class='icon plus icon-plus\
                                        glyphicon glyphicon-plus'),
                           _class='button btn btn-default',
                           _href=URL(c='pacientes', f='agendar',
                                     args=[row.id]))]
    grid = SQLFORM.grid(db.pacientes,
                        fields=[db.pacientes.nome, db.pacientes.cpf],
                        links=links, csv=False, editable=False,
                        deletable=False, details=False, create=False)
    return locals()


def agendar():
    id_paciente = request.args(0) or redirect(URL(c='pacientes',
                                                  f='novo_agendamento'),
                                              client_side=True)
    paciente = buscar('paciente', id_paciente)
    form = SQLFORM(db.agendamentos)
    form.vars.id_paciente = id_paciente
    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='pacientes', f='agendamento', args=id),
                 client_side=True)
    return locals()


def editar_agendamento():
    id_agendamento = request.args(0) or redirect(URL(c='pacientes',
                                                     f='agendamentos'),
                                                 client_side=True)
    agendamento = buscar('agendamento', id_agendamento)
    db.agendamentos.id.readable = False
    form = SQLFORM(db.agendamentos, agendamento)
    if form.process().accepted:
        redirect(URL(c='pacientes', f='agendamento', args=id_agendamento),
                 client_side=True)
    return locals()


def agendamento():
    id_agendamento = request.args(0) or redirect(URL(c='pacientes',
                                                     f='agendamentos'),
                                                 client_side=True)
    agendamento = buscar('agendamento', id_agendamento)
    agendamento.dia = agendamento.dia.strftime('%d-%m-%Y')
    id_paciente = agendamento.id_paciente
    paciente = buscar('paciente', id_paciente)
    form = SQLFORM.factory(Field('tipo_consulta',
                                 requires=IS_IN_SET([i['label']
                                                    for i in tipos_consultas])),
                                 formstyle='bootstrap3_stacked')
    if form.process().accepted:
        tipo_consulta = form.vars.tipo_consulta
        tipo_consulta = [i['form'] for i in tipos_consultas
                         if i['label'] == tipo_consulta][0]
        redirect(URL(c='pacientes', f='consulta',
                     args=[tipo_consulta, id_agendamento],
                     vars=dict(agendamento=True)),
                 client_side=True)
    return locals()


def apagar_agendamento():
    id_agendamento = request.args(0) or redirect(URL(c='pacientes',
                                                     f='agendamentos'),
                                                 client_side=True)
    agendamento = buscar('agendamento', id_agendamento)
    agendamento.dia = agendamento.dia.strftime('%d-%m-%Y')
    id_paciente = agendamento.id_paciente
    paciente = buscar('paciente', id_paciente)
    form = SQLFORM.factory()
    if form.process().accepted:
        db(db.agendamentos.id == id_agendamento).delete()
        redirect(URL(c='pacientes', f='agendamentos'), client_side=True)
    return locals()


def agendamentos():
    agendamentos = db(db.agendamentos).select()
    lista = []
    for agendamento in agendamentos:
        paciente = buscar('paciente', agendamento.id_paciente)
        agendamento.dia = agendamento.dia.strftime('%d-%m-%Y')
        lista.append(dict({'dia': agendamento.dia,
                           'hora_inicio': agendamento.hora_inicio,
                           'hora_fim': agendamento.hora_fim,
                           'id_paciente': paciente.id,
                           'nome': paciente.nome,
                           'id_agendamento': agendamento.id}))
    lista = sorted(lista,
                   key=lambda x: '{0} {1}'.format(x['dia'], x['hora_inicio']))
    return dict(lista=lista)


def consulta():
    tipo_consulta = request.args(0) or redirect(URL(c='pacientes',
                                                    f='agendamentos'))
    # TODO: gambiarra.start()
    if request.vars['agendamento'] == 'True':
        id_agendamento = request.args(1) or redirect(URL(c='pacientes',
                                                         f='agendamentos'))
        agendamento = buscar('agendamento', id_agendamento)
        id_paciente = agendamento.id_paciente
        paciente = buscar('paciente', id_paciente)
        paciente.nascimento = paciente.nascimento.strftime('%d-%m-%Y')
    elif request.vars['agendamento'] == 'False':
        id_paciente = request.args(1) or redirect(URL(c='pacientes',
                                                      f='agendamentos'))
        paciente = buscar('paciente', id_paciente)
    else:
        raise HTTP(404)
    # TODO: gambiarra.stop()
    try:
        tipo_consulta = [i for i in tipos_consultas
                         if i['form'] == tipo_consulta][0]
    except IndexError:
        raise HTTP(404)
    form = SQLFORM(tipo_consulta['base'])
    response.view = tipo_consulta['view_form']
    form.vars.id_paciente = paciente.id
    if form.process().accepted:
        id_form = form.vars.id
        id_insert = db.consultas.insert(id_paciente=paciente.id,
                                        hora_fim=request.now,
                                        tipo_consulta=tipo_consulta['form'],
                                        id_form=id_form)
        if not id_insert:
            raise HTTP(500)
        redirect(URL(c='pacientes', f='ver_consulta', args=id_insert),
                 client_side=True)
    return locals()


def consultas():
    id_paciente = request.args(0) or redirect(URL(c='pacientes',
                                                  f='todas_consultas'))
    paciente = buscar('paciente', id_paciente)
    consultas = buscar('consulta_paciente', id_paciente)
    for consulta in consultas:
        consulta.tipo_consulta = [i['label'] for i in tipos_consultas
                                  if consulta.tipo_consulta == i['form']][0]
    return locals()


def nova_consulta():
    links = [lambda row: A('Iniciar consulta', _class='button btn\
                                                       btn-default',
                           _href=URL(c='pacientes', f='consultar',
                                     args=[row.id]))]
    grid = SQLFORM.grid(db.pacientes,
                        fields=[db.pacientes.nome, db.pacientes.cpf],
                        links=links, csv=False, editable=False,
                        deletable=False, details=False, create=False)
    return locals()


def consultar():
    id_paciente = request.args(0) or redirect(URL(c='pacientes',
                                                  f='todas_consultas'))
    paciente = buscar('paciente', id_paciente)
    form = SQLFORM.factory(Field('tipo_consulta',
                                 requires=IS_IN_SET([i['label'] for i in
                                                    tipos_consultas])),
                                 formstyle='bootstrap3_stacked')
    if form.process().accepted:
        tipo_consulta = form.vars.tipo_consulta
        tipo_consulta_form = [i['form'] for i in tipos_consultas
                              if tipo_consulta == i['label']][0]
        redirect(URL(c='pacientes', f='consulta',
                 args=[tipo_consulta_form, id_paciente],
                 vars=dict(agendamento=False)), client_side=True)
    return locals()


def todas_consultas():
    links = [lambda row: A('Ver consulta', _class='button btn btn-default',
                           _href=URL(c='pacientes', f='ver_consulta',
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
    id_consulta = request.args(0) or redirect(URL(c='pacientes',
                                                  f='todas_consultas'))
    consulta = buscar('consulta', id_consulta)
    consulta.tipo_consulta = [i['label'] for i in tipos_consultas
                              if consulta.tipo_consulta == i['form']][0]
    paciente = buscar('paciente', consulta.id_paciente)
    return locals()


def prontuario_consulta():
    id_consulta = request.args(0) or redirect(URL(c='pacientes',
                                                  f='todas_consultas'))
    consulta = buscar('consulta', id_consulta)
    tipo_consulta = consulta.tipo_consulta
    ficha = [i['base'] for i in tipos_consultas
             if i['form'] == tipo_consulta][0]
    formulario = db(ficha.id == consulta.id_form).select().first()
    response.view = [i['view_prontuario'] for i in tipos_consultas
                     if i['form'] == tipo_consulta][0]
    return locals()


@cache.action()
def download():
    return response.download(request, db)

