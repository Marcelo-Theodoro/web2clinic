# -*- coding: utf-8 -*-


db.define_table('atestados',
                Field('id_paciente', 'reference pacientes',
                      readable=False, writable=False),
                Field('id_consulta', 'reference consultas',
                      readable=False, writable=False),
                Field('atestado', 'text'),
                Field('data_criacao', type='datetime', default=request.now,
                      requires=IS_DATE(format=('%d/%m/%Y'))),
                )
