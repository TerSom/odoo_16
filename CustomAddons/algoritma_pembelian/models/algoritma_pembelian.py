from odoo import fields,models

class algoritma_pembelian(models.Model):
    _name = "algoritma.pembelian"
    _description = "algoritma pembelian"
    
    nama = fields.Char(string="Nama")
    tanggal = fields.Date(string="Tanggal")
    status = fields.Selection(string="Status",
         selection=[
            ('draft','Draft'),
            ('to_approve','To Approve'),
            ('approved','Approved'),
            ('done','Done')
            ],required=True,default="draft"
    )
    algoritma_pembelian_line_ids = fields.One2many('algoritma.pembelian.line','algoritma_pembelian_id' ,string="algoritma pembelian line ids")
    algoritma_brand_ids = fields.Many2many('algoritma.brand','algoritma_brand_rel' , 'algoritma_pembelian_id','brand_id',string="algorita pembelian ids")
    
    
class algoritma_pembelian_line(models.Model):
    _name = "algoritma.pembelian.line"
    
    algoritma_pembelian_id = fields.Many2one('algoritma.pembelian', string="algoritma pembelian id")
    product_id = fields.Many2one('product.product',string="product id")
    quantity = fields.Float(string="Quantity", default= 0.0)
    uom_id = fields.Many2one('uom.uom',string="Uom id")
    

class algoritma_brand(models.Model):
    _name = "algoritma.brand"
    
    name = fields.Char(string="Name")
    color = fields.Integer()
    