# -*- coding: utf-8 -*-

from gluon.tools import Auth


db = DAL('sqlite://storage.sqlite')


response.formstyle = 'bootstrap3_stacked'
response.form_label_separator = ''


auth = Auth(db)
auth.settings.actions_disabled.append('register')
auth.settings.actions_disabled.append('request_reset_password')
auth.settings.actions_disabled.append('reset_password')
auth.settings.actions_disabled.append('retrieve_password')
auth.settings.actions_disabled.append('email_reset_password')
auth.settings.actions_disabled.append('change_password')


auth.define_tables(username=True, signature=False)


auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

