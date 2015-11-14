# -*- coding: utf-8 -*-


# Opções para formulários
ufs = ['SP', 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
        'MT', 'MS', 'MG', 'PR', 'PB', 'PA', 'PE', 'PI', 'RJ', 'RN', 'RS',
          'RO', 'RR', 'SC', 'SE', 'TO']
escolaridade = ['Nenhuma', '1º grau', '2º grau', 'Superior']
cor = ['Branca', 'Negra', 'Parda', 'Indígena', 'Asiática']
estadocivil = ['Casada', 'Solteira (sem união estável)',
               'Solteira (com união estável)', 'Outra']
sexo = ['Feminino', 'Masculino']


# Configurações da clínica
CC = dict(
    nome_clinica = 'Clínica do X',
    nome_medico = 'João X',
    especialidade = 'Clínico Geral',
    crm = '9999999999999',
    telefone = '14 9999999',
    endereco = 'R. Getúlio Vargas, 560, Centro - Ourinhos, SP, BRASIL.'
)


remedios = ['remedio{0}'.format(n) for n in range(20)]


db.define_table('pacientes',
                Field('nome', requires=IS_NOT_EMPTY()),
                Field('sexo', default='Feminino', requires=IS_IN_SET(sexo)),
                Field('cpf'),
                Field('profissao'),
                Field('nascimento', type='date',
                    requires=IS_EMPTY_OR(IS_DATE(format='%d-%m-%Y'))),
                Field('telefone'),
                Field('escolaridade',
                    requires=IS_EMPTY_OR(IS_IN_SET(escolaridade))),
                Field('estadocivil',
                    requires=IS_EMPTY_OR(IS_IN_SET(estadocivil))),
                Field('cor', requires=IS_EMPTY_OR(IS_IN_SET(cor))),
                Field('image', 'upload'),
                Field('endereco'),
                Field('cidade'),
                Field('uf', requires=IS_EMPTY_OR(IS_IN_SET(ufs))),
                Field('cep'),
                Field('observacoes', type='text'),
                format='%(nome)s'
                )


db.define_table('agendamentos',
                Field('id_paciente', 'reference pacientes',
                    readable=False, writable=False),
                Field('dia', type='date',
                    requires=IS_DATE(format='%d-%m-%Y')),
                Field('hora_inicio', type='time', requires=IS_TIME()),
                Field('hora_fim', type='time', requires=IS_TIME()),
                format='%(id_paciente)s %(dia)s'
                )


db.define_table('consultas',
                Field('id_paciente', 'reference pacientes',
                    readable=False, writable=False),
                #Field('dia'),
                #Field('hora_inicio'),
                Field('hora_fim', requires=IS_TIME()),
                Field('tipo_consulta'),
                Field('id_form'),
                format='%(id_paciente)s %(tipo_consulta)s'
                )


db.define_table('atestados',
                Field('id_paciente', 'reference pacientes',
                      readable=False, writable=False),
                Field('atestado', 'text'),
                Field('data_criacao', type='datetime', default=request.now,
                      requires=IS_DATE(format=('%d-%m-%Y'))),
                )

db.define_table('prescricoes',
                Field('id_paciente', 'reference pacientes',
                      readable=False, writable=False),
                # Field('id_consulta', 'reference consultas',
                #       readable=False, writable=False),
                Field('data_criacao', type='date', default=request.now,
                      requires=IS_DATE(format='%d/%m/%Y')),
                Field('texto', type='text'),
                Field('remedios', requires=IS_IN_SET(remedios, multiple=True),
                      widget=SQLFORM.widgets.checkboxes.widget),
                )

