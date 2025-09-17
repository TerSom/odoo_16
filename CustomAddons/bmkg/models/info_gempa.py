from odoo import fields, models, api

class GempaBumiTerbaru(models.Model):
    _name = "gempa.bumi.terbaru"
    _description = "Gempa Bumi Terbaru"
    
    tanggal = fields.Char(string="Tanggal")
    jam = fields.Char(string="Jam")
    dateTime = fields.Char(string="DateTime")
    coordinates = fields.Char(string="Coordinates")
    lintang = fields.Char(string="Lintang")
    bujur = fields.Char(string="Bujur")
    magnitude = fields.Float(string="Magnitude")
    kedalaman = fields.Char(string="Kedalaman")
    wilayah = fields.Char(string="Wilayah")
    potensi = fields.Char(string="Potensi")
    dirasakan = fields.Char(string="Dirasakan")
    
class GempaBumi_M_5_0(models.Model):
    _name = "gempa.bumi.m.5.0"
    _description = "Gempa Bumi M 5.0"
    
    tanggal = fields.Char(string="Tanggal")
    jam = fields.Char(string="Jam")
    dateTime = fields.Char(string="DateTime")
    coordinates = fields.Char(string="Coordinates")
    lintang = fields.Char(string="Lintang")
    bujur = fields.Char(string="Bujur")
    magnitude = fields.Float(string="Magnitude")
    kedalaman = fields.Char(string="Kedalaman")
    wilayah = fields.Char(string="Wilayah")
    potensi = fields.Char(string="Potensi")
    
class GempaBumi(models.Model):
    _name = "gempa.bumi"
    _description = "Gempa Bumi"

    tanggal = fields.Char(string="Tanggal")
    jam = fields.Char(string="Jam")
    dateTime = fields.Char(string="DateTime")
    coordinates = fields.Char(string="Coordinates")
    lintang = fields.Char(string="Lintang")
    bujur = fields.Char(string="Bujur")
    magnitude = fields.Float(string="Magnitude")
    kedalaman = fields.Char(string="Kedalaman")
    wilayah = fields.Char(string="Wilayah")
    dirasakan = fields.Char(string="Dirasakan")
    
    