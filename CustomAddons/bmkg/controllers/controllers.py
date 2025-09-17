import requests
import json
from odoo import http
from odoo.http import request

class InfoGempaController(http.Controller):
    @http.route(["/api/gempa_bumi_terbaru/"], type='http', auth='public', methods=['GET'], csrf=False)
    def get_gempa_bumi_terbaru(self, **params):
        URL = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36"
        }
        response = requests.get(URL, headers=headers)

        if response.status_code != 200:
            return http.Response(
                json.dumps({
                    "status": response.status_code,
                    "message": "gagal untuk fetch API"
                }),
                content_type='application/json',
                status=response.status_code
            )

        data = response.json().get('Infogempa', {})
        gempaTerbaru = data.get("gempa")

        if gempaTerbaru:
            request.env["gempa.bumi.terbaru"].sudo().create({
                "tanggal": gempaTerbaru.get("Tanggal"),
                "jam": gempaTerbaru.get("Jam"),
                "dateTime" : gempaTerbaru.get("DateTime"),
                "coordinates": gempaTerbaru.get("Coordinates"),
                "lintang": gempaTerbaru.get("Lintang"),
                "bujur": gempaTerbaru.get("Bujur"),
                "magnitude": gempaTerbaru.get("Magnitude"),
                "kedalaman": gempaTerbaru.get("Kedalaman"),
                "wilayah": gempaTerbaru.get("Wilayah"),
                "potensi": gempaTerbaru.get("Potensi"),
                "dirasakan": gempaTerbaru.get("Dirasakan"),
            })

        return http.Response(
            json.dumps({
                "status": 200,
                "message": "Gempa terbaru berhasil disimpan",
                "history_saved": 1,
            }),
            content_type='application/json',
            status=200
        )

    @http.route(["/api/gempa_M_5_0/"], type='http', auth='public', methods=['GET'], csrf=False)
    def get_gempa_bumi_M_5_0(self, **params):
        URL = "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36"
        }
        response = requests.get(URL, headers=headers)

        if response.status_code != 200:
            return http.Response(
                json.dumps({
                    "status": response.status_code,
                    "message": "gagal untuk fetch API"
                }),
                content_type='application/json',
                status=response.status_code
            )

        data = response.json().get('Infogempa', {})
        
        gempa_m_5_0_list = data.get("gempa", [])
        for gempa_m_5_0 in gempa_m_5_0_list:
            request.env["gempa.bumi.m.5.0"].sudo().create({
                "tanggal": gempa_m_5_0.get("Tanggal"),
                "jam": gempa_m_5_0.get("Jam"),
                "coordinates": gempa_m_5_0.get("Coordinates"),
                "lintang": gempa_m_5_0.get("Lintang"),
                "bujur": gempa_m_5_0.get("Bujur"),
                "magnitude": gempa_m_5_0.get("Magnitude"),
                "kedalaman": gempa_m_5_0.get("Kedalaman"),
                "wilayah": gempa_m_5_0.get("Wilayah"),
                "potensi": gempa_m_5_0.get("Potensi"),
            })

        return http.Response(
            json.dumps({
                "status": 200,
                "message": "Gempa terbaru berhasil disimpan",
                "history_saved": len(gempa_m_5_0),
            }),
            content_type='application/json',
            status=200
        )
        
    @http.route(["/api/gempa_bumi/"], type='http', auth="public" ,methods=['GET'], csrf=False)
    def get_gempa_bumi(self, **params):
        URL = "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36"
        }
        response = requests.get(URL, headers=headers)
        
        if response.status_code != 200:
            return http.Response(
                json.dumps({
                    "status" : response.status_code,
                    "message" :"api gempa bumi gk masuk"
                }),
                content_type='application/json',
                status=response.status_code
            )
        
        data = response.json().get('Infogempa', {})
        
        gempa_list = data.get("gempa" , [])
        for gempa in gempa_list:
            request.env['gempa.bumi'].sudo().create({
                "tanggal" : gempa.get("Tanggal"),
                "jam" : gempa.get("Jam"),
                "dateTime" : gempa.get("DateTime"),
                "coordinates" : gempa.get("Coordinates"),
                "lintang" : gempa.get("Lintang"),
                "bujur" : gempa.get("Bujur"),
                "magnitude" : gempa.get("Magnitude"),
                "kedalaman" : gempa.get("Kedalaman"),
                "wilayah" : gempa.get("Wilayah"),
                "dirasakan" : gempa.get("Dirasakan")
            })
            
        return http.Response(
            json.dumps({
                "status" : 200,
                "message" : "apinya berhasil di fetch",
                "history_saved" : len(gempa)
            }),
            content_type = 'application/json',
            status = 200
            
        )