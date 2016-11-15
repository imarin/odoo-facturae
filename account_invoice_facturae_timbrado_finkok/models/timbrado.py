# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import UserError
from suds.client import Client

import logging
_logger = logging.getLogger(__name__)

class account_invoice(models.Model):
	_inherit = 'account.invoice'

	def timbrar(self, xml_base64):
		
		# Username and Password, assigned by FINKOK
		company = self.env.user.company_id

		if not company.finkok_username or not company.finkok_password or not company.finkok_url:
			raise UserError("Error en credenciales de Finkok")

		client = Client(company.finkok_url, cache=None)
		_logger.info("xml_base64")

		contenido = client.service.stamp(xml_base64, company.finkok_username, company.finkok_password)

		xml_string = ''
		
		if contenido.Incidencias:
			msg = ""
			for incidencia in contenido.Incidencias:
				msg += "\tIdIncidencia = " + str(incidencia[1][0].IdIncidencia) + "\n"
				msg += "\tUuid = " + str(incidencia[1][0].Uuid) + "\n"
				msg += "\tCodigoError = " + str(incidencia[1][0].CodigoError) + "\n"
				msg += "\tWorkProcessId = " + str(incidencia[1][0].WorkProcessId) + "\n"
				msg += "\tMensajeIncidencia = " + incidencia[1][0].MensajeIncidencia + "\n"
				msg += "\tRfcEmisor = " + str(incidencia[1][0].RfcEmisor) + "\n"
				msg += "\tNoCertificadoPac = " + str(incidencia[1][0].NoCertificadoPac) + "\n"
				msg += "\tFechaRegistro = " + str(incidencia[1][0].FechaRegistro)

			raise UserError("Error al timbrar: \n\n" + msg)
		
		xml_string = contenido.xml.encode("utf-8")

		_logger.info("------------********----------------")
		_logger.info(xml_string)
		_logger.info("------------********----------------")
			
		return xml_string