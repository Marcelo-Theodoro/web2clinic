# -*- coding: utf-8 -*-

def gerar_atestado():
    id_paciente = request.args(0) or redirect(URL(c='paciente',
                                                  f='todas_consultas'))
    paciente = db(db.pacientes.id == id_paciente).select().first()
    form = SQLFORM(db.atestados)
    form.vars.id_paciente = paciente.id
    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='atestado', f='atestado', args=id), client_side=True)
    return locals()


def atestado():
    id_atestado = request.args(0) or redirect(URL(c='paciente',
                                                  f='todas_consultas'))
    atestado = db(db.atestados.id == id_atestado).select().first()
    paciente = db(db.pacientes.id == atestado.id_paciente)
    return locals()


def atestados():
    id_paciente = request.args(0) or redirect(URL(c='paciente',
                                                  f='todas_consultas'))
    paciente = db(db.pacientes.id == id_paciente)
    atestados = db(db.atestados.id_paciente == id_paciente)
    return locals()
