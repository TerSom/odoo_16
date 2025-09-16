import requests
import json
from odoo import http
from odoo.http import request

class GoldPriceController(http.Controller):

    @http.route(['/api/gold_price_get/'], type='http', auth='public', methods=['GET'], csrf=False)
    def sync_gold_price_get(self, **params):
        url = "https://pluang.com/api/asset/gold/pricing?daysLimit=100"
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
            request.env["current.price"].sudo().create({
                "mid_price": current.get("midPrice"),
                "sell": current.get("sell"),
                "buy": current.get("buy"),
                "installment": current.get("installment"),
                "updated_at": current.get("updated_at"),
            })
            
        history_list = data.get("history", [])
        for history in history_list:
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
