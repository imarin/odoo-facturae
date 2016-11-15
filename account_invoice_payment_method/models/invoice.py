# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to Odoo
#
#    Copyright (c) 2011 X8BIT - http://www.x8bit.com
#    All Rights Reserved.
#    info@x8bit.com
############################################################################
#    Coded by: Juan Carlos del Valle (juan@x8bit.com)
############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class account_invoice_x(models.Model):
	_inherit = "account.invoice"

	@api.onchange('partner_id')
	def _onchange_partner(self):
		if self.partner_id:
			self.acc_payment = self.partner_id.acc_payment and self.partner_id.acc_payment.id or False
			self.pay_method_id = self.partner_id.pay_method_id and self.partner_id.pay_method_id.id or False

	pay_method_id = fields.Many2one('l10n_mx.pay.method', string='Payment Method', readonly=True, states={'draft': [('readonly', False)]}, required=True, help="Método de pago para esta factura")
	acc_payment = fields.Many2one('res.partner.bank', string='Account Number', readonly=True, states={'draft': [('readonly', False)]}, required=True, help="Cuenta con la que se pagará esta factura")