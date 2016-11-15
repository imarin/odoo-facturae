# -*- coding: utf-8 -*-
from openerp import models, fields, api

class FinkokConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'
    _name = 'finkok.config.settings'

    finkok_username = fields.Char(string="Usuario de finkok")
    finkok_password = fields.Char(string="Contraseña de finkok")
    finkok_url = fields.Char(string="URL de finkok")

    @api.model
    def get_default_company_values(self, fields):
    	company = self.env.user.company_id
    	return {
    		'finkok_username' : company.finkok_username,
    		'finkok_password' : company.finkok_password,
    		'finkok_url' : company.finkok_url
    	}

    @api.one
    def set_company_values(self):
    	company = self.env.user.company_id
    	company.finkok_username = self.finkok_username
    	company.finkok_password = self.finkok_password
    	company.finkok_url = self.finkok_url