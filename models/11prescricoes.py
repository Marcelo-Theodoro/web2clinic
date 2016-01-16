# -*- coding: utf-8 -*-


db.define_table('prescricoes',
                Field('id_paciente', 'reference pacientes',
                      readable=False, writable=False),
                Field('id_consulta', 'reference consultas',
                      readable=False, writable=False),
                Field('data_criacao', type='date', default=request.now,
                      requires=IS_DATE(format='%d/%m/%Y')),
                Field('texto', type='text'),
                Field('medicamentos', type='list:string'),
                )


def BuscaPrescricao(id):
    # Recebe id da prescrição
    if not id:
        raise HTTP(404, 'ID inválido')
    try:
        prescricao = db(db.prescricoes.id == id).select().first()
    except ValueError:
        raise HTTP(404, 'ID inválido')
    if not prescricao:
        raise HTTP(404, 'Prescrição não encontrada')
    return prescricao
