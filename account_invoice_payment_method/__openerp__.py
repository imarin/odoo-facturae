{
    'name': "Agrega método de pago al partner y factura ( 2016 )",
    'version': '1.0',
    'author': "X8BIT SA DE CV",
    'category': 'Localization/Mexico',
    'depends': ['account'],
    'description': """
    Agrega método de pago al partner y factura ( 2016 )
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/pay_method.xml',
        'views/partner.xml',
        'views/invoice.xml',
        'data/payment_method_data.xml',
    ],
    'installable': True,
    'auto_install': False,
}