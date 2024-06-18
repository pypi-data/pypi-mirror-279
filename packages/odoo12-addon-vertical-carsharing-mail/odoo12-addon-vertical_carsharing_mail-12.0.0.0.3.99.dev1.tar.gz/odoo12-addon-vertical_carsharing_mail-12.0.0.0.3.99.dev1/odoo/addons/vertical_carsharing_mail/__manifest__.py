# -*- coding: utf-8 -*-
{
    'name': "vertical_carsharing_mail",

    'summary': """
    Modules to manage mail templates""",

    'author': "Som Mobilitat",
    'website': "https://www.sommobilitat.coop",

    'category': 'vertical-carsharing',
    'version': '12.0.0.0.3',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'mail',
        'account'
    ],

    # always loaded
    'data': [
        'data/vc_mail_data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
