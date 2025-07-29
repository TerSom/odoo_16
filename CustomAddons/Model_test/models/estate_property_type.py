from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    
    _sql_constraints = [
        ('unique_nama', 'unique(nama)', 'Nama harus unik!')
    ]
    
    name = fields.Char(required=True)