{
    'name': "Lunch Buffalo",
    'summary': """""",
    'description': """
        """,
    'author': "Odoo Development Services",
    'maintainer': "Odoo Development Services",
    'website': "https://www.odoo.com/",
    'category': "Custom Development",
    'version': "18.0.1.0.0",
    'license': "OPL-1",
    'depends': ['product', 'website_event', 'hr_attendance'],
    'data': [
        "security/ir.model.access.csv",
        'data/lunch_data.xml',
        # 'data/food_items.xml',
        'views/lunch_templates.xml',
        "views/product_views.xml",
        "views/menu_views.xml",
        # 'views/hr_attendance_kiosk_templates.xml'
    ],
    'assets': {
        'hr_attendance.assets_public_attendance': [
            "lunch_buffalo/static/src/public_kiosk/**/*",
        ]
    },
    'application': False,
}
