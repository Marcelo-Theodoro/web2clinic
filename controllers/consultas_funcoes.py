
def buscar_paciente(id):
    paciente = db(db.pacientes.id == id).select().first()
    return paciente


def buscar_agendamento(id):
    agendamento = db(db.agendamentos.id == id).select().first()
    return agendamento


def buscar_consulta(id):
    consulta = db(db.consultas.id == id).select().first()
    return consulta


def buscar_atestado(id):
    atestado = db(db.atestados.id == id).select().first()
    return atestado


def buscar_atestados(id):
    atestado = db(db.atestados.id_paciente == id).select()
    return atestado


def buscar_consulta_paciente(id):
    consulta = db(db.consultas.id_paciente == id).select()
    return consulta


def buscar_prescricao(id):
    prescricao = db(db.prescricoes.id == id).select().first()
    return prescricao


def buscar_prescricoes_paciente(id):
    prescricoes = db(db.prescricoes.id_paciente == id).select()
    return prescricoes


def buscar(base, id):
    bases = ['paciente',
            'agendamento',
            'consulta',
            'consulta_paciente',
            'atestado',
            'atestados',
            'prescricao',
            'prescricoes_paciente']
    if base not in bases:
        raise HTTP(403)
    try:
        if base == 'paciente':
            dados = buscar_paciente(id)
        elif base == 'agendamento':
            dados = buscar_agendamento(id)
        elif base == 'consulta':
            dados = buscar_consulta(id)
        elif base == 'consulta_paciente':
            dados = buscar_consulta_paciente(id)
        elif base == 'atestado':
            dados = buscar_atestado(id)
        elif base == 'atestados':
            dados = buscar_atestados(id)
        elif base == 'prescricao':
            dados = buscar_prescricao(id)
        elif base == 'prescricoes_paciente':
            dados = buscar_prescricoes_paciente(id)
        else:
            raise HTTP(404)

        if not dados:
            raise HTTP(404)
    except ValueError:
        raise HTTP(404)
    return dados
