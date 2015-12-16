# -*- coding: utf-8 -*-

@auth.requires_login()
def consulta():
    # Falta a edição
    tipo_consulta = request.args(0) or redirect(URL(c='consulta',
                                                    f='todas_consultas'))
    id_paciente = request.args(1) or redirect(URL(c='consulta',
                                                 f='todas_consultas'))
    # Trata o tipo de consulta
    tipo_consulta = [i for i in tipos_consultas
                     if tipo_consulta == i['form']][0]
    # Busca paciente
    paciente = db(db.pacientes.id == id_paciente).select().first()
    paciente.nascimento = paciente.nascimento.strftime(format='%d/%m/%Y')
    # Trata agendamento
    if request.vars['agendamento']:
        id_agendamento = request.vars['agendamento']
        agendamento = db(db.agendamentos.id == id_agendamento).select().first()
    else:
        id_agendamento = False
    # Trata edição
    if request.vars['editar']:
        u_consulta_id = request.vars['editar']
        u_consulta = db(db.consultas.id == u_consulta_id).select().first()
        u_tipo_consulta = [x['base'] for x in tipos_consultas
                           if u_consulta.tipo_consulta == x['form']][0]
        u_form_id = u_consulta.id_form
        u_ficha = db(u_tipo_consulta.id == u_form_id).select().first()
    else:
        u_ficha = False

    # Cria form, verifica se é edição
    form = SQLFORM(tipo_consulta['base'] if not u_ficha
                   else tipo_consulta['base'], record=u_ficha)
    # Selecionar a view para edição
    response.view = tipo_consulta['view_form']
    # Inputa o ID do paciente no form
    form.vars.id_paciente = paciente.id
    if form.process().accepted:
        # Caso não seja edição de ficha é criada uma nova consulta
        if not u_ficha:
            id_form = form.vars.id
            # Cria a consulta
            id_consulta = db.consultas.insert(id_paciente=paciente.id,
                                          dia=request.now,
                                          hora_inicio=request.now,
                                          hora_fim=request.now)
            # Cria o registro da ficha
            id_ficha = db.fichas.insert(id_paciente=paciente.id,
                                        id_consulta=id_consulta,
                                        tipo_consulta = tipo_consulta['form'],
                                        id_form=id_form)
            # Se houver agendamento, deleta
            if id_agendamento:
                db(db.agendamentos.id == id_agendamento).delete()
        else:
            # Caso SEJA edição de ficha
            id_consulta = u_consulta_id
        redirect(URL(c='consulta', f='ver_consulta', args=id_consulta),
                 client_side=True)
    return locals()


@auth.requires_login()
def consultas():
    # Ok
    id_paciente = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    paciente = db(db.pacientes.id == id_paciente).select().first()
    consultas = db(db.consultas.id_paciente == id_paciente).select()
    for consulta in consultas:
        consulta.dia = consulta.dia.strftime(format='%d/%m/%Y')
    return locals()


@auth.requires_login()
def nova_consulta():
    # ok
    links = [lambda row: A('Iniciar consulta', _class='button btn\
                                                       btn-default',
                           _href=URL(c='consulta', f='consultar',
                                     args=[row.id]))]
    grid = SQLFORM.grid(db.pacientes,
                        fields=[db.pacientes.nome, db.pacientes.cpf],
                        links=links, csv=False, editable=False,
                        deletable=False, details=False, create=False,
                        paginate=10)
    return locals()


@auth.requires_login()
def consultar():
    # ok
    id_paciente = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    paciente = db(db.pacientes.id == id_paciente).select().first()
    form = SQLFORM.factory(Field('tipo_consulta',
                                 requires=IS_IN_SET([i['label'] for i in
                                                    tipos_consultas])))
    if form.process().accepted:
        tipo_consulta = form.vars.tipo_consulta
        tipo_consulta_form = [i['form'] for i in tipos_consultas
                              if tipo_consulta == i['label']][0]
        redirect(URL(c='consulta', f='consulta',
                 args=[tipo_consulta_form, id_paciente]), client_side=True)
    return locals()


@auth.requires_login()
def todas_consultas():
    # ok
    links = [lambda row: A('Ver consulta', _class='button btn btn-default',
                           _href=URL(c='consulta', f='ver_consulta',
                                     args=[row.id]))]
    haders = {'consultas.id_paciente': 'Paciente'}
    db.consultas.id_paciente.readable = True
    form = SQLFORM.grid(db.consultas,
                        fields=[db.consultas.id_paciente,
                                db.consultas.dia],
                        csv=False, editable=False, deletable=False,
                        details=False, create=False, links=links,
                        headers=haders, paginate=10)
    return locals()


@auth.requires_login()
def ver_consulta():
    # ok
    id_consulta = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    consulta = db(db.consultas.id == id_consulta).select().first()
    if not consulta:
        raise HTTP(404)
    fichas = db(db.fichas.id_consulta == consulta.id).select()
    # Retorna objeto fichas que traz, bom, todas as fichas.
    for ficha in fichas:
        ficha.tipo_consulta = [i for i in tipos_consultas
                                  if ficha.tipo_consulta == i['form']][0]
        ficha.label = ficha.tipo_consulta['label']
        ficha.form = ficha.tipo_consulta['form']
    consulta.dia = consulta.dia.strftime(format='%d/%m/%Y')
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    atestados = db(db.atestados.id_consulta == consulta.id).select()
    exames = db(db.exames.id_consulta == consulta.id).select()
    prescricoes = db(db.prescricoes.id_consulta == consulta.id).select()
    return locals()


@auth.requires_login()
def apagar_consulta():
    # NÃO ESTÁ OK
    id_consulta = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    consulta = db(db.consultas.id == id_consulta).select().first()
    if not consulta:
        raise HTTP(404)
    consulta.dia = consulta.dia.strftime(format='%d/%m/%Y')
    consulta.tipo_consulta = ''.join(i['label'] for i in tipos_consultas
                                     if i['form'] == consulta.tipo_consulta)
    form = SQLFORM.factory()
    if form.process().accepted:
        # Deleta a ficha associada
        base_consulta = [i['base'] for i in tipos_consultas
                        if i['label'] == consulta.tipo_consulta][0]
        db(base_consulta.id == consulta.id_form).delete()
        # Deleta prescrições associadas a consulta
        db(db.prescricoes.id_consulta == consulta.id).delete()
        # Deleta atestados associados a consulta
        db(db.atestados.id_consulta == consulta.id).delete()
        # Deleta exames associados a consulta
        db(db.exames.id_consulta == consulta.id).delete()
        # Delete a consulta
        db(db.consultas.id == consulta.id).delete()
        redirect(URL(c='consulta', f='todas_consultas'))
    return locals()


