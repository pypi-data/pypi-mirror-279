# -*- coding: utf-8 -*-
{
    'name': "vertical_carsharing",

    'summary': """
    Modules to masnage your carsharing enerprise using TMF reservation app""",

    'author': "Som Mobilitat",
    'website': "https://www.sommobilitat.coop",

    'category': 'vertical-carsharing',
    'version': '12.0.0.1.7',

    # any module necessary for this one to work correctly
    'depends': [
        'base_vat',
        'base',
        'project',
        'analytic',
        'product_analytic',
    ],

    # always loaded
    'data': [
        'data/sm_account_journal.xml',
        'views/views.xml',
        'views/views_members.xml',
        'views/views_cs_task.xml',
        'views/product_view.xml',
        'views/account_invoice_view.xml',
    ],
    'demo': [],
}
