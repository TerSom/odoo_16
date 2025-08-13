from odoo import models,fields,api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "name"
    
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property",'property_type_id',readonly=True)
    sequence = fields.Integer(default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")
    
    _sql_constraints = [
        ('check_name','UNIQUE(name)',
        'Nama tidak boleh sama.')
    ]   
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    