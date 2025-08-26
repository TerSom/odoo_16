from odoo import fields,models, api

class algoritma_pembelian(models.Model):
    _name = "algoritma.pembelian"
    _description = "algoritma pembelian"
    _order = 'nama asc'
    
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
    name = fields.Char(string="Name")
    sales_price = fields.Float(string="Sales Price")
    standar_price = fields.Float(string="Cost")

    @api.onchange('product_id')
    def _get_name_product_id(self):
        if not self.product_id:
            return {}
        else:
            self.name = self.product_id.name
            self.sales_price = self.product_id.list_price
            self.standar_price = self.product_id.standard_price
            self.quantity = self.product_id.qty_available
            # self.uom_id = self.product_id.
            
class algoritma_brand(models.Model):
    _name = "algoritma.brand"
    
    name = fields.Char(string="Name")
    color = fields.Integer()
    