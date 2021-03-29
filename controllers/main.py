import logging

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request
from odoo.osv import expression
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class FilterWebsiteSale(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values, search_in_description=True):
        domain = super(FilterWebsiteSale, self)._get_search_domain(search, category, attrib_values)
        domains = []
        # if search:
        #     for srch in search.split(" "):
        #         subdomains = [
        #             [('name', 'ilike', srch)],
        #             [('product_variant_ids.default_code', 'ilike', srch)]
        #         ]
        # if search_in_description:
        # subdomains.append([('description', 'ilike', srch)])
        # subdomains.append([('description_sale', 'ilike', srch)])
        # subdomains.append([('website_description', 'ilike', srch)])
        # domain = domain + '|' + ['!', ('website_description', 'ilike', srch)]
        # domains.append(expression.OR(subdomains))

        # dom = domain + expression.OR(domains
        return domain + [('website_description', 'ilike', search)]
