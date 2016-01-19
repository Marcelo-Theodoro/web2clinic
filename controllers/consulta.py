# -*- coding: utf-8 -*-

@auth.requires_login()
def nova_ficha():
    tipo_consulta = request.args(0)
    id_consulta = request.args(1)
    tipo_consulta = TipoConsultaFormParaDict(tipo_consulta)
    consulta = BuscaConsulta(id_consulta)
    paciente = BuscaPaciente(consulta.id_paciente)

    if consulta.id_agendamento != 'NaoAgendado':
        pre_consulta_agendamento = BuscaPreConsultaAgendamento(consulta.id_agendamento)
    else:
        pre_consulta_agendamento = False

    if ChecaFichaValida(tipo_consulta['base']):
        base = eval(tipo_consulta['base'])
    else:
        raise HTTP(403)

    form = SQLFORM(base)
    if tipo_consulta['form'] == 'ficha_clinica_pre_natal':
        form.vars.id_consulta = consulta.id
    response.view = tipo_consulta['view_form']
    form.vars.id_paciente = paciente.id

    if form.process().accepted:
        id_form = form.vars.id
        id_ficha = db.fichas.insert(id_paciente=paciente.id,
                                    id_consulta=consulta.id,
                                    tipo_consulta = tipo_consulta['form'],
                                    id_form=id_form)
        redirect(URL(c='prontuario', f='ficha', args=id_ficha))
    return locals()


@auth.requires_login()
def editar_ficha():
    # Recebe: consulta/editar_ficha/*tipo_consulta['form']*/*id_consulta*?editar=*id_ficha*
    tipo_consulta = request.args(0) # depreciated
    id_consulta = request.args(1)
    ficha_id = request.vars['editar']
    # Busca a consulta
    consulta = BuscaConsulta(id_consulta)
    # Busca a pre consulta do agendamento, se houver.
    if consulta.id_agendamento != 'NaoAgendado':
        pre_consulta_agendamento = BuscaPreConsultaAgendamento(consulta.id_agendamento)
    else:
        pre_consulta_agendamento = False
    # Busca o paciente
    paciente = BuscaPaciente(consulta.id_paciente)
    # Busca o registro da ficha
    ficha = BuscaFicha(ficha_id)
    # Busca o dicionário para o tipo de consulta selecionado em args(0)
    tipo_consulta = TipoConsultaFormParaDict(ficha.tipo_consulta)
    # Verifica se o que será executado pelo eval() é realmente o objeto
    # db.*, e não um código malicioso
    if ChecaFichaValida(tipo_consulta['base']):
        base = eval(tipo_consulta['base'])
    else:
        raise HTTP(403)
    # Busca o formulario que vai ser atualizado
    formulario = db(base.id == ficha.id_form).select().first()
    # Oculta o id no form
    base.id.readable = False
    # Cria o form para update da ficha
    form = SQLFORM(base, record=formulario)
    # Selecionar a view para edição
    response.view = tipo_consulta['view_form']

    if form.process().accepted:
        redirect(URL(c='prontuario', f='ficha', args=ficha.id))
    return locals()


@auth.requires_login()
def consultas():
    id_paciente = request.args(0)
    paciente = BuscaPaciente(id_paciente)
    consultas = BuscaTodasConsultasPaciente(paciente.id)
    return locals()


@auth.requires_login()
def nova_consulta():
    pacientes = BuscaTodosPacientes()
    if pacientes:
        links = [lambda row: A('Iniciar consulta', _class='button btn\
                                                           btn-default',
                               _href=URL(c='consulta', f='consultar',
                                         args=[row.id]))]
        grid = SQLFORM.grid(db.pacientes,
                            fields=[db.pacientes.nome, db.pacientes.cpf],
                            links=links, csv=False, editable=False,
                            deletable=False, details=False, create=False,
                            paginate=10)
    else:
        grid = False
    return locals()


@auth.requires_login()
def consultar():
    id_paciente = request.args(0)
    paciente = BuscaPaciente(id_paciente)

    if request.vars['agendamento']:
        # Busca o agendamento e guarda em "agendamento"
        id_agendamento = request.vars['agendamento']
        agendamento = BuscaAgendamento(id_agendamento)
        # Busca pre consulta
        pre_consulta_agendamento = BuscaPreConsultaAgendamento(agendamento.id)
    else:
        agendamento = False

    form = SQLFORM.factory(submit_button='Iniciar consulta')

    if form.process().accepted:
         # Faz o registro da consulta
        id_agendamento = id_agendamento if agendamento else 'NaoAgendado'
        id_consulta = db.consultas.insert(id_paciente=paciente.id,
                                          id_agendamento=str(id_agendamento),
                                          dia=request.now,
                                          hora_inicio=request.now,
                                          hora_fim=request.now)

        # Atualizado o status
        if agendamento:
            AtualizaStatusAgendamento(agendamento.id, status='realizado')

        redirect(URL(c='consulta', f='ver_consulta', args=id_consulta))
    return locals()


