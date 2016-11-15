{
    'name': "Modulo para timbrado con PAC finkok",
    'version': '1.0',
    'depends': [
        'account_invoice_facturae'
    ],
    'author': "X8BIT SA DE CV",
    'website': 'www.x8bit.com',
    'category': 'Accounting',
    'description': """
        Modulo para timbrado con PAC finkok
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
    ],
}