tipos_consultas = [
                   dict(form='ficha_clinica_mulher',
                        label='Ficha Clínica Mulher',
                        base=db.ficha_clinica_mulher,
                        view_form='pacientes/fichas/ficha_clinica_mulher.html',
                        view_prontuario='pacientes/prontuarios/prontuario_mulher.html'),

                   dict(form='ficha_clinica_de_climaterio',
                        label='Ficha Clíninica de Climaterio',
                        base=db.ficha_clinica_de_climaterio,
                        view_form='pacientes/fichas/ficha_clinica_de_climaterio.html',
                        view_prontuario='pacientes/prontuarios/prontuario_climaterio.html'),

                   dict(form='ficha_clinica_de_anticoncepcao',
                        label='Ficha Clínica de Anticoncepção',
                        base=db.ficha_clinica_de_anticoncepcao,
                        view_form='pacientes/fichas/ficha_clinica_de_anticoncepcao.html',
                        view_prontuario='pacientes/prontuarios/prontuario_de_anticoncepcao.html'),

                   dict(form='ficha_clinica_mastologia',
                        label='Ficha Clínica de Mastologia',
                        base=db.ficha_clinica_mastologia,
                        view_form='pacientes/fichas/ficha_clinica_mastologia.html',
                        view_prontuario='pacientes/prontuarios/prontuario_de_mastologia.html'),

                   dict(form='ficha_clinica_parto_e_puerperio',
                        label='Ficha Clínica de parto e Puerperio',
                        base=db.ficha_clinica_parto_e_puerperio,
                        view_form='pacientes/fichas/ficha_clinica_parto_e_puerperio.html',
                        view_prontuario='pacientes/prontuarios/prontuario_parto_e_puerperio.html'),

                   dict(form='ficha_clinica_pre_natal',
                        label='Ficha Clínica de Pré Natal',
                        base=db.ficha_clinica_pre_natal,
                        view_form='pacientes/fichas/ficha_clinica_pre_natal.html',
                        view_prontuario='pacientes/prontuarios/'), # TODO

                   dict(form='ficha_clinica_de_uroginecologia',
                        label='Ficha Clínica de Uroginecologia',
                        base=db.ficha_clinica_de_uroginecologia,
                        view_form='pacientes/fichas/ficha_clinica_de_uroginecologia.html',
                        view_prontuario='pacientes/prontuarios/prontuario_de_uroginecologia.html'),

                   dict(form='ficha_de_anticoncepcao',
                        label='Ficha de Anticoncepção',
                        base=db.ficha_de_anticoncepcao,
                        view_form='pacientes/fichas/ficha_de_anticoncepcao.html',
                        view_prontuario='pacientes/prontuarios/prontuario_anticoncepcao.html'),
                  ]
