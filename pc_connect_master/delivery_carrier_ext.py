# b-*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2016 brain-tec AG (http://www.braintec-group.com)
#    All Right Reserved
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

from openerp.osv import osv, fields, orm
from openerp.tools.translate import _


class delivery_carrier_ext(osv.Model):
    _inherit = 'delivery.carrier'

    _columns = {
        'show_customer_phone_on_picking': fields.boolean('Show Customer Phone Number on the Picking Report',
                                                         help='If checked, the phone of the customer will be shown on the report for the picking.'),
        'show_name_on_picking': fields.boolean('Show Delivery Method on the Picking Report',
                                               help='If checked, the name of the delivery method will be shown on the report for the picking.'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
