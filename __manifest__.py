# -*- coding: utf-8 -*-
{
    'name': "STeSI Import Profumeria Public",

    'summary': """
       Import Order for Profumeria""",

    'category': 'MRP',

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
    'depends': ['point_of_sale', 'base_automation'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/view_pos_order.xml',
        'views/product_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
