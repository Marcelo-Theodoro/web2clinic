# -*- coding: utf-8 -*-
db.define_table('agendamentos',
                Field('id_paciente', 'reference pacientes',
                    readable=False, writable=False),
                Field('dia', type='date',
                    requires=IS_DATE(format='%d/%m/%Y')),
                Field('hora_inicio', type='time', requires=IS_TIME()),
                Field('hora_fim', type='time', requires=IS_TIME()),
                format='%(id_paciente)s %(dia)s'
                )
