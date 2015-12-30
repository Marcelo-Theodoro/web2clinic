# -*- coding: utf-8 -*-


db.define_table('fichas',
                Field('id_paciente', 'reference pacientes',
                    readable=False, writable=False),
                Field('id_consulta', 'reference consultas',
                      readable=False, writable=False),
                Field('tipo_consulta'),
                Field('id_form'),
                )
