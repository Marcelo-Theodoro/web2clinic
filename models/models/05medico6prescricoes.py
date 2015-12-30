# -*- coding: utf-8 -*-


db.define_table('prescricoes',
                Field('id_paciente', 'reference pacientes',
                      readable=False, writable=False),
                Field('id_consulta', 'reference consultas',
                      readable=False, writable=False),
                Field('data_criacao', type='date', default=request.now,
                      requires=IS_DATE(format='%d/%m/%Y')),
                Field('texto', type='text'),
                Field('medicamentos',
                      requires=IS_IN_DB(db, db.lista_medicamentos.nome,
                                        multiple=True),
                      widget=SQLFORM.widgets.checkboxes.widget),
                )
