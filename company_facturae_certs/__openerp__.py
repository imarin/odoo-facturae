{
    'name': "Modulo que administra los certificados de facturación electrónica",
    'version': '1.0',
    'depends': ['document', 'base'],
    'author': "X8BIT SA DE CV",
    'website': 'www.x8bit.com',
    'category': 'Accounting',
    'description': """
    Modulo que administra los certificados de facturación electrónica
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/settings.xml',
    ],
}