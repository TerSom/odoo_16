from odoo import fields,models

class algoritma_pembelian_wizard_report(models.TransientModel):
    _name = "algoritma.pembelian.wizard.report"
    
    name = fields.Char(string="Nama")
    periode_awal = fields.Date(string="Periode Awal")
    periode_akhir = fields.Date(string="Periode Akhir")