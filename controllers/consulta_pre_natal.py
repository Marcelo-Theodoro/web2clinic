# -*- coding: utf-8 -*-

@auth.requires_login()
def nova_ficha():
    id_consulta_pre_natal = request.args(0)

    if not id_consulta_pre_natal:
        raise HTTP(404, 'Consulta não encontrada')
    consulta = db(db.ficha_clinica_pre_natal.id == id_consulta_pre_natal).select().first()
    if not consulta:
        raise HTTP(404, 'Consulta não encontrada')

    paciente = BuscaPaciente(consulta.id_paciente)

    pre_natal_anteriores = db(db.ficha_pre_natal_evolucao.id_ficha == consulta.id).select()

    numero_pre_natal = len(pre_natal_anteriores) + 1

    consulta_original = BuscaConsulta(consulta.id_consulta)
    if consulta_original.id_agendamento != 'NaoAgendado':
        pre_consulta_agendamento = BuscaPreConsultaAgendamento(consulta_original.id_agendamento)
    else:
        pre_consulta_agendamento = False

    form = SQLFORM(db.ficha_pre_natal_evolucao)
    form.vars.id_ficha = consulta.id
    form.vars.consulta_numero = numero_pre_natal
    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='consulta_pre_natal', f='ver_ficha', args=id))
    return locals()


@auth.requires_login()
def ver_ficha():
    id_ficha = request.args(0) or redirect(URL(c='consulta',
                                               f='todas_consultas'))
    ficha = db(db.ficha_pre_natal_evolucao.id == id_ficha).select().first()
    consulta = db(db.ficha_clinica_pre_natal.id == ficha.id_ficha).select().first()
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    consulta_original = BuscaConsulta(consulta.id_consulta)
    if consulta_original.id_agendamento != 'NaoAgendado':
        pre_consulta_agendamento = BuscaPreConsultaAgendamento(consulta_original.id_agendamento)
    else:
        pre_consulta_agendamento = False
    return locals()


@auth.requires_login()
def editar_ficha():
    id_ficha = request.args(0) or redirect(URL(c='consulta',
                                               f='todas_consultas'))
    ficha = db(db.ficha_pre_natal_evolucao.id == id_ficha).select().first()
    consulta = db(db.ficha_clinica_pre_natal.id == ficha.id_ficha).select().first()
    consulta_original = BuscaConsulta(consulta.id_consulta)
    if consulta_original.id_agendamento != 'NaoAgendado':
        pre_consulta_agendamento = BuscaPreConsultaAgendamento(consulta_original.id_agendamento)
    else:
        pre_consulta_agendamento = False
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    form = SQLFORM(db.ficha_pre_natal_evolucao, record=ficha)
    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='consulta_pre_natal', f='ver_ficha', args=id))
    return locals()
