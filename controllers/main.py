import logging

from werkzeug.exceptions import NotFound

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request
from odoo.osv import expression
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class FilterWebsiteSale(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values, search_in_description=True):
        domains = [request.website.sale_product_domain()]
        if search:
            for srch in search.split(" "):
                subdomains = [
                    [('name', 'ilike', srch)],
                    [('product_variant_ids.default_code', 'ilike', srch)]
                ]
                if search_in_description:
                    subdomains.append([('description', 'ilike', srch)])
                    subdomains.append([('description_sale', 'ilike', srch)])
                    subdomains.append([('website_description', 'ilike', srch)])
                domains.append(expression.OR(subdomains))

        if category:
            domains.append([('public_categ_ids', 'child_of', int(category))])

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domains.append([('attribute_line_ids.value_ids', 'in', ids)])
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domains.append([('attribute_line_ids.value_ids', 'in', ids)])

        domain = expression.AND(domains)

        cust_min_val = request.httprequest.values.get('min_price', False)
        cust_max_val = request.httprequest.values.get('max_price', False)

        if cust_max_val and cust_min_val:
            try:
                cust_max_val = float(cust_max_val)
                cust_min_val = float(cust_min_val)
            except ValueError:
                raise NotFound()
            products = request.env['product.template'].sudo().search(domain)
            new_prod_ids = []
            pricelist = request.website.pricelist_id
            # return the product ids as per option selected (sale price or discounted price)
            if products:
                if request.website.price_filter_on == 'website_price':
                    context = dict(request.context, quantity=1, pricelist=pricelist.id if pricelist else False)
                    products = products.with_context(context)
                    new_prod_ids = products.filtered(
                        lambda r: r.price >= float(cust_min_val) and r.price <= float(cust_max_val)).ids
                else:
                    new_prod_ids = products.filtered(
                        lambda r: r.currency_id._convert(r.lst_price, pricelist.currency_id,
                                                         request.website.company_id, date=fields.Date.today()) >= float(
                            cust_min_val) and
                                  r.currency_id._convert(r.lst_price, pricelist.currency_id,
                                                         request.website.company_id, date=fields.Date.today()) <= float(
                            cust_max_val)).ids
                domain += [('id', 'in', new_prod_ids)]
            else:
                domain = [('id', '=', False)]
        if attrib_values:
            ids = []
            # brand Filter
            for value in attrib_values:
                if value[0] == 0:
                    ids.append(value[1])
                    domain += [('product_brand_ept_id.id', 'in', ids)]
        return domain
