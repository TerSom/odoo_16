from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "name"
    
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property",'property_type_id',readonly=True)
    sequence = fields.Integer(default=1)
    
    _sql_constraints = [
        ('check_name','UNIQUE(name)',
        'Nama tidak boleh sama.')
    ]