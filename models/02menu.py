# -*- coding: utf-8 -*-

if auth.user:
    response.menu = [
        ('Home', False, URL(c='default', f='index'), []),
        ('Agendamentos', False, URL('#'), [
            ('Novo agendamento', False, URL(c='agendamento', f='novo_agendamento')),
            ('Ver todos agendamentos', False, URL(c='agendamento', f='agendamentos')),
            ]),
        ('Pacientes', False, URL('#'), [
                ('Novo cadastro', False, URL(c='paciente', f='cadastro')), # alterar para novo_paciente
                ('Todos cadastros', False, URL(c='paciente', f='pacientes')),
            ]),
        ('Consultas', False, URL('#'), [
                ('Nova consulta', False, URL(c='consulta', f='nova_consulta')),
                ('Todas consultas', False, URL(c='consulta', f='todas_consultas')),
            ]),
        ('Admin', False, URL('#'), [
                ('Cadastrar medicamento', False, URL(c='admin', f='cadastrar_medicamento')),
                ('Todos medicamentos', False, URL(c='admin', f='medicamentos')),
                ('Cadastrar exame', False, URL(c='admin', f='cadastrar_exame')),
                ('Todos exames', False, URL(c='admin', f='exames')),
                ('Backup', False, URL(c='backup', f='index')),
            ]),
    ]


if "auth" in locals():
    auth.wikimenu()
