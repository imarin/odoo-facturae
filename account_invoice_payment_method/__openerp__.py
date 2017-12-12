{
    'name': "Agrega método de pago al partner y factura ( 2016 )",
    'version': '1.0',
    'author': "X8BIT SA DE CV",
    'category': 'Localization/Mexico',
    'depends': ['account', 'account_invoice_facturae_catalogos'],
    'description': """
    Agrega método de pago al partner y factura ( 2016 )
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/pay_method.xml',
        'views/pay_metodopago.xml',
        'views/partner.xml',
        'views/invoice.xml',
        'data/payment_method_data.xml',
        'data/payment_metodopago_data.xml',
    ],
    'installable': True,
    'auto_install': False,
}