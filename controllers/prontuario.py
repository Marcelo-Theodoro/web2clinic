# -*- coding: utf-8 -*-

def ficha():
    import re
    id_ficha = request.args(0)

    ficha = BuscaFicha(id_ficha)
    paciente = BuscaPaciente(ficha.id_paciente)
    consulta = BuscaConsulta(ficha.id_consulta)
    tipo_consulta = TipoConsultaFormParaDict(ficha.tipo_consulta)
    if consulta.id_agendamento != 'NaoAgendado':
        agendamento = True
        pre_consulta_agendamento = BuscaPreConsultaAgendamento(consulta.id_agendamento)
    else:
        agendamento = False

    if re.match('db.ficha_([a-z]+|_+[a-z]+)|db.retorno', tipo_consulta['base']):
        base = eval(tipo_consulta['base'])
    else:
        raise HTTP(403)
    formulario = db(base.id == ficha.id_form).select().first()
    if tipo_consulta['form']  == 'retorno':
        if formulario.data:
            formulario.data = formulario.data.strftime(format='%d/%m/%Y')
    response.view = tipo_consulta['view_prontuario']
    return locals()











