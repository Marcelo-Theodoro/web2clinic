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
    id_paciente = request.args(0)
    paciente = BuscaPaciente(id_paciente)
    agendamentos = db(db.agendamentos.id_paciente == paciente.id).select()
    return locals()


@auth.requires_login()
def pacientes():
    pacientes = BuscaTodosPacientes()
    
    return locals()

@auth.requires_login()
def pesquisa():
    pesquisa = request.args(0)
    if pesquisa:
        pacientes = db(db.pacientes.nome.contains(pesquisa)).select() or db(db.pacientes.cpf.contains(pesquisa)).select()
    else:
        pacientes = db(db.pacientes).select()

    return locals()


@auth.requires_login()
def download():
    return response.download(request, db)
