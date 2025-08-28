from odoo import fields,models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    status = fields.Selection(string="Status",default="draft",
        selection=[
        ('draft','Draft'),                               
        ('to_approve','To Approve'),
        ('approved','Approved'),
        ('done','Done'),
        ('canceled','Canceled')
        ])
    
    def to_approve(self):
        for record in self:
            if record.status == 'draft':
                record.status = 'to_approve'
                
    def approved(self):
        for record in self:
            if record.status == 'to_approve':
                record.status = 'approved'
                
    def done(self):
        for record in self:
            if record.status == 'approved':
                record.status = 'done'
                
    def cancel(self):
        for record in self:
            if record.status == 'draft':
                record.status = 'canceled'
                
    