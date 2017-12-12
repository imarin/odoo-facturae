{
    'name': "Agrega Uso CFDI al invoice ( cfdi 3.3 )",
    'version': '1.0',
    'author': "X8BIT SA DE CV",
    'category': 'Localization/Mexico',
    'depends': ['account_invoice_facturae_catalogos'],
    'description': """
        Agrega Uso CFDI al invoice ( cfdi 3.3 )
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/usocfdi.xml',
        'views/invoice.xml',
        'data/invoice_usocfdi.xml',
    ],
    'installable': True,
    'auto_install': False,
}