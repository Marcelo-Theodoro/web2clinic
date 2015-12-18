# -*- coding: utf-8 -*-
# Transformar um agendamento em uma consulta? Maybe.
# Ou então, a consulta ser criada antes de dar o submit na primeira ficha.
# Dessa maneira é possível, por exemplo, que o usuário crie um atestado antes
# da ficha, ou só solicite um exame.


@auth.requires_login()
def consulta():
    # Tipo de consulta deve ser o primeiro args na URL
    tipo_consulta = request.args(0) or redirect(URL(c='consulta',
                                                    f='todas_consultas'))
    # Seguido pelo ID do paciente
    id_paciente = request.args(1) or redirect(URL(c='consulta',
                                                 f='todas_consultas'))

    # Usando o args(0), busca um dict com todas as infos do
    # tipo de consulta em questão
    tipo_consulta = [i for i in tipos_consultas
                     if tipo_consulta == i['form']][0]
    # Busca paciente
    paciente = db(db.pacientes.id == id_paciente).select().first()
    paciente.nascimento = paciente.nascimento.strftime(format='%d/%m/%Y')
    # Se houver a váriável "agendamento" na URL
    if request.vars['agendamento']:
        # Busca o agendamento e guarda em "agendamento"
        id_agendamento = request.vars['agendamento']
        agendamento = db(db.agendamentos.id == id_agendamento).select().first()
    else:
        id_agendamento = False
    # Cria o form
    base = eval(tipo_consulta['base'])
    form = SQLFORM(base)
    # Selecionar a view para edição
    response.view = tipo_consulta['view_form']
    # Inputa o ID do paciente no form
    form.vars.id_paciente = paciente.id

    if form.process().accepted:
        id_form = form.vars.id
         # Faz o registro da consulta
        id_consulta = db.consultas.insert(id_paciente=paciente.id,
                                      dia=request.now,
                                      hora_inicio=request.now,
                                      hora_fim=request.now)
        # Faz o registro da ficha
        id_ficha = db.fichas.insert(id_paciente=paciente.id,
                                    id_consulta=id_consulta,
                                    tipo_consulta = tipo_consulta['form'],
                                    id_form=id_form)
        # Se houver agendamento, deleta
        if id_agendamento:
            db(db.agendamentos.id == id_agendamento).delete()
        redirect(URL(c='consulta', f='ver_consulta', args=id_consulta),
                 client_side=True)
    return locals()

def editar_ficha():
    # Falta os html's e testar
    tipo_consulta = request.args(0) or redirect(URL(c='consulta',
                                                    f='todas_consultas'))
    id_consulta = request.args(1) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    ficha_id = request.vars['editar'] or redirect(URL(c='consulta',
                                                        f='todas_consultas'))
    # Busca o dicionário para o tipo de consulta selecionado em args(0)
    tipo_consulta = [i for i in tipos_consultas
                     if i == tipos_consultas][0]
    # Busca a consulta
    consulta = db(db.consultas.id == id_consulta).select().first()
    # Busca o paciente
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    paciente.nascimento = paciente.nascimento.strftime(format='%d/%m/%Y')
    # Define a base usando o dict.
    base = eval(tipo_consulta['base'])
    # Busca a ficha que vai ser atualizada
    ficha = db(u_base.id == u_ficha_id).select().first()
    # Cria o form para update da ficha
    form = SQLFORM(tipo_consulta['base'], update=ficha)
    # Selecionar a view para edição
    response.view = tipo_consulta['view_form']
    # Inputa o ID do paciente no form
    form.vars.id_paciente = paciente.id

    if form.process().accepted:
        redirect(URL(c='consulta', f='ver_consulta', args=consulta.id),
                 client_side=True)
    return locals()


@auth.requires_login()
def consultas():
    id_paciente = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    paciente = db(db.pacientes.id == id_paciente).select().first()
    consultas = db(db.consultas.id_paciente == id_paciente).select()
    for consulta in consultas:
        consulta.dia = consulta.dia.strftime(format='%d/%m/%Y')
    return locals()


