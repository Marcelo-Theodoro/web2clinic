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


db.define_table('pacientes',
                Field('nome', label='Nome', requires=IS_NOT_EMPTY()),
                Field('sexo', label='Sexo', default='Feminino', requires=IS_IN_SET(sexo)),
                Field('cpf', label='CPF'),
                Field('profissao', label='Profissão'),
                Field('nascimento', label='Data de nascimento', type='date',
                    requires=[IS_NOT_EMPTY(), IS_DATE(format='%d/%m/%Y')]),
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
    if paciente.endereco == None or paciente.endereco == '':
        paciente.endereco = NI
    if paciente.cidade == None or paciente.cidade == '':
        paciente.cidade = NI
    if paciente.telefone == None or paciente.telefone == '':
        paciente.telefone = NI
    if paciente.escolaridade == None or paciente.escolaridade == '':
        paciente.escolaridade = NI
    if paciente.observacoes == None or paciente.observacoes == '':
        paciente.observacoes = NI
    if paciente.cpf == None or paciente.cpf == '':
        paciente.cpf = NI
    if paciente.uf == None or paciente.uf == '':
        paciente.uf = NI
    if paciente.estadocivil == None or paciente.estadocivil == '':
        paciente.estadocivil = NI
    if paciente.cor == None or paciente.cor == '':
        paciente.cor = NI
    if paciente.cep == None or paciente.cep == '':
        paciente.cep = NI
    return paciente


def BuscaTodosPacientes():
    pacientes = db(db.pacientes).select()
    return pacientes



