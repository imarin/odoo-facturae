{
    'name': "Agrega regimen fiscal al partner ( cfdi 3.3 )",
    'version': '1.0',
    'author': "X8BIT SA DE CV",
    'category': 'Localization/Mexico',
    'depends': ['account_invoice_facturae_catalogos'],
    'description': """
        Agrega regimen fiscal al partner ( cfdi 3.3 )
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/regimenfiscal.xml',
        'views/partner.xml',
        'data/partner_regimenfiscal.xml',
    ],
    'installable': True,
    'auto_install': False,
}