# -*- coding: utf-8 -*-

@auth.requires_login()
def nova_ficha():
    id_consulta_pre_natal = request.args(0) or redirect(URL(c='consulta',
                                                            f='todas_consultas'))
    consulta = db(db.ficha_clinica_pre_natal.id == id_consulta_pre_natal).select().first()
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    pre_natal_anteriores = db(db.ficha_pre_natal_evolucao.id_ficha == consulta.id).select()
    numero_pre_natal = len(pre_natal_anteriores) + 1
    form = SQLFORM(db.ficha_pre_natal_evolucao)
    form.vars.id_ficha = consulta.id
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
    return locals()


@auth.requires_login()
def editar_ficha():
    id_ficha = request.args(0) or redirect(URL(c='consulta',
                                               f='todas_consultas'))
    ficha = db(db.ficha_pre_natal_evolucao.id == id_ficha).select().first()
    consulta = db(db.ficha_clinica_pre_natal.id == ficha.id_ficha).select().first()
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    form = SQLFORM(db.ficha_pre_natal_evolucao, record=ficha)
    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='consulta_pre_natal', f='ver_ficha', args=id))
    return locals()


