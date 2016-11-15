# -*- coding: utf-8 -*-
from openerp import models, fields, api

class res_company(models.Model):
	_inherit = 'res.company'

	diverza_url_emision = fields.Char(string="URL de emisión")
	diverza_url_emision_completa = fields.Char(string="URL de emisión completa")
	diverza_url_cancelacion = fields.Char(string="URL de cancelación")
	diverza_token = fields.Char(string="Token")