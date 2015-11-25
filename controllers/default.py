# -*- coding: utf-8 -*-
# TODO: agendamentos por dia, agendamentos por mês, consultas hoje, consultas neste mês

def user():
    return dict(form=auth())

@auth.requires_login()
def index():
    from datetime import datetime
    data = datetime.now().date()
    mes = datetime.now().date().strftime(format='%m/%Y')
    # Consultas
    pacientes = db(db.pacientes).select()
    agendamentos = db(db.agendamentos).select()
    consultas = db(db.consultas).select()
    # Total pacientes cadastrados
    total_pacientes =  len(pacientes)
    # Total de agendamentos
    total_agendamentos = len(agendamentos)
    # Total de consultas
    total_consultas = len(consultas)
    # Total agendamentos do dia
    qtd_agendamentos_dia = len([i for i in agendamentos
                                if i.dia == data])
    # Total agendamentos mês
    qtd_agendamentos_mes = len([i for i in agendamentos
                                if i.dia.strftime(format='%m/%Y') == mes])
    # Total consultas do dia
    qtd_consultas_dia = len([i for i in consultas
                                if i.dia == data])
    # Total consultas mês
    qtd_consultas_mes = len([i for i in consultas
                                if i.dia.strftime(format='%m/%Y') == mes])

    itens = [i['form'] for i in tipos_consultas]
    lista = []
    for item in itens:
        qtd_consultas = len(db(db.consultas.tipo_consulta == item).select())
        if qtd_consultas:
            label = [i['label'] for i in tipos_consultas
                     if item == i['form']][0]
            lista.append({'label': label, 'qtd': qtd_consultas})
    return locals()

