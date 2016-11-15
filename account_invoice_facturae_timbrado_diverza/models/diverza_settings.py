# -*- coding: utf-8 -*-
from openerp import models, fields, api

class DiverzaConfigSettings(models.TransientModel):
	_inherit = 'account.config.settings'
	_name = 'diverza.config.settings'

	diverza_url_emision = fields.Char(string="URL de emisión")
	diverza_url_emision_completa = fields.Char(string="URL de emisión completa")
	diverza_url_cancelacion = fields.Char(string="URL de cancelación")
	diverza_token = fields.Char(string="Token")


	@api.model
	def get_default_company_values(self, fields):
		company = self.env.user.company_id
		return {
			'diverza_url_emision' : company.diverza_url_emision,
			'diverza_url_emision_completa' : company.diverza_url_emision_completa,
			'diverza_url_cancelacion' : company.diverza_url_cancelacion,
			'diverza_token' : company.diverza_token
		}

	@api.one
	def set_company_values(self):
		company = self.env.user.company_id
		company.diverza_url_emision = self.diverza_url_emision
		company.diverza_url_emision_completa = self.diverza_url_emision_completa
		company.diverza_url_cancelacion = self.diverza_url_cancelacion
		company.diverza_token = self.diverza_token