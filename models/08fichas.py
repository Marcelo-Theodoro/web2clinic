# -*- coding: utf-8 -*-


db.define_table('fichas',
                Field('id_paciente', 'reference pacientes',
                    readable=False, writable=False),
                Field('id_consulta', 'reference consultas',
                      readable=False, writable=False),
                Field('tipo_consulta'),
                Field('id_form'),
                )


def BuscaFicha(id):
    # Recebe id da ficha
    if not id:
        raise HTTP(404, 'ID ficha não encontrado')
    try:
        ficha = db(db.fichas.id == id).select().first()
    except ValueError:
        raise HTTP(404, 'ID ficha inválido')
    if not ficha:
        raise HTTP(404, 'Ficha não encontrada')
    return ficha

def BuscaTodasFichasConsulta(id):
    # Recebe id da consulta
    if not id:
        raise HTTP(404, 'ID inválido')
    fichas = db(db.fichas.id_consulta == id).select()
    return fichas
