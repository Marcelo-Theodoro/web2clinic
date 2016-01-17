# -*- coding: utf-8 -*-

STATUS_AGENDAMENTO = [
    ('agendado', 'Agendado'),
    ('aguardando', 'Aguardando'),
    ('realizado', 'Realizado'),
    ('faltou', 'Faltou'),
]

db.define_table('agendamentos',
                Field('id_paciente', 'reference pacientes',
                    readable=False, writable=False),
                Field('dia', type='date',
                    requires=IS_DATE(format='%d/%m/%Y')),
                Field('hora_inicio', type='time', requires=IS_TIME()),
                Field('hora_fim', type='time', requires=IS_TIME()),
                Field('status', requires=IS_IN_SET(STATUS_AGENDAMENTO), default='agendado',
                      readable=False, writable=False),
                format='%(id_paciente)s %(dia)s'
                )


db.define_table('pre_consulta_agendamento',
                Field('id_agendamento', 'reference agendamentos',
                      readable=False, writable=False),
                Field('peso', label='Peso', type='string'),
                Field('pressao_arterial', label='Pressão arterial', type='string'),
                )

def BuscaAgendamento(id):
    if not id:
        raise HTTP(404, 'ID agendamento não encontrado')
    try:
        agendamento = db(db.agendamentos.id == id).select().first()
    except ValueError:
        raise HTTP(404, 'Argumento AGENDAMENTO inválido')
    if not agendamento:
        raise HTTP(404, 'Agendamento não encontrado')
    if agendamento.dia and request.function != 'editar_agendamento':
        agendamento.dia = agendamento.dia.strftime('%d/%m/%Y')
    return agendamento


def BuscaPreConsultaAgendamento(id):
    # Recebe id do agendamento
    id = int(id)
    if not id:
        raise HTTP(404)
    try:
        pre_consulta = db(db.pre_consulta_agendamento.id_agendamento == id).select().first()
    except ValueError:
        raise HTTP(404)
    if not pre_consulta:
        raise HTTP(404)
    return pre_consulta


def AtualizaStatusAgendamento(id, status):
    # Recebe id do agendamento e o novo status
    if not id or status not in dict(STATUS_AGENDAMENTO):
        raise HTTP(404)
    db(db.agendamentos.id == id).update(status=status)

















