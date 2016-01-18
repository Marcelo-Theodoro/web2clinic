# -*- coding: utf-8 -*-

@auth.requires_login()
def gerar_prescricao():
    id_consulta = request.args(0)

    consulta = BuscaConsulta(id_consulta)

    paciente = BuscaPaciente(consulta.id_paciente)

    lista_medicamentos = db(db.lista_medicamentos).select()
    for medicamento in lista_medicamentos:
        medicamento.nome_sanitizado = ''.join(s for s in medicamento.nome if s.isalnum())
        if medicamento.fichas:
            medicamento.fichas = medicamento.fichas.replace('|', ' ')
        else:
            medicamento.fichas = ''
    if not lista_medicamentos:
        lista_medicamentos = []

    form = SQLFORM(db.prescricoes)
    form.vars.id_paciente = paciente.id
    form.vars.id_consulta = consulta.id

    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='prescricao', f='prescricao', args=id),
                 client_side=True)
    return locals()


@auth.requires_login()
def prescricao():
    id_prescricao = request.args(0)
    prescricao = BuscaPrescricao(id_prescricao)
    paciente = BuscaPaciente(prescricao.id_paciente)

    prescricao.uso_interno = [] # Uso interno
    prescricao.uso_externo = [] # Uso externo
    prescricao.uso_local = [] # Uso local
    prescricao.uso_transdermico = [] # Uso transdérmico
    prescricao.uso_sublingual = [] # Uso sublingual
    prescricao.sem_categoria = []

    for medicamento in prescricao.medicamentos:
        medicamento = medicamento.split('|||')
        nome = medicamento[0]
        texto = medicamento[1]
        categoria = medicamento[2]
        medicamento = {'nome': nome, 'texto': texto}

        if categoria == 'Uso interno':
            prescricao.uso_interno.append(medicamento)
        elif categoria == 'Uso externo':
            prescricao.uso_externo.append(medicamento)
        elif categoria == 'Uso local':
            prescricao.uso_local.append(medicamento)
        elif categoria == 'Uso transdérmico':
            prescricao.uso_transdermico.append(medicamento)
        elif categoria == 'Uso sublingual':
            prescricao.uso_sublingual.append(medicamento)
        else:
            prescricao.sem_categoria.append(medicamento)

    return locals()


@auth.requires_login()
def prescricoes():
    id_paciente = request.args(0)
    if id_paciente:
        paciente = db(db.pacientes.id == id_paciente).select().first()
        if not paciente:
            raise HTTP(404)
    db.prescricoes.id_paciente.readable = True
    haders = {'prescricoes.id_paciente': 'Paciente'}
    links = [lambda row: A(SPAN('Visualizar',
                                _class='icon magnifier icon-zoom-in\
                                        glyphicon glyphicon-zoom-in'),
                           _class='button btn btn-default',
                           _href=URL(c='prescricao', f='prescricao.html',
                                     args=[row.id]))]
    grid = SQLFORM.grid(db.prescricoes.id_paciente == paciente.id
                        if id_paciente else db.prescricoes,
                        fields=[db.prescricoes.id_paciente,
                                db.prescricoes.data_criacao],
                        args=request.args[:1],
                        csv=False,
                        user_signature=False,
                        headers=haders,
                        details=False,
                        links=links,
                        editable=False,
                        deletable=False,
                        create=False,
                        searchable=False,
                        paginate=10)
    return locals()
