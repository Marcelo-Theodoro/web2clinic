# -*- coding: utf-8 -*-


CC = dict(
    nome_clinica = 'Clínica do X',
    nome_medico = 'João X',
    especialidade = 'Clínico Geral',
    crm = '9999999999999',
    telefone = '14 9999999',
    endereco = 'R. Getúlio Vargas, 560, Centro - Ourinhos, SP, BRASIL.'
)

CATEGORIAS_MEDICAMENTOS = ['Uso interno', 'Uso externo', 'Uso local',
                           'Uso transdérmico', 'Uso sublingual']


db.define_table('lista_medicamentos',
                Field('nome', label='Nome', requires=IS_NOT_EMPTY()),
                Field('texto'),
                Field('categoria', requires=IS_IN_SET(CATEGORIAS_MEDICAMENTOS)),
                Field('fichas',
                      requires=IS_EMPTY_OR(IS_IN_SET([i['form'] for i in tipos_consultas],
                                                     multiple=True)),
                      widget=SQLFORM.widgets.checkboxes.widget),
                format='%(nome)s'
                )

db.define_table('lista_exames',
                Field('nome', label='Nome', requires=IS_NOT_EMPTY()),
                Field('fichas',
                      requires=IS_EMPTY_OR(IS_IN_SET([i['form'] for i in tipos_consultas],
                                                     multiple=True)),
                      widget=SQLFORM.widgets.checkboxes.widget),
                format='%(nome)s'
                )
