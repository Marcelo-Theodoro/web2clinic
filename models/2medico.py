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
                Field('nome', label='Nome', requires=IS_NOT_EMPTY()),
                Field('sexo', label='Sexo', default='Feminino', requires=IS_IN_SET(sexo)),
                Field('cpf', label='CPF'),
                Field('profissao', label='Profissão'),
                Field('nascimento', label='Data de nascimento', type='date',
                    requires=IS_EMPTY_OR(IS_DATE(format='%d-%m-%Y'))),
                Field('telefone', label='Telefone'),
                Field('escolaridade', label='Escolaridade',
                    requires=IS_EMPTY_OR(IS_IN_SET(escolaridade))),
                Field('estadocivil', label='Estado civil',
                    requires=IS_EMPTY_OR(IS_IN_SET(estadocivil))),
                Field('cor', label='Cor',
                      requires=IS_EMPTY_OR(IS_IN_SET(cor))),
                Field('image', 'upload', label='Foto'),
                Field('endereco', label='Endereço'),
                Field('cidade', label='Cidade'),
                Field('uf', label='UF', default='SP',
                      requires=IS_EMPTY_OR(IS_IN_SET(ufs))),
                Field('cep', label='CEP'),
                Field('observacoes', label='Observações', type='text'),
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
                Field('dia', type='date', requires=IS_DATE()),
                Field('hora_inicio', requires=IS_TIME()),  # TODO: testar se consigo tempo total
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
                Field('data_criacao', type='date', default=request.now,
                      requires=IS_DATE(format='%d/%m/%Y')),
                Field('texto', type='text'),
                Field('remedios', requires=IS_IN_SET(remedios, multiple=True),
                      widget=SQLFORM.widgets.checkboxes.widget),
                )

