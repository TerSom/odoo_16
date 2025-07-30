from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    
    name = fields.Char(required=True)
    
    property_ids = fields.One2many("estate.property",'property_type_id',readonly=True)
    
    _sql_constraints = [
        ('check_name','UNIQUE(name)',
        'Nama tidak boleh sama.')
    ]