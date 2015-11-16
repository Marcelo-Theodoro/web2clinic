# -*- coding: utf-8 -*-

def index():
    total_pacientes = db(db.pacientes).count()
    total_agendamentos = db(db.agendamentos).count()
    total_consultas = db(db.consultas).count()
    itens = [i['form'] for i in tipos_consultas]
    lista = []
    for item in itens:
        qtd_consultas = len(db(db.consultas.tipo_consulta == item).select())
        if qtd_consultas:
            label = [i['label'] for i in tipos_consultas
                     if item == i['form']][0]
            lista.append({'label': label, 'qtd': qtd_consultas})
    return locals()
