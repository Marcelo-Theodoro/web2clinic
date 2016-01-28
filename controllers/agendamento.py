# -*- coding: utf-8 -*-

@auth.requires_login()
def novo_agendamento():
    pacientes = BuscaTodosPacientes()
    if pacientes:
        links = [lambda row: A(SPAN('Agendar',
                                    _class='icon plus icon-plus\
                                            glyphicon glyphicon-plus'),
                               _class='button btn btn-default',
                               _href=URL(c='agendamento', f='agendar',
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
def agendar():
    id_paciente = request.args(0)
    paciente = BuscaPaciente(id_paciente)
    form = SQLFORM(db.agendamentos)
    form.vars.id_paciente = id_paciente
    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='agendamento', f='agendamentos'),
                 client_side=True)
    return locals()


@auth.requires_login()
def editar_agendamento():
    id_agendamento = request.args(0)
    agendamento = BuscaAgendamento(id_agendamento)
    db.agendamentos.id.readable = False
    form = SQLFORM(db.agendamentos, record=agendamento)
    if form.process().accepted:
        redirect(URL(c='agendamento', f='agendamento', args=id_agendamento),
                 client_side=True)
    return locals()


@auth.requires_login()
def agendamento():
    id_agendamento = request.args(0)

    agendamento = BuscaAgendamento(id_agendamento)
    paciente = BuscaPaciente(agendamento.id_paciente)

    if agendamento.status == 'agendado':
        '''
        Se o status for agendado: Vai retornar um form para a
        pre_consulta_agendamento.
        Ao submitar o form, é alterado o status para aguardando
        e da um reload na página.
        '''
        form = SQLFORM(db.pre_consulta_agendamento, submit_button='Salvar pré consulta')
        form.vars.id_agendamento = agendamento.id

        if form.process().accepted:
            AtualizaStatusAgendamento(agendamento.id, status='aguardando')
            redirect(URL(c='agendamento', f='agendamento', args=agendamento.id))

        form_faltou = SQLFORM.factory(submit_button='Paciente não compareceu')
        if form_faltou.process().accepted:
            AtualizaStatusAgendamento(agendamento.id, status='faltou')
            redirect(URL(c='agendamento', f='agendamento', args=agendamento.id))
    elif agendamento.status == 'aguardando':
        # Apenas redireciona para outra página
        redirect(URL(c='consulta', f='consultar', args=paciente.id, vars=dict(agendamento=agendamento.id)))
    elif agendamento.status == 'realizado':
        form = False
        form_faltou = False
    elif agendamento.status == 'faltou':
        form = False
        form_faltou = False

    return locals()


@auth.requires_login()
def apagar_agendamento():
    id_agendamento = request.args(0)
    agendamento = BuscaAgendamento(id_agendamento)
    paciente = BuscaPaciente(agendamento.id_paciente)
    form = SQLFORM.factory()
    if form.process().accepted:
        db(db.agendamentos.id == id_agendamento).delete()
        redirect(URL(c='agendamento', f='agendamentos'), client_side=True)
    return locals()


@auth.requires_login()
def agendamentos():
    from datetime import datetime
    data = datetime.now().date()
    agendamentos = db(db.agendamentos).select()
    qtd_agendamentos_dia = len([i for i in agendamentos
                                if i.dia == data])
    lista = []
    for agendamento in agendamentos:
        paciente = db(db.pacientes.id == agendamento.id_paciente).select().first()
        # armazena o valor no formato iso para uso de um js.
        agendamento.dia_iso = agendamento.dia
        # Representação no padrão hue br.
        agendamento.dia = agendamento.dia.strftime('%d/%m/%Y')
        lista.append(dict({'dia': agendamento.dia,
                           'dia_iso': agendamento.dia_iso,
                           'hora_inicio': agendamento.hora_inicio,
                           'hora_fim': agendamento.hora_fim,
                           'id_paciente': paciente.id,
                           'nome': paciente.nome,
                           'id_agendamento': agendamento.id,
                            'status': agendamento.status}))
    lista = sorted(lista,
                   key=lambda x: '{0} {1}'.format(x['dia'], x['hora_inicio']))
    return dict(lista=lista, qtd_agendamentos_dia=qtd_agendamentos_dia)
    
@auth.requires_login()
def pesquisa():
    pesquisa = request.args(0)
    if pesquisa:
        pacientes = db(db.pacientes.nome.contains(pesquisa)).select() or db(db.pacientes.cpf.contains(pesquisa)).select()
    else:
        pacientes = db(db.pacientes).select()

    return locals()

