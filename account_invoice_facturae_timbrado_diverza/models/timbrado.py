# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import UserError
import requests
import base64
from lxml import etree as ET

import logging
_logger = logging.getLogger(__name__)

class account_invoice(models.Model):
	_inherit = 'account.invoice'

	def timbrar(self, xml_base64):
		company = self.env.user.company_id
		xml_str = base64.b64decode(xml_base64)
		url = company.diverza_url_emision_completa
		headers = { "x-auth-token": company.diverza_token }
		r = requests.post(url, headers=headers, data=xml_str)
		if r.status_code == requests.codes.ok:
			_logger.info("r.text")
			_logger.info(r.text)
			return r.text.encode("utf-8")
		else:
			raise UserError("Error al timbrar con diverza")

	def cancelar_timbre(self, emisor_rfc, uuid):
		company = self.env.user.company_id
		url = '%s/%s/%s' % (company.diverza_url_cancelacion,emisor_rfc, uuid)
		headers = { "x-auth-token": company.diverza_token }
		r = requests.post(url, headers=headers)
		_logger.info("r")
		_logger.info(r)
		_logger.info(r.text)
		if r.status_code == requests.codes.ok:
			return True
		else:
			raise UserError("Error al cancelar timbre con diverza")
