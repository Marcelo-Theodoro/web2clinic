# -*- coding: utf-8 -*-

@auth.requires_login()
def consulta():
    '''
    Página de consulta, onde os formulários são preenchidos.

    Recebe:
        arg0: tipo de consulta(form, de acordo com {tipos_consultas})
        arg1: id do paciente que fará a consulta.
    Pode receber também:
        agendamento: Uma variáveis que traz o id de um agendamento,
                     que será deletado ao final da consulta
        editar: Caso receba a variável editar com o id de uma consulta,
                ao invés da função fazer a criação de um novo form,
                ela irá editar um form já existente.
    '''
    tipo_consulta = request.args(0) or redirect(URL(c='consulta',
                                                    f='todas_consultas'))
    try:
        # Busca no dicionário tipos_consultas as informações
        # deste tipo de consulta.
        tipo_consulta = [i for i in tipos_consultas
                         if i['form'] == tipo_consulta][0]
    except IndexError:
        # O tipo de consulta passada não existe.
        raise HTTP(404)

    id_paciente = request.args(1) or redirect(URL(c='consulta',
                                                 f='todas_consultas'))
    paciente = db(db.pacientes.id == id_paciente).select().first()
    if not paciente:
        # Paciente não existe.
        raise HTTP(404)

    if request.vars['agendamento']:
        # Caso exista essa variável, quer dizer que existe um agendamento
        # que deve ser deletado ao final da consulta.
        id_agendamento = request.vars['agendamento']
        agendamento = db(db.agendamentos.id == id_agendamento).select().first()
        if not agendamento:
            # O agendamento não existe
            raise HTTP(404)
        if str(agendamento.id_paciente) != id_paciente:
            # O agendamento não pertence ao mesmo paciente.
            raise HTTP(404)
    else:
        # Não tem agendamento.
        id_agendamento = False

    if request.vars['editar']:
        # u -> update
        u_consulta_id = request.vars['editar']
        u_consulta = db(db.consultas.id == u_consulta_id).select().first()
        if str(u_consulta.id_paciente) != id_paciente:
            # A consulta não pertence ao mesmo paciente.
            raise HTTP(404)
        if not u_consulta:
            # id recebido não corresponde a nenhuma consulta
            raise HTTP(404)
        u_tipo_consulta = [x['base'] for x in tipos_consultas
                           if u_consulta.tipo_consulta == x['form']][0]
        u_form_id = u_consulta.id_form
        u_ficha = db(u_tipo_consulta.id == u_form_id).select().first()
        if not u_ficha:
            # Ficha não existe
            raise HTTP(404)
    else:
        u_ficha = False


    form = SQLFORM(tipo_consulta['base'] if not u_ficha
                   else tipo_consulta['base'], record=u_ficha)
    response.view = tipo_consulta['view_form']
    form.vars.id_paciente = paciente.id
    if form.process().accepted:
        if not u_ficha:
            id_form = form.vars.id
            # Insere as informações no BD consultas
            id_next = db.consultas.insert(id_paciente=paciente.id,
                                          dia=request.now,
                                          hora_inicio=request.now,
                                          hora_fim=request.now,
                                          tipo_consulta=tipo_consulta['form'],
                                          id_form=id_form)

            if id_agendamento:
                # Se houver agendamento, então este bloco vai deleta-lo
                # ao fim a consulta.
                db(db.agendamentos.id == id_agendamento).delete()

        else:
            id_next = u_consulta_id

        redirect(URL(c='consulta', f='ver_consulta', args=id_next),
                 client_side=True)
    return locals()


@auth.requires_login()
def consultas():
    id_paciente = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    paciente = db(db.pacientes.id == id_paciente).select().first()
    consultas = db(db.consultas.id_paciente == id_paciente).select()
    for consulta in consultas:
        consulta.dia = consulta.dia.strftime(format='%d/%m/%Y')
        consulta.tipo_consulta = [i['label'] for i in tipos_consultas
                                  if consulta.tipo_consulta == i['form']][0]
    return locals()


@auth.requires_login()
def nova_consulta():
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
                                db.consultas.dia],
                        csv=False, editable=False, deletable=False,
                        details=False, create=False, links=links,
                        headers=haders, paginate=10)
    return locals()


@auth.requires_login()
def ver_consulta():
    id_consulta = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    consulta = db(db.consultas.id == id_consulta).select().first()
    if not consulta:
        raise HTTP(404)
    consulta.tipo_consulta = [i for i in tipos_consultas
                              if consulta.tipo_consulta == i['form']][0]
    consulta.label = consulta.tipo_consulta['label']
    consulta.form = consulta.tipo_consulta['form']
    consulta.dia = consulta.dia.strftime(format='%d/%m/%Y')
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    return locals()


@auth.requires_login()
def apagar_consulta():
    id_consulta = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    consulta = db(db.consultas.id == id_consulta).select().first()
    if not consulta:
        raise HTTP(404)
    consulta.dia = consulta.dia.strftime(format='%d/%m/%Y')
    form = SQLFORM.factory()
    if form.process().accepted:
        # Deleta prescrições associadas a consulta
        db(db.prescricoes.id_consulta == consulta.id).delete()
        # Deleta atestados associadas a consulta
        db(db.atestados.id_consulta == consulta.id).delete()
        # Delete a consulta
        db(db.consultas.id == consulta.id).delete()
        redirect(URL(c='consulta', f='todas_consultas'))
    return locals()


