from odoo import models, fields, api
from odoo.exceptions import ValidationError       
                
class inheritResUsers(models.Model):
    _inherit = 'res.users'
        
    property_ids = fields.One2many('estate.property', 'salesperson_id')