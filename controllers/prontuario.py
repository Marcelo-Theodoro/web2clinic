# -*- coding: utf-8 -*-

def ficha():
    import re
    id_ficha = request.args(0) or redirect(URL(c='consulta',
                                               f='todas_consultas'))
    ficha = db(db.fichas.id == id_ficha).select().first()
    if not ficha:
        raise HTTP(404)
    paciente = db(db.pacientes.id == ficha.id_paciente).select().first()
    paciente.nascimento = paciente.nascimento.strftime('%d/%m/%Y')
    consulta = db(db.consultas.id == ficha.id_consulta).select().first()
    consulta.dia = consulta.dia.strftime('%d/%m/%Y')
    tipo_consulta = [i for i in tipos_consultas
                     if i['form'] == ficha.tipo_consulta][0]
    if re.match('db.ficha_([a-z]+|_+[a-z]+)|db.retorno', tipo_consulta['base']):
        base = eval(tipo_consulta['base'])
    else:
        raise HTTP(403)
    formulario = db(base.id == ficha.id_form).select().first()
    response.view = tipo_consulta['view_prontuario']
    return locals()











