# -*- coding: utf-8 -*-

def gerar_prescricao():
    id_paciente = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    paciente = db(db.pacientes.id == id_paciente).select().first()
    form = SQLFORM(db.prescricoes)
    form.vars.id_paciente = paciente.id
    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='prescricao', f='prescricao', args=id),
                 client_side=True)
    return locals()


def prescricao():
    id_prescricao = request.args(0) or redirect(URL(c='consulta',
                                                    f='todas_consultas'))
    prescricao = db(db.prescricoes.id == id_prescricao).select().first()
    paciente = db(db.pacientes.id == prescricao.id_paciente)
    return locals()


def prescricoes():
    id_paciente = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    paciente = db(db.pacientes.id == id_paciente).select().first()
    prescricoes = db(db.prescricoes.id_paciente == paciente.id).select()
    return locals()
