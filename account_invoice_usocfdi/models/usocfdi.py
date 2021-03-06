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

from openerp import models, fields

class UsoCFDI(models.Model):
    _name = 'l10n_mx.invoice.usocfdi'

    name = fields.Char(string="Uso CFDI", required=True)
    code = fields.Char(string="Clave", required=True)
    aplica_fisica = fields.Boolean(string="Aplica para persona física")
    aplica_moral = fields.Boolean(string="Aplica para persona moral")