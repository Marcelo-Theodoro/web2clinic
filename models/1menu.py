# -*- coding: utf-8 -*-

response.menu = [
    ('Home', False, URL(c='pacientes', f='index'), []),
    ('Agendamentos', False, URL('#'), [
        ('Novo agendamento', False, URL(c='pacientes', f='novo_agendamento')),
        ('Ver todos agendamentos', False, URL(c='pacientes', f='agendamentos')),
        ]),
    ('Pacientes', False, URL('#'), [
            ('Novo cadastro', False, URL(c='pacientes', f='cadastrar')), # alterar para novo_paciente
            ('Todos cadastros', False, URL(c='pacientes', f='pacientes')),
        ]),
    ('Consultas', False, URL('#'), [
            ('Nova consulta', False, URL(c='pacientes', f='nova_consulta')),
            ('Todas consultas', False, URL(c='pacientes', f='todas_consultas')),
        ]),
]


if "auth" in locals(): auth.wikimenu()
