# -*- coding: utf-8 -*-

def user():
    return dict(form=auth())

@auth.requires_login()
def index():
    import os
    import shutil
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
        qtd_consultas = len(db(db.fichas.tipo_consulta == item).select())
        if qtd_consultas:
            label = [i['label'] for i in tipos_consultas
                     if item == i['form']][0]
            lista.append({'label': label, 'qtd': qtd_consultas})


    # Backup automático
    DIA = datetime.now().strftime(format='%Y%m%d')
    SRC = '/home/marcelotheodoro/web2py/applications/web2clinic/databases/'
    DST = '/home/marcelotheodoro/teste/{0}'.format(DIA)
    if not os.path.exists(DST):
        try:
            shutil.copytree(SRC, DST)
        except:
            response.flash = '''Falha no backup automático.
                                Entre em contato com o desenvolvedor.'''
    return locals()

