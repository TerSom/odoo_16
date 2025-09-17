# -*- coding: utf-8 -*-
{
    'name': "bmkg",

    'summary': """
        Info Gempa
        """,

    'description': """
        Info Gempa Api BMKG
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/gempa_bumi_terbaru.xml',
        'views/gempa_bumi_m_5_0.xml',
        'views/gempa_bumi.xml',
        'data/corn.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
