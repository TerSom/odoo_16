import requests
import logging
from odoo import models

_logger = logging.getLogger(__name__)

class GoldPriceCron(models.Model):
    _name = "gold.price.cron"
    _description = "Gold Price Cron"
    
    def sync_gold_price(self):
        URL = "https://pluang.com/api/asset/gold/pricing?daysLimit=20"
        response = requests.get(URL)

        if response.status_code != 200:
            _logger.error("Gagal fetch API: %s", response.status_code)
            return False

        data = response.json().get("data", {})
        
        current = data.get("current")
        if current:
            self.env["current.price"].sudo().create({
                "mid_price": current.get("midPrice"),
                "sell": current.get("sell"),
                "buy": current.get("buy"),
                "installment": current.get("installment"),
                "updated_at": current.get("updated_at"),
            })
        
        history_list = data.get("history", [])
        for history in history_list:
            self.env["history.price"].sudo().create({
                "sell": history.get("sell"),
                "buy": history.get("buy"),
                "installment": history.get("installment"),
                "updated_at": history.get("updated_at"),
            })

        _logger.info("Gold price berhasil di-fetch (history: %s)", len(history_list))
        return True
