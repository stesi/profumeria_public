# -*- coding: utf-8 -*-
{
    'name': "STeSI Profumeria Public",

    'summary': """
       Improvements for Profumeria""",

    'category': 'General',

    'description': """
        Long description of module's purpose
    """,
    'license': 'OPL-1',

    'author': "STeSI",
    'website': "http://www.stesi.srl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['payment_transfer', 'point_of_sale', 'base_automation', 'sale', 'purchase', 'point_of_sale',
                'pos_margin', 'l10n_it_delivery_note', 'emipro_theme_base', 'theme_clarico', 'stesi_ldv',
                'stesi_countersign_woo_odoo_cft'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/base_automation.xml',
        'views/view_pos_order.xml',
        'views/product_template.xml',
        'views/pos_order_view.xml',
        'views/purchase_order_view.xml',
        'views/sale_order_view.xml',
        'views/note_pos_order_view.xml',
        'views/stock_delivery_note.xml',
        'views/templates.xml',
        'views/product_label.xml',
        'views/res_partner.xml',
        'views/product_brand_ept.xml',
        'views/account_payment_term.xml',
        'views/payment_acquirer.xml',
        'views/res_users.xml',
        'views/stock_delivery_note_type.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
