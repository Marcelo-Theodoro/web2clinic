# -*- coding: utf-8 -*-

@auth.requires_login()
def prontuario_consulta():
    id_consulta = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    consulta = db(db.consultas.id == id_consulta).select().first()
    if not consulta:
        raise HTTP(404)
    consulta.dia = consulta.dia.strftime(format='%d/%m/%Y')
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    paciente.nascimento = paciente.nascimento.strftime(format='%d/%m/%Y')
    tipo_consulta = consulta.tipo_consulta
    ficha = [i['base'] for i in tipos_consultas
             if i['form'] == tipo_consulta][0]
    formulario = db(ficha.id == consulta.id_form).select().first()
    response.view = [i['view_prontuario'] for i in tipos_consultas
                     if i['form'] == tipo_consulta][0]
    return locals()

