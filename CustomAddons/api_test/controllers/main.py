import requests
import json
from odoo import http
from odoo.http import request

class GoldPriceController(http.Controller):

    @http.route(['/api/gold_price_get/'], type='http', auth='public', methods=['GET'], csrf=False)
    def sync_gold_price_get(self, **params):
        url = "https://pluang.com/api/asset/gold/pricing?daysLimit=200"
        response = requests.get(url)

        if response.status_code != 200:
            return http.Response(
                json.dumps({
                    "status": response.status_code,
                    "message": "Failed to fetch API"
                }),
                content_type='application/json',
                status=response.status_code
            )

        data = response.json().get("data", {})
        
        current = data.get("current")
        if current:
            exiting = request.env["current.price"].sudo().search([
                ('updated_at','<=', current.get('updated_at')),
            ], limit=1 )
            if exiting:
                exiting.write({
                "mid_price": current.get("midPrice"),
                "sell" : current.get("sell"),
                "buy" : current.get("buy"),
                "installment" : current.get("installment"),
                "updated_at" : current.get("updated_at"),
            })
            else:
                request.env['current.price'].sudo().create({
                    "mid_price": current.get("midPrice"),
                    "sell" : current.get("sell"),
                    "buy" : current.get("buy"),
                    "installment" : current.get("installment"),
                    "updated_at" : current.get("updated_at"),
                })
                
            
        history_list = data.get("history", [])
        for history in history_list:
            exiting = request.env['history.price'].sudo().search([
                ('updated_at', '=', history.get('updated_at'))
            ],limit=1)
            if exiting:
                exiting.write({
                    "sell": history.get("sell"),
                    "buy": history.get("buy"),
                    "installment": history.get("installment"),
                })
            else:
                request.env["history.price"].sudo().create({
                "sell": history.get("sell"),
                "buy": history.get("buy"),
                "installment": history.get("installment"),
                "updated_at": history.get("updated_at"),
            })

        return http.Response(
            json.dumps({
                "status": 200,
                "message": "Gold price synced successfully via GET",
                "history_saved": len(history_list),
            }),
            content_type='application/json',
            status=200
        )

    @http.route(['/api/local_gold_price_api/'], type='http', auth='public', methods=['GET'], csrf=False)
    def local_gold_price_get(self, **params):
        current_price = request.env['current.price'].sudo().search([])
        history_price = request.env['history.price'].sudo().search([])
        
        current_list = []
        for current in current_price:
            current_list.append({
                "mid_price" : current.mid_price,
                "sell" : current.sell,
                "buy" : current.buy,
                "installment" : current.installment,
                "updated_at" : current.updated_at,   
            })
        
        history_list = []
        for history in history_price:
            history_list.append({
                "sell" : history.sell,
                "buy" : history.buy,
                "installment" : history.installment,
                "updated_at" : history.updated_at,   
            })
            
        if not current_list and not history_list:
            return http.Response(
                json.dumps({
                    "status": 404,
                    "message": "Data tidak ditemukan"
                }),
                content_type='application/json',
                status=404
            )
        
        return http.Response(
            json.dumps({
                "status": 200,
                "count_current" : len(current_list),
                "count_history" : len(history_list),
                "current" : current_list,
                "history" : history_list
            },default=str ),
            content_type='application/json',
            status=200
        )