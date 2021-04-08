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
    'depends': ['point_of_sale', 'base_automation', 'sale', 'purchase', 'point_of_sale','pos_margin', 'l10n_it_delivery_note', 'emipro_theme_base', 'theme_clarico'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/view_pos_order.xml',
        'views/product_template.xml',
        'views/product_product.xml',
        'views/pos_order_view.xml',
        'views/purchase_order_view.xml',
        'views/sale_order_view.xml',
        'views/note_pos_order_view.xml',
        'views/stock_delivery_note.xml',
        'views/res_partner_inherit_view_tree.xml',
        'views/templates.xml'
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
