import json
import requests
from odoo.tests import Form
import werkzeug.wrappers


from odoo import http, _,exceptions
from odoo.http import content_disposition,request
import io


class AlgoritmaPembelianRestApi(http.Controller):
    @http.route(['/api/algoritma_pembelian_get/'],type='http', auth='public', methods=['GET'],csrf=False)
    def algoritma_pembelian_resapi_sef(self, **params):
        algoritma_pembelian = request.env['algoritma.pembelian'].sudo().search([])
        dict_algoritma_pembelian = {}
        data_algoritma_pembelian = []
        for h in algoritma_pembelian:
            dict_detail_brand = {}
            detail_brand = []
            dict_detail_product = {}
            detail_product = []
            for b in h.algoritma_brand_ids:
                dict_detail_brand = {'id': b.id, 'name': b.name }
                detail_brand.append(dict_detail_brand)
            for p in h.algoritma_pembelian_line_ids:
                dict_detail_product = {'product_id': p.product_id.display_name, 'description':p.name, 'quantity': p.quantity, 'uom_id': p.uom_id.name, 'price': p.sales_price, "subtotal": p.total_price }
                detail_product.append(dict_detail_product)
            dict_algoritma_pembelian = {'id': h.id, 'name': h.nama, 'brand_ids': detail_brand, 'algoritma_pembelian_line_ids': detail_product}
            data_algoritma_pembelian.append(dict_algoritma_pembelian)
        data = {
            'status': 200,
            'message': 'success',
            'response': data_algoritma_pembelian
        }
        try:
            return werkzeug.wrappers.Response(
                status=200,
                content_type='application/json; charset=utf-8',
                response=json.dumps(data)
            )
        except:
            return werkzeug.wrappers.Response(
                status=400,
                content_type='application/json; charset=utf-8',
                headers=[('Access-Control-Allow-Origin', '*')],
                response=json.dumps({
                    'error': 'Error',
                    'error_descrip': 'Rrror Description'
                })
            )
            
