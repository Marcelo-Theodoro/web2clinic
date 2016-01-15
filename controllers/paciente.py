# -*- coding: utf-8 -*-


@auth.requires_login()
def cadastro():
    if request.vars['editar']:
        editar_id = request.vars['editar']
        editar_paciente = db(db.pacientes.id == editar_id).select().first()
        if not editar_paciente:
            # id informado não existe
            raise HTTP(404)
    else:
            # Cadastro de novo paciente
        editar_paciente = False

    # Caso editar seja True, utiliza a sintaxe de update do sqlform,
    # caso editar seja False, utiliza a sintaxe
    # de criação de novo cadastro
    form = SQLFORM(db.pacientes if not editar_paciente
                   else db.pacientes, upload=URL('download'),
                   record=editar_paciente)
    if form.process().accepted:
        id = form.vars.id
        redirect(URL(c='paciente', f='paciente', args=id), client_side=True)
    return locals()


@auth.requires_login()
def paciente():
    id_paciente = request.args(0) or redirect(URL(c='paciente',
                                                    f='pacientes'),
                                              client_side=True)
    paciente = db(db.pacientes.id == id_paciente).select().first()
    if not paciente:
        raise HTTP(404)
    if paciente.nascimento:
        paciente.nascimento = paciente.nascimento.strftime('%d/%m/%Y')
    agendamentos = db(db.agendamentos.id_paciente == paciente.id).select()
    return locals()


@auth.requires_login()
def pacientes():
    links = [lambda row: A(SPAN('Visualizar',
                                _class='icon magnifier icon-zoom-in\
                                        glyphicon glyphicon-zoom-in'),
                           _class='button btn btn-default',
                           _href=URL(c='paciente', f='paciente',
                                     args=[row.id])),
             lambda row: A(SPAN('Editar',
                                _class='icon pen icon-pencil\
                                        glyphicon glyphicon-pencil'),
                           _class='button btn btn-default',
                           _href=URL(c='paciente', f='cadastro',
                                     vars = {'editar': row.id}))]
    grid = SQLFORM.grid(db.pacientes,
                        fields=[db.pacientes.nome, db.pacientes.nascimento,
                                db.pacientes.sexo],
                        csv=False, links=links, details=False, create=False,
                        editable=False, deletable=True, paginate=10)
    return locals()

@auth.requires_login()
def download():
    return response.download(request, db)
