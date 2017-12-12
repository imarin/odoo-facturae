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

class account_invoice_y(models.Model):
    _inherit = "account.invoice"

    @api.model
    def _default_usocfdi_(self):
        return self.env['l10n_mx.invoice.usocfdi'].search([('code','=','G03')], limit=1)

    invoice_usocfdi_id = fields.Many2one('l10n_mx.invoice.usocfdi', string='Uso CFDI', readonly=True, states={'draft': [('readonly', False)]}, required=True, help="Uso del CFDI", default=_default_usocfdi_)