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
tipo = ['Particular', 'Convênio']


db.define_table('pacientes',
                Field('nome', label='Nome', requires=IS_NOT_EMPTY()),
                Field('sexo', label='Sexo', default='Feminino', requires=IS_IN_SET(sexo)),
                Field('cpf', label='CPF'),
                Field('profissao', label='Profissão'),
                Field('nascimento', label='Data de nascimento', type='date',
                    requires=[IS_NOT_EMPTY(), IS_DATE(format='%d/%m/%Y')]),
                Field('telefone', label='Telefone', requires=IS_NOT_EMPTY()),
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
                Field('tipo', label='Tipo de atendimento', requires=IS_IN_SET(tipo)),
                format='%(nome)s'
                )

db.pacientes.cpf.represent = lambda field, x: field if field else 'Não informado'


def BuscaPaciente(id):
    if not id:
        raise HTTP(404, 'ID paciente não encontrado')
    try:
        paciente = db(db.pacientes.id == id).select().first()
    except ValueError:
        raise HTTP(404, 'Argumento PACIENTE inválido')
    if not paciente:
        raise HTTP(404, 'Paciente não encontrado')
    if paciente.nascimento:
        paciente.nascimento = paciente.nascimento.strftime('%d/%m/%Y')

    NI = 'Não informado'

    campos = []

    campos.append(paciente.endereco)
    campos.append(paciente.cidade)
    campos.append(paciente.telefone)
    campos.append(paciente.escolaridade)
    campos.append(paciente.observacoes)
    campos.append(paciente.cpf)
    campos.append(paciente.uf)
    campos.append(paciente.estadocivil)
    campos.append(paciente.cor)
    campos.append(paciente.cep)

    for campo in campos:
    	if not campo:
    		campo = NI

    return paciente


def BuscaTodosPacientes():
    pacientes = db(db.pacientes).select()
    return pacientes



