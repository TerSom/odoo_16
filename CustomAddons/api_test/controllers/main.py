import requests
import json
from odoo import http
from odoo.http import request


class GoldPriceController(http.Controller):

    @http.route(['/api/gold_price_post/'], type='http', auth='public', methods=['POST'], csrf=False)
    def sync_gold_price(self, **params):
        url = "https://pluang.com/api/asset/gold/pricing?daysLimit=1000"
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

        # Save Current Price
        current = data.get("current")
        if current:
            request.env["current.price"].sudo().create({
                "mid_price": current.get("midPrice"),
                "sell": current.get("sell"),
                "buy": current.get("buy"),
                "installment": current.get("installment"),
                "updated_at": current.get("updated_at"),
            })

        # Save History Price
        history_list = data.get("history", [])
        for history in history_list:
            request.env["history.price"].sudo().create({
                "sell": history.get("sell"),
                "buy": history.get("buy"),
                "installment": history.get("installment"),
                "updated_at": history.get("updated_at"),
            })

        # Response JSON
        return http.Response(
            json.dumps({
                "status": 200,
                "message": "Gold price synced successfully",
                "current": current,
                "history_count": len(history_list),
            }),
            content_type='application/json',
            status=200
        )
