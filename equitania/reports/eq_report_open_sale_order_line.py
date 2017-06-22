# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
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

import time
from openerp.osv import osv
from openerp import api
from openerp.report import report_sxw

class eq_report_open_sale_order_line(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
        super(eq_report_open_sale_order_line, self).__init__(cr, uid, name, context=context)
        
        self.localcontext.update({
            'get_qty':self.get_qty,
            'get_price': self.get_price,
            'get_standard_price': self.get_standard_price,
            'get_records': self._get_records,
        })
        
    
    def get_qty(self, object, language):
        return self.pool.get("eq_report_helper").get_qty(self.cr, self.uid, object, language, 'Sale Quantity Report')
           
    
    def get_price(self, object, language, currency_id):                
        return self.pool.get("eq_report_helper").get_price(self.cr, self.uid, object, language, 'Sale Price Report', currency_id)
    
    
    def get_standard_price(self, object, language, currency_id):
        return self.pool.get("eq_report_helper").get_standard_price(self.cr, self.uid, object, language, currency_id)


    def _get_records(self):
        """
            Get all records created by wizard and show them as lines in table
            @return: An array with all created records from eq_product_sales_data table
        """

        result = []
        table = self.pool.get('eq_buffer_order_line_list')
        ids = table.search(self.cr, self.uid, [])
        for id in ids:
            result.append(table.browse(self.cr, self.uid, id))

        return result
          
    
class report_lunchorder(osv.AbstractModel):
    
    _name = 'report.equitania.report_open_sale_order_line'
    _inherit = 'report.abstract_report'
    _template = 'equitania.report_open_sale_order_line'
    _wrapped_report_class = eq_report_open_sale_order_line