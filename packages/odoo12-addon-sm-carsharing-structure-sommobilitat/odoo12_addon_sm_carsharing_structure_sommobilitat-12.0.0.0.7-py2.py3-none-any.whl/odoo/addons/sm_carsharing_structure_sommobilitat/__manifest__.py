# -*- coding: utf-8 -*-
{
    'name': "sm_carsharing_structure_sommobilitat",

    'summary': """
         Extra fields any enterprise would need to add to fleet vehicle""",

    'author': "Som Mobilitat",
    'website': "https://www.sommobilitat.coop",

    'category': '',
    'version': '12.0.0.0.7',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'vertical_carsharing',
        'fleet',
        'sm_carsharing_structure',
        'account_loan',
        'analytic',
    ],

    # always loaded
    'data': [
        'data/fleet_vehicle_state.xml',
        'views/fleet_vehicle_state_view.xml',
        'views/views_cs_car.xml',
        'views/views_res_config_settings.xml',
    ],
}
