# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools import config
from lxml import etree as ET
from datetime import datetime
import xml.dom.minidom as minidom
from openerp.exceptions import UserError
from M2Crypto import RSA
import base64
import hashlib
import pytz
from reportlab.graphics.barcode import createBarcodeDrawing
import urllib

import logging
_logger = logging.getLogger(__name__)

class account_invoice(models.Model):
	_inherit = 'account.invoice'

	facturada = fields.Boolean(string="Invoice timbrado", copy=False, readonly=True)
	factura_xml = fields.Many2one("ir.attachment", string="XML de la factura", readonly=True)
	factura_pdf = fields.Many2one("ir.attachment", string="PDF de la factura", readonly=True)
	factura_xml_download = fields.Binary(string="XML de la factura", related='factura_xml.datas')
	factura_xml_fname = fields.Char(related='factura_xml.datas_fname')
	factura_moneda = fields.Char(string="Moneda", readonly=True)
	factura_formapago = fields.Char(string="Forma de pago", readonly=True)
	factura_uuid = fields.Char(string="UUID", readonly=True)
	factura_fecemi = fields.Char(string="Fecha de emision", readonly=True)
	factura_sellosat = fields.Char(string="Sello Sat", readonly=True)
	factura_rfcpac = fields.Char(string="RFC PAC", readonly=True)
	factura_certificado = fields.Char(string="Certificado Sat", readonly=True)
	factura_nocertificado = fields.Char(string="Certificado", readonly=True)
	factura_sello = fields.Char(string="Sello", readonly=True)
	factura_cadena = fields.Char(string="Cadena", readonly=True)
	factura_qr_cadena = fields.Char(string="QR", readonly=True)
	factura_cadena_timbrada = fields.Char(string="Cadena timbrada", readonly=True)
	factura_version = fields.Char(string="Versión", readonly=True)

	def timbrar(self, xml_base64, refid):
		raise UserError("No hay ningún módulo de PAC instalado")

	def cancelar_timbre(self, xml_base64):
		raise UserError("No hay ningún módulo de PAC instalado")

	def sella_xml(self, cfdi, numero_certificado, archivo_cer, archivo_pem, now):
		keys = RSA.load_key(archivo_pem)
		cert_file = open(archivo_cer, 'r')
		cert = base64.b64encode(cert_file.read())
		xdoc = ET.fromstring(cfdi)

		xdoc.attrib['Fecha'] = str(now.isoformat())[:19]

		comp = xdoc.get('Comprobante')
		xdoc.attrib['Certificado'] = cert
		xdoc.attrib['NoCertificado'] = numero_certificado

		cadena_original = self.get_cadena(xdoc, 'cadenaoriginal_3_3.xslt')

		digest = hashlib.new('sha256', str(cadena_original)).digest()
		sello = base64.b64encode(keys.sign(digest, "sha256"))

		comp = xdoc.get('Comprobante')
		xdoc.attrib['Sello'] = sello

		# print ET.tostring(xdoc)
		return ET.tostring(xdoc),numero_certificado,sello,cadena_original

	def extract_timbre_info(self, xml_string):
		root = ET.fromstring(xml_string)
		if not 'cfdi' in root.nsmap:
			raise UserError("Namespace cfdi no definido")
		
		nspace = root.nsmap['cfdi']
		complemento = root.find( '{%s}%s' % (nspace,'Complemento') )
		if complemento is None:
			raise UserError("Namespace cfdi no definido")
		return complemento.find('{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital')

	def get_cadena(self, xml_element, filename):
		xsl_root = ET.parse(config["addons_path"] + '/account_invoice_facturae/sat/'+ filename)
		xsl = ET.XSLT(xsl_root)
		return xsl(xml_element) or ''

	@api.multi
	def action_cancel(self):
		for inv in self:
			if inv.facturada:
				emisor_rfc = inv.company_id.vat[2:]
				uuid = inv.factura_uuid
				inv.cancelar_timbre(emisor_rfc, uuid)
			return super(account_invoice, self).action_cancel()
			
	@api.model
	def genFacturae(self, cr, uid):
		invoice = self.browse(cr)

		if invoice.facturada:
			raise UserError("Invoice ya timbrado")

		tz_name = uid['tz'] or 'America/Monterrey'
		user_tz = pytz.timezone(tz_name)
		now = pytz.utc.localize(datetime.now()).astimezone(user_tz)
		qr_string = ""
		namespaces =  {
			'cfdi' : "http://www.sat.gob.mx/cfd/3",
			'xsi' : "http://www.w3.org/2001/XMLSchema-instance",
		}

		root = ET.Element('{%s}Comprobante' % namespaces['cfdi'], nsmap=namespaces)
		root.set("{%s}schemaLocation" % namespaces['xsi'], "http://www.sat.gob.mx/cfd/3 http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd")
		root.set("Version", "3.3")
		serie_folio = invoice.number.split("-")
		root.set("Serie", serie_folio[0])
		root.set("Folio", serie_folio[1])

		try:
			pay_method_id = invoice.pay_method_id.code
			pay_metodopago_id = invoice.pay_metodopago_id.code
		except TypeError:
			raise UserError("Error en forma de pago, método de pago o cuenta de pago")

		root.set("FormaPago", pay_method_id)
		root.set("MetodoPago", pay_metodopago_id)

		moneda = "MXN"

		if invoice.currency_id.name == "USD":
			moneda = "USD"
			root.set("TipoCambio", "%.2f" % (1 / invoice.currency_id.rate))

		root.set("Moneda", moneda)

		root.set("TipoDeComprobante", "I")

		try:
			root.set("LugarExpedicion", invoice.company_id.zip)
		except TypeError:
			raise UserError("Error en dirección de la compañía que esta facturando")

		# root.set("NumCtaPago", cta_pago)
		try:
			root.set("CondicionesDePago", invoice.payment_term_id.name)
			root.set("SubTotal", unicode(invoice.amount_untaxed))
			root.set("Total", unicode(invoice.amount_total))
		except TypeError:
			raise UserError("Condiciones de pago no asignado en la factura")

		emisor = ET.SubElement(root, '{%s}Emisor' % namespaces['cfdi'])
		
		try:
			emisor.set("Rfc", invoice.company_id.vat[2:])
			emisor.set("Nombre", invoice.company_id.name)
			qr_string += '?re=%s' % invoice.company_id.vat[2:15]
		except TypeError:
			raise UserError("RFC no asignado en la compañía que esta facturando")

		# emisor_df = ET.SubElement(emisor, '{%s}DomicilioFiscal' % namespaces['cfdi'])
		# try:
		# 	emisor_df.set("calle", invoice.company_id.street) 
		# 	emisor_df.set("noExterior", invoice.company_id.l10n_mx_street3) 
		# 	emisor_df.set("noInterior", invoice.company_id.l10n_mx_street4) 
		# 	emisor_df.set("colonia", invoice.company_id.street2) 
		# 	emisor_df.set("municipio", invoice.company_id.city) 
		# 	emisor_df.set("estado", invoice.company_id.state_id.name) 
		# 	emisor_df.set("pais", invoice.company_id.country_id.name) 
		# 	emisor_df.set("codigoPostal", invoice.company_id.zip)
		# except TypeError:
		# 	raise UserError("Error en el domicilio de la compañía que esta facturando")

		# emisor_rf = ET.SubElement(emisor, '{%s}RegimenFiscal' % namespaces['cfdi'])
		try:
			emisor.set("RegimenFiscal", invoice.company_id.partner_id.regimen_fiscal_id.code)
			# emisor_rf.set("Regimen", invoice.company_id.partner_id.regimen_fiscal_id.name)
		except:
			raise UserError("Error en el régimen de la compañía que esta facturando")

		receptor = ET.SubElement(root, '{%s}Receptor' % namespaces['cfdi'])
		try:
			receptor.set("Rfc", invoice.partner_id.vat[2:])
			receptor.set("Nombre", invoice.partner_id.name)
			qr_string += '&rr=%s' % invoice.partner_id.vat[2:15]
		except TypeError:
			raise UserError("RFC no asignado en la compañía a la que esta facturando")

		receptor.set("UsoCFDI", invoice.invoice_usocfdi_id.code)
		# receptor_d = ET.SubElement(receptor, '{%s}Domicilio' % namespaces['cfdi'])
		# try:
		# 	receptor_d.set("calle", invoice.partner_id.street) 
		# 	receptor_d.set("noExterior", invoice.partner_id.l10n_mx_street3)
		# 	if invoice.partner_id.l10n_mx_street4:
		# 		receptor_d.set("noInterior", invoice.partner_id.l10n_mx_street4)
		# 	receptor_d.set("colonia", invoice.partner_id.street2) 
		# 	receptor_d.set("municipio", invoice.partner_id.city) 
		# 	receptor_d.set("estado", invoice.partner_id.state_id.name) 
		# 	receptor_d.set("pais", invoice.partner_id.country_id.name) 
		# 	receptor_d.set("codigoPostal", invoice.partner_id.zip)
		# except TypeError:
		# 	raise UserError("Error en el domicilio de la compañía a la que esta facturando")
		
		conceptos = ET.SubElement(root, '{%s}Conceptos' % namespaces['cfdi'])

		for invoice_line in invoice.invoice_line_ids:
			concepto = ET.SubElement(conceptos, '{%s}Concepto' % namespaces['cfdi'])
			concepto.set("ClaveProdServ", invoice_line.product_id.claveprodserv_id.code)
			concepto.set("NoIdentificacion", str(invoice_line.product_id.id))
			concepto.set("Cantidad", "{:.2f}".format(invoice_line.quantity))
			concepto.set("ClaveUnidad", invoice_line.product_id.claveunidad_id.code)
			concepto.set("Unidad", invoice_line.product_id.claveunidad_id.name)
			concepto.set("Descripcion", invoice_line.name)
			concepto.set("ValorUnitario", "{:.2f}".format(invoice_line.price_unit))
			concepto.set("Importe", "{:.2f}".format(invoice_line.price_subtotal))

			impuestos = ET.SubElement(concepto, '{%s}Impuestos' % namespaces['cfdi'])
			traslados = ET.SubElement(impuestos, '{%s}Traslados' % namespaces['cfdi'])
			traslado = ET.SubElement(traslados, '{%s}Traslado' % namespaces['cfdi'])
			traslado.set("Base", "{:.2f}".format(invoice_line.price_subtotal))
			traslado.set("Impuesto", "002")
			traslado.set("TipoFactor", "Tasa")
			traslado.set("TasaOCuota", "0.160000")
			traslado.set("Importe", "{:.2f}".format(invoice_line.price_subtotal*.16))

		impuestos = ET.SubElement(root, '{%s}Impuestos' % namespaces['cfdi'])
		impuestos.set("TotalImpuestosTrasladados", "{:.2f}".format(invoice.amount_tax))

		traslados = ET.SubElement(impuestos, '{%s}Traslados' % namespaces['cfdi'])
		for tax_line in invoice.tax_line_ids:
			traslado = ET.SubElement(traslados, '{%s}Traslado' % namespaces['cfdi'])
			traslado.set("Impuesto", "002")
			traslado.set("TipoFactor", "Tasa")
			traslado.set("TasaOCuota", "0.160000")
			traslado.set("Importe", "{:.2f}".format(tax_line.amount))

		xml_sin_sellar = ET.tostring(root)

		archivo_cer_path = config.filestore(self.env.cr.dbname) + "/" + invoice.company_id.achivo_cer.store_fname
		archivo_pem_path = config.filestore(self.env.cr.dbname) + "/" + invoice.company_id.achivo_pem.store_fname
		# Se agregan mas variables, para recibir valores que regresa la funcion
		xml_sellado,no_certificado,sello_sella,cadena = self.sella_xml(xml_sin_sellar, invoice.company_id.numero_certificado, archivo_cer_path, archivo_pem_path, now)
		xml_sellado = '<?xml version="1.0" encoding="utf-8"?>' + xml_sellado

		xml_base64 = base64.b64encode(xml_sellado)

		#xml,UUID,fecha,sello,certificado, version = self.timbrar(xml_base64)
		xml = self.timbrar(xml_base64, serie_folio[0] + serie_folio[1])

		timbre_fiscal = self.extract_timbre_info(xml)

		if timbre_fiscal is None:
			raise UserError("Timbre fiscal no encontrado")

		UUID = timbre_fiscal.attrib['UUID']
		fecha = timbre_fiscal.attrib['FechaTimbrado']
		sello = timbre_fiscal.attrib['SelloSAT']
		rfcpac = timbre_fiscal.attrib['RfcProvCertif']
		certificado = timbre_fiscal.attrib['NoCertificadoSAT']
		version = timbre_fiscal.attrib['Version']

		cadena_timbrada = self.get_cadena(timbre_fiscal, 'cadenaoriginal_TFD_1_1.xslt')
		
		name = invoice.company_id.vat[2:5] + "%010d" % (int(serie_folio[1]),)
		
		total_float = float(unicode(invoice.amount_total))
		qr_string += '&tt=%017.6f' % total_float
		qr_string += '&id=%s' % UUID

		factura_xml = self.env['ir.attachment'].create({
			'res_model'    : 'account.invoice',
			'res_id'       : invoice.id,
			'mimetype'     :'application/xml',
			'datas'        : base64.encodestring(xml),
			'name'         : name + ".xml",
			'datas_fname'  : name + ".xml",
			'display_name' : name + ".xml"
		})

		values = {
			'facturada': True,
			'factura_xml': factura_xml.id,
			'factura_moneda' : moneda,
			'factura_formapago' : pay_method_id,
			'factura_uuid' : UUID,
			'factura_fecemi' : fecha,
			'factura_sellosat' : sello,
			'factura_rfcpac' : rfcpac,
			'factura_certificado' : certificado,
			'factura_nocertificado': no_certificado,
			'factura_sello' : sello_sella,
			'factura_cadena' : cadena,
			'factura_qr_cadena' : urllib.quote(qr_string),
			'factura_version' : version,
			'factura_cadena_timbrada' : cadena_timbrada,
		}

		invoice.write(values)

		return self.env['report'].get_action(self, 'account.report_invoice_facturae')

	@api.multi
	def invoice_print(self):
		self.ensure_one()
		self.sent = True
		return self.env['report'].get_action(self, 'account.report_invoice_facturae')