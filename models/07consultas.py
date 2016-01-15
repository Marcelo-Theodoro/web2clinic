# -*- coding: utf-8 -*-


db.define_table('consultas',
                Field('id_paciente', 'reference pacientes',
                    readable=False, writable=False),
                Field('dia', type='date', requires=IS_DATE(format='%d/%m/%Y')),
                Field('hora_inicio', requires=IS_TIME()),  # TODO
                Field('hora_fim', requires=IS_TIME()),
                )
