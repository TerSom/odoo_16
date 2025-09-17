import requests
from odoo import models, api

class GempaCron(models.Model):
    _name = "gempa.cron"
    _description = "Cron untuk fetch API gempa BMKG"

    def _fetch_data(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json().get("Infogempa", {}).get("gempa", [])
        except Exception as e:
            _logger = self.env["ir.logging"]
            _logger.create({
                "name": "BMKG Cron",
                "type": "server",
                "level": "ERROR",
                "dbname": self._cr.dbname,
                "message": str(e),
                "path": "gempa.cron",
                "func": "_fetch_data",
                "line": "0",
            })
        return []

    @api.model
    def cron_fetch_gempa(self):
        """Dipanggil otomatis oleh ir.cron tiap 1 jam"""
        
        # API Gempa Terbaru
        data_terbaru = self._fetch_data("https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json")
        if data_terbaru:
            g = data_terbaru[0] if isinstance(data_terbaru, list) else data_terbaru
            self.env["gempa.bumi.terbaru"].sudo().create({
                "tanggal": g.get("Tanggal"),
                "jam": g.get("Jam"),
                "dateTime": g.get("DateTime"),
                "coordinates": g.get("Coordinates"),
                "lintang": g.get("Lintang"),
                "bujur": g.get("Bujur"),
                "magnitude": g.get("Magnitude"),
                "kedalaman": g.get("Kedalaman"),
                "wilayah": g.get("Wilayah"),
                "potensi": g.get("Potensi"),
                "dirasakan": g.get("Dirasakan"),
            })

        # API Gempa M 5.0
        data_m5 = self._fetch_data("https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json")
        for g in data_m5:
            self.env["gempa.bumi.m.5.0"].sudo().create({
                "tanggal": g.get("Tanggal"),
                "jam": g.get("Jam"),
                "dateTime": g.get("DateTime"),
                "coordinates": g.get("Coordinates"),
                "lintang": g.get("Lintang"),
                "bujur": g.get("Bujur"),
                "magnitude": g.get("Magnitude"),
                "kedalaman": g.get("Kedalaman"),
                "wilayah": g.get("Wilayah"),
                "potensi": g.get("Potensi"),
            })

        # API Gempa Bumi
        for g in data_m5:
            self.env["gempa.bumi"].sudo().create({
                "tanggal": g.get("Tanggal"),
                "jam": g.get("Jam"),
                "dateTime": g.get("DateTime"),
                "coordinates": g.get("Coordinates"),
                "lintang": g.get("Lintang"),
                "bujur": g.get("Bujur"),
                "magnitude": g.get("Magnitude"),
                "kedalaman": g.get("Kedalaman"),
                "wilayah": g.get("Wilayah"),
                "dirasakan": g.get("Dirasakan"),
            })