@auth.requires_login()
def nova_consulta():
    links = [lambda row: A('Iniciar consulta', _class='button btn\
                                                       btn-default',
                           _href=URL(c='consulta', f='consultar',
                                     args=[row.id]))]
    grid = SQLFORM.grid(db.pacientes,
                        fields=[db.pacientes.nome, db.pacientes.cpf],
                        links=links, csv=False, editable=False,
                        deletable=False, details=False, create=False,
                        paginate=10)
    return locals()


@auth.requires_login()
def consultar():
    id_paciente = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    paciente = db(db.pacientes.id == id_paciente).select().first()
    form = SQLFORM.factory(Field('tipo_consulta',
                                 requires=IS_IN_SET([i['label'] for i in
                                                    tipos_consultas])))
    if form.process().accepted:
        tipo_consulta = form.vars.tipo_consulta
        tipo_consulta_form = [i['form'] for i in tipos_consultas
                              if tipo_consulta == i['label']][0]
        redirect(URL(c='consulta', f='consulta',
                 args=[tipo_consulta_form, id_paciente]), client_side=True)
    return locals()


@auth.requires_login()
def todas_consultas():
    links = [lambda row: A('Ver consulta', _class='button btn btn-default',
                           _href=URL(c='consulta', f='ver_consulta',
                                     args=[row.id]))]
    haders = {'consultas.id_paciente': 'Paciente'}
    db.consultas.id_paciente.readable = True
    form = SQLFORM.grid(db.consultas,
                        fields=[db.consultas.id_paciente,
                                db.consultas.dia],
                        csv=False, editable=False, deletable=False,
                        details=False, create=False, links=links,
                        headers=haders, paginate=10)
    return locals()


@auth.requires_login()
def ver_consulta():
    id_consulta = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    consulta = db(db.consultas.id == id_consulta).select().first()
    if not consulta:
        raise HTTP(404)
    fichas = db(db.fichas.id_consulta == consulta.id).select()
    # Retorna objeto fichas que traz, bom, todas as fichas.
    for ficha in fichas:
        ficha.tipo_consulta = [i for i in tipos_consultas
                                  if ficha.tipo_consulta == i['form']][0]
        ficha.label = ficha.tipo_consulta['label']
        ficha.form = ficha.tipo_consulta['form']
    consulta.dia = consulta.dia.strftime(format='%d/%m/%Y')
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    atestados = db(db.atestados.id_consulta == consulta.id).select()
    exames = db(db.exames.id_consulta == consulta.id).select()
    prescricoes = db(db.prescricoes.id_consulta == consulta.id).select()
    return locals()


@auth.requires_login()
def apagar_consulta():
    id_consulta = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    consulta = db(db.consultas.id == id_consulta).select().first()
    if not consulta:
        raise HTTP(404)
    consulta.dia = consulta.dia.strftime(format='%d/%m/%Y')
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    fichas = db(db.fichas.id_consulta == consulta.id).select()
    form = SQLFORM.factory()
    if form.process().accepted:
        # Deletas as fichas associadas
        for ficha in fichas:
            base_consulta = [i['base'] for i in tipos_consultas
                            if i['form'] == ficha.tipo_consulta][0]
            db(base_consulta.id == ficha.id_form).delete()
        # Deleta os registros das fichas
        db(db.fichas.id_consulta == consulta.id).delete()
        # Deleta prescrições associadas a consulta
        db(db.prescricoes.id_consulta == consulta.id).delete()
        # Deleta atestados associados a consulta
        db(db.atestados.id_consulta == consulta.id).delete()
        # Deleta exames associados a consulta
        db(db.exames.id_consulta == consulta.id).delete()
        # Delete a consulta
        db(db.consultas.id == consulta.id).delete()
        redirect(URL(c='consulta', f='todas_consultas'))
    return locals()


