from openerp import models, fields, api
from openerp.tools import config
from subprocess import check_output
import base64, os

import logging
_logger = logging.getLogger(__name__)

class res_company(models.Model):
	_inherit = 'res.company'

	achivo_cer = fields.Many2one("ir.attachment", string="Archivo .CER")
	achivo_key = fields.Many2one("ir.attachment", string="Archivo .KEY")
	achivo_pem = fields.Many2one("ir.attachment", string="Archivo .PEM")
	cer_password = fields.Char(string="Password para el CSD:")
	numero_certificado = fields.Char(string="Serie del certificado", readonly=True)

	@api.model
	def generateNumCER(self, cr):
		company = self.browse(cr)
		
		archivo_cer_path = config.filestore(self.env.cr.dbname) + "/" + company.achivo_cer.store_fname

		out = check_output(["openssl", "x509", "-inform", "DER", "-in", archivo_cer_path, "-serial"])
		serial_numbers = out.replace("serial=", "").split("\n")[0]
		numero_certificado = ""
		for idx, num in enumerate(serial_numbers):
			if(idx % 2):
				numero_certificado = numero_certificado + num

		company.numero_certificado = numero_certificado

	@api.model
	def generatePEM(self, cr):
		company = self.browse(cr)
		archivo_cer_path = config.filestore(self.env.cr.dbname) + "/" + company.achivo_cer.store_fname
		archivo_key_path = config.filestore(self.env.cr.dbname) + "/" + company.achivo_key.store_fname
		archivo_pem_path = config.filestore(self.env.cr.dbname) + "/" + company.achivo_key.store_fname + ".pem"

		try:
		    os.remove(archivo_pem_path)
		except OSError:
		    pass

		check_output(["openssl", "x509", "-inform", "DER", "-in", archivo_cer_path, "-outform", "PEM", "-pubkey", "-out", archivo_pem_path])
		check_output(["openssl", "x509", "-in", archivo_pem_path, "-serial", "-noout"])
		check_output(["openssl", "pkcs8", "-inform", "DER", "-in", archivo_key_path, "-passin", "pass:" + company.cer_password, "-out", archivo_pem_path])

		cert_file = open(archivo_pem_path, 'r')
		pem_datas = base64.b64encode(cert_file.read())

		attachment_ids = self.env['ir.attachment'].search([('res_model', '=', 'res.company'),('res_id','=',company.id), ('mimetype','=','application/octet-stream')])
		attachment_ids.unlink()

		pem_file = company.achivo_key.copy()
		pem_file.write({
			'mimetype':'application/octet-stream',
			'datas_fname' : pem_file.datas_fname + ".pem",
			'display_name' : pem_file.display_name + ".pem",
			'name' : pem_file.name + ".pem",
			'datas' : pem_datas
			})
		company.achivo_pem = pem_file

		os.remove(archivo_pem_path)
