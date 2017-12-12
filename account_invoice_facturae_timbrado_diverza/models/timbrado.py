# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import UserError
from collections import OrderedDict
import requests
import base64
from lxml import etree as ET
import json

import logging
_logger = logging.getLogger(__name__)

class account_invoice(models.Model):
	_inherit = 'account.invoice'

	def timbrar(self, xml_base64, refid):
		# raise UserError(xml_base64)
		company = self.env.user.company_id
		# xml_str = base64.b64decode(xml_base64)
		url = company.diverza_url_emision
		headers = { "Content-Type": 'application/json' }
		body = OrderedDict([
			('credentials',{
				"id": company.diverza_id,
				"token": company.diverza_token
			}),
			('issuer', {
				"rfc": company.vat[2:]
			}), 
			('document', {
				"ref-id": refid,
				"certificate-number": company.numero_certificado,
				"section": "all",
				"format": "xml",
				"template": "letter",
				"type": "application/vnd.diverza.cfdi_3.3+xml",
				"content": xml_base64
			})])
		# _logger.info(json.dumps(body, sort_keys=False))
		r = requests.post(url, headers=headers, data=json.dumps(body, sort_keys=False))
		j = json.loads(r.text)
		if not "uuid" in j:
			_logger.info(r.text);
			raise UserError("Error al timbrar con diverza\n\nCode: %s\nMessage: %s\nDetails: %s" % (j["code"], j["message"], j["error_details"]))
		else:
			xml_str = base64.b64decode(j["content"])
			return xml_str

	def cancelar_timbre(self, emisor_rfc, uuid):
		company = self.env.user.company_id
		url = company.diverza_url_cancelacion.replace("UUID", uuid)
		headers = { "Content-Type": 'application/json' }
		body = OrderedDict([
			('credentials',{
				"id": company.diverza_id,
				"token": company.diverza_token
			}),
			('issuer', {
				"rfc": company.vat[2:]
			}),
			('document', {
				"certificate-number": company.numero_certificado,
			})
		]);
		r = requests.put(url, headers=headers, data=json.dumps(body, sort_keys=False))
		_logger.info(r.text)
		j = json.loads(r.text)
		if not "code" in j:
			return True
		else:
			raise UserError("Error al cancelar timbre con diverza\n\nCode: %s\nMessage: %s\nDetails: %s" % (j["code"], j["message"], j["error_details"]))
