from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSale
from datetime import timedelta
import datetime
from odoo.http import request
from odoo import http, _
from odoo.tools.safe_eval import safe_eval


class SliderBuilder(WebsiteSale):

    # Render the custom domain products
    def custom_domain_products(self,filter_id,limit=20,sort_by='name asc'):
        filter = False
        if filter_id:
            filter = request.env['slider.filter'].sudo().browse(filter_id[0]).filtered(lambda r:r.exists())
        if filter and filter.website_published:
            if filter.filter_domain.find(",uid]")>0:
                domain = safe_eval(filter.filter_domain.replace(",uid]",","+str(request.uid)+"]"))
            else:
                domain = safe_eval(filter.filter_domain)
            domain += ['|', ('website_id', '=', None), ('website_id', '=', request.website.id),
                       ('website_published', '=', True),('type','in',['product','consu']),('sale_ok','=',True)]
            return request.env['product.template'].sudo().search(domain,limit=limit,order=sort_by)
        return False