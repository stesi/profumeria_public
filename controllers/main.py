import logging

from werkzeug.exceptions import NotFound

from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.exceptions import UserError
from odoo.http import request
from odoo.osv import expression
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute, WebsiteSaleForm
from odoo.addons.website_mass_mailing.controllers.main import MassMailController
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.tools import datetime

_logger = logging.getLogger(__name__)


class AuthSignupHomeProfumeria(AuthSignupHome):

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        res = super(AuthSignupHomeProfumeria, self).web_auth_signup(*args, **kw)
        qcontext = self.get_auth_signup_qcontext()
        values = { key: qcontext.get(key) for key in ('login', 'name')}
        if values:
            user = request.env['res.users'].sudo().search(
                [('login', '=', qcontext.get("login")), ('name', '=', qcontext.get("name"))])
            partner = request.env['res.partner'].sudo().search(
                [('email', '=', qcontext.get("login")), ('name', '=', qcontext.get("name"))])

            if qcontext.get("date_of_birth"):
                date = datetime.strptime(str(qcontext.get("date_of_birth")), '%Y-%m-%d')
                if user:
                    user.sudo().update({'birthday': date})
                if partner:
                    partner.sudo().update({'date': date})
        return res


class WebsiteSaleFormProfumeria(WebsiteSaleForm):

    @http.route('/website_form/shop.sale.order', type='http', auth="public", methods=['POST'], website=True)
    def website_form_saleorder(self, **kwargs):
        res = super(WebsiteSaleFormProfumeria, self).website_form_saleorder(**kwargs)
        order = request.website.sale_get_order()

        if order and kwargs.get("invoice_check") == 'on':
            # if len(str(kwargs.get("fiscal_code_iva"))) > 4 and len(str(kwargs.get("pec_address"))) > 4:
            #     body = '<h3> Partner request invoice, Tax/Vat: **'+ str(kwargs.get("fiscal_code_iva"))[2:-2] + '** Pec/SDI: **' + str(kwargs.get("pec_address"))[2:-2] + '**'+'</h3>'
            # else:
            #     body = '<h3>Partner request invoice</h3>'
            # order.with_context(mail_create_nosubscribe=True).message_post(body=body)
            order.update({
                'tax_vat_number': str(kwargs.get("fiscal_code_iva")),
                'pec_sdi_code': str(kwargs.get("pec_address"))
            })
        return res


class FilterWebsiteSale(WebsiteSale):

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap=WebsiteSale.sitemap_shop)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        domain = self._get_search_domain(search, category, attrib_values)

        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list,
                        order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        Product = request.env['product.template'].with_context(bin_size=True)

        label_list = request.httprequest.args.getlist('label')
        product_label = False
        product_label_line = []

        if len(label_list) == 1:
            for label in label_list:
                # product_label_line = request.env['product.label.line'].search([('label.name', 'ilike', label)])
                product_label = request.env['product.label'].search([('name', 'ilike', label)], limit=1)
            domain = domain + [('label_line_ids.label', '=', product_label.id)]

        search_product = Product.search(domain, order=self._get_search_order(post))
        website_domain = request.website.website_domain()
        categs_domain = [('parent_id', '=', False)] + website_domain
        if search:
            search_categories = Category.search(
                [('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        if category:
            url = "/shop/category/%s" % slug(category)

        product_count = len(search_product)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        offset = pager['offset']
        products = search_product[offset: offset + ppg]

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.search([('product_tmpl_ids', 'in', search_product.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref('website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
            'product_label': product_label,
        }
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)

    def _get_search_domain(self, search, category, attrib_values, search_in_description=True):
        domains = [request.website.sale_product_domain()]
        if search:
            for srch in search.split(" "):
                subdomains = [
                    [('name', 'ilike', srch)],
                    [('product_variant_ids.default_code', 'ilike', srch)],
                    [('brand', 'ilike', srch)]
                ]
                if search_in_description:
                    subdomains.append([('website_description', '=ilike', "% " + srch + " %")])
                    subdomains.append([('website_description', '=ilike', srch + " %")])
                    subdomains.append([('website_description', '=ilike', srch)])
                    subdomains.append([('website_description', '=ilike', "% " + srch)])
                    subdomains.append(
                        [('website_id', '=', request.website.id), ('label_line_ids.label', '=ilike', srch)])
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

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def address(self, **kw):
        res = super(FilterWebsiteSale, self).address(**kw)
        if kw.get("newsletter_registration") and kw.get("email"):
            MassMailController.subscribe(self, 1, str(kw.get("email")))
        elif not kw.get("newsletter_registration"):
            request.env['mailing.contact'].sudo().search([('email', '=', str(kw.get("email")))], limit=1).unlink()
        return res
