{
    'name': "Agrega claves a los productos ( cfdi 3.3 )",
    'version': '1.0',
    'author': "X8BIT SA DE CV",
    'category': 'Localization/Mexico',
    'depends': ['account_invoice_facturae_catalogos'],
    'description': """
        Agrega claves a los productos ( cfdi 3.3 )
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/claveprodserv.xml',
        'views/claveunidad.xml',
        'views/product.xml',
        'data/product_claves.xml',
        'data/product_claveunidad.xml',
    ],
    'installable': True,
    'auto_install': False,
}