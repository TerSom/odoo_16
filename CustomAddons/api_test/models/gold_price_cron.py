import requests
import logging
from odoo import models

_logger = logging.getLogger(__name__)

class GoldPriceCron(models.Model):
    _name = "gold.price.cron"
    _description = "Gold Price Cron"

    def sync_gold_price(self):
        url = "https://pluang.com/api/asset/gold/pricing?daysLimit=200"
        response = requests.get(url)

        if response.status_code != 200:
            _logger.error("Failed to fetch API: %s", response.status_code)
            return

        data = response.json().get("data", {})

        current = data.get("current")
        if current:
            date_only = current.get("updated_at").split("T")[0]
            exiting = self.env["current.price"].sudo().search([
                ('updated_at', '=', date_only),
            ], limit=1)
            if exiting:
                exiting.write({
                    "mid_price": current.get("midPrice"),
                    "sell": current.get("sell"),
                    "buy": current.get("buy"),
                    "installment": current.get("installment"),
                    "updated_at": date_only,
                })
            else:
                self.env['current.price'].sudo().create({
                    "mid_price": current.get("midPrice"),
                    "sell": current.get("sell"),
                    "buy": current.get("buy"),
                    "installment": current.get("installment"),
                    "updated_at": date_only,
                })

        history_list = data.get("history", [])
        for history in history_list:
            date_only = history.get("updated_at").split("T")[0]
            exiting = self.env['history.price'].sudo().search([
                ('updated_at', '=', date_only)
            ], limit=1)
            if exiting:
                exiting.write({
                    "sell": history.get("sell"),
                    "buy": history.get("buy"),
                    "installment": history.get("installment"),
                })
            else:
                self.env["history.price"].sudo().create({
                    "sell": history.get("sell"),
                    "buy": history.get("buy"),
                    "installment": history.get("installment"),
                    "updated_at": date_only,
                })
