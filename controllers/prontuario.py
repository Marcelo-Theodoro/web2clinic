# -*- coding: utf-8 -*-

def prontuario_consulta():
    id_consulta = request.args(0) or redirect(URL(c='consulta',
                                                  f='todas_consultas'))
    consulta = db(db.consultas.id == id_consulta).select().first()
    paciente = db(db.pacientes.id == consulta.id_paciente).select().first()
    tipo_consulta = consulta.tipo_consulta
    ficha = [i['base'] for i in tipos_consultas
             if i['form'] == tipo_consulta][0]
    formulario = db(ficha.id == consulta.id_form).select().first()
    response.view = [i['view_prontuario'] for i in tipos_consultas
                     if i['form'] == tipo_consulta][0]
    return locals()