@auth.requires_login()
def todas_consultas():
    consultas = BuscaTodasConsultas()
    if consultas:
        links = [lambda row: A(SPAN('Visualizar',
                                    _class='icon magnifier icon-zoom-in\
                                            glyphicon glyphicon-zoom-in'),
                               _class='button btn btn-default',
                               _href=URL(c='consulta', f='ver_consulta',
                                         args=[row.id])),
                 lambda row: A(SPAN('Apagar',
                                    _class='icon trash icon-trash glyphicon\
                                    glyphicon-trash'),
                               _class='button btn btn-default',
                               _href=URL(c='consulta', f='apagar_consulta',
                                         args=[row.id]))]
        haders = {'consultas.id_paciente': 'Paciente'}
        db.consultas.id_paciente.readable = True
        form = SQLFORM.grid(db.consultas,
                            fields=[db.consultas.id_paciente,
                                    db.consultas.dia],
                            csv=False, editable=False, deletable=False,
                            details=False, create=False, links=links,
                            headers=haders, paginate=10)
    else:
        form = False
    return locals()


@auth.requires_login()
def ver_consulta():
    id_consulta = request.args(0)
    consulta = BuscaConsulta(id_consulta)
    fichas = BuscaTodasFichasConsulta(consulta.id)
    for ficha in fichas:
        ficha.tipo_consulta = TipoConsultaFormParaDict(ficha.tipo_consulta)
        ficha.label = ficha.tipo_consulta['label']
        ficha.form = ficha.tipo_consulta['form']
    paciente = BuscaPaciente(consulta.id_paciente)
    consultas_pre_natal = db(db.ficha_clinica_pre_natal.id_paciente == paciente.id).select()
    atestados = db(db.atestados.id_consulta == consulta.id).select()
    exames = db(db.exames.id_consulta == consulta.id).select()
    prescricoes = db(db.prescricoes.id_consulta == consulta.id).select()
    return locals()


@auth.requires_login()
def apagar_consulta(): # depreciated
    import re
    id_consulta = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    consulta = db(db.consultas.id == id_consulta).select().first()
    if not consulta:
        raise HTTP(404)
    consulta.dia = consulta.dia.strftime(format='%d/%m/%Y')
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    fichas = db(db.fichas.id_consulta == consulta.id).select()
    consultas_pre_natal = db(db.ficha_clinica_pre_natal.id_paciente == paciente.id).select()
    form = SQLFORM.factory()
    if form.process().accepted:
        # Deleta ficha_pre_natal_evolucao associadas
        for consulta in consultas_pre_natal:
            db(db.ficha_pre_natal_evolucao.id_ficha == consulta.id).delete()
        # Deletas as fichas associadas
        for ficha in fichas:
            # Verifica se o que será executado pelo eval() é realmente o objeto
            # db.*, e não um código malicioso
            tipo_consulta = [i for i in tipos_consultas
                             if i['form'] == ficha.tipo_consulta][0]
            if re.match('db.ficha_([a-z]+|_+[a-z]+)|db.retorno', tipo_consulta['base']):
                base = eval(tipo_consulta['base'])
                db(base.id == ficha.id_form).delete()
            else:
                raise HTTP(403)
        # Deleta os registros das fichas
        db(db.fichas.id_consulta == consulta.id).delete()
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
    
@auth.requires_login()
def pesquisa():
    pesquisa = request.args(0)

    if pesquisa:
        pacientes = db(db.pacientes.nome.contains(pesquisa)).select() or db(db.pacientes.cpf.contains(pesquisa)).select()
    else:
        pacientes = db(db.pacientes).select()

    return locals()

@auth.requires_login()
def pesquisa_consultas():
    pesquisa = request.args(0)
    db.consultas.id_paciente.readable = True

    if pesquisa:
        consultas = db(db.pacientes.nome.contains(pesquisa)).select(join=db.consultas.on(db.pacientes.id == db.consultas.id_paciente))
    else:
        consultas = db(db.consultas).select(join=db.pacientes.on(db.pacientes.id == db.consultas.id_paciente))

    return locals()


