# -*- coding: utf-8 -*-

ufs = ['SP', 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
        'MT', 'MS', 'MG', 'PR', 'PB', 'PA', 'PE', 'PI', 'RJ', 'RN', 'RS',
          'RO', 'RR', 'SC', 'SE', 'TO']

escolaridade = ['Nenhuma', '1º grau', '2º grau', 'Superior']
cor = ['Branca', 'Negra', 'Parda', 'Indígena', 'Asiática']
estadocivil = ['Casada', 'Solteira (sem união estável)', 'Solteira (com união estável)', 'Outra']
sexo = ['Feminino', 'Masculino']

# Configurações da clínica
CC_nome_clinica = 'Clínica de urologia do Lucas'
CC_nome_medico = 'Lucas Augusto de Morais'
CC_especialidade = 'Urologista'
CC_crm = '666.666.666-24'
CC_telefone = '(14) 998361111'
CC_endereco = 'Rua Getúlio Vargas, 560, centro.'


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
