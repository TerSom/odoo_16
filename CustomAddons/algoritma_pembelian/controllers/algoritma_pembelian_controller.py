import json
import requests
from odoo.tests import Form
import werkzeug.wrappers


from odoo import http, _,exceptions
from odoo.http import content_disposition,request
import io


class AlgoritmaPembelianRestApi(http.Controller):
    @http.route(['/api/algoritma_pembelian_get/'],type='http', auth='public', methods=['GET'],csrf=False)
    def algoritma_pembelian_restapi_get(self, **params):
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
            dict_algoritma_pembelian = {'id': h.id, 'name': h.nama, 'algoritma_brand_ids': detail_brand, 'algoritma_pembelian_line_ids': detail_product}
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
                
    @http.route(['/api/algoritma_pembelian_post/'],type='json', auth='public', methods=['POST'],csrf=False)
    def algoritma_pembelian_restapi_post(self, **params):
        order = params.get("order")
        tanggal = order[0]['tanggal']
        nama = order[0]['nama']
        algoritma_brand_ids = order[0]['algoritma_brand_ids']
        name_brand = []
        for a in algoritma_brand_ids:
            name_brand.append(a['name'])
        brand_obj = request.env["algoritma.brand"].sudo().search([('name', 'in', name_brand)])
        algoritma_pembelian_line_ids = order[0]['algoritma_pembelian_line_ids']
        vals_line = []
        for i in algoritma_pembelian_line_ids:
            product_obj = request.env["product.product"].sudo().search([('default_code', '=' , i['product_id'])])
            uom_obj = request.env['uom.uom'].sudo().search([('name', '=', i['uom_id'])])
            vals_line.append((0,0,{
                'product_id': product_obj.id,
                'name': product_obj.name,
                'quantity': i['quantity'],
                'uom_id': uom_obj.id,
                'sales_price': i['sales_price'],
                'standar_price': i['standar_price']
            }))
        vals_header = {
            'tanggal' : tanggal, 'nama' : nama ,'algoritma_brand_ids' : [(6,0,brand_obj.ids)], 'algoritma_pembelian_line_ids' : vals_line
        }
        new_algoritma_pembelian = request.env['algoritma.pembelian'].sudo().create(vals_header)
        data = {
            'status': 200,
            'message': 'succes',
            'nama' : nama,
            'tanggal': tanggal,
            'brands': algoritma_brand_ids,
            'algoritma_pembelian_line_ids' : algoritma_pembelian_line_ids
        }
        return data
        