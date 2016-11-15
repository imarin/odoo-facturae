# -*- coding: utf-8 -*-
from openerp import models, fields, api

class res_company(models.Model):
	_inherit = 'res.company'

	finkok_username = fields.Char()
	finkok_password = fields.Char()
	finkok_url = fields.Char()