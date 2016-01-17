# -*- coding: utf-8 -*-


db.define_table('consultas',
                Field('id_paciente', 'reference pacientes',
                    readable=False, writable=False),
                Field('id_agendamento', type='string',
                      readable=False, writable=False),
                Field('dia', type='date', requires=IS_DATE(format='%d/%m/%Y')),
                Field('hora_inicio', requires=IS_TIME()),  # TODO
                Field('hora_fim', requires=IS_TIME()),
                )

def BuscaConsulta(id):
    # Recebe id da consulta
    if not id:
        raise HTTP(404, 'Consulta ID não encontrada')
    try:
        consulta = db(db.consultas.id == id).select().first()
        if consulta.dia:
            consulta.dia = consulta.dia.strftime('%d/%m/%Y')
    except ValueError:
        raise HTTP(404, 'Consulta inválida')
    if not consulta:
        raise HTTP(404, 'Consulta não encontrada')
    return consulta

def BuscaTodasConsultasPaciente(id):
    # Recebe id paciente
    if not id:
        raise HTTP(404, 'ID inválido')
    consultas = db(db.consultas.id_paciente == id).select()
    for consulta in consultas:
        if consulta.dia:
            consulta.dia = consulta.dia.strftime(format='%d/%m/%Y')
    return consultas



def BuscaTodasConsultas():
    consultas = db(db.consultas).select()
    return consultas






