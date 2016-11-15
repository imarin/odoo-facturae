{
    'name': "Modulo que agrega la facturación electrónica a los invoices de odoo",
    'version': '1.0',
    'depends': [
        'document',
        'company_facturae_certs',
        'account_invoice_payment_method',
        'partner_facturae_address',
        'account_invoice_amount_to_text'
    ],
    'author': "X8BIT SA DE CV",
    'website': 'www.x8bit.com',
    'category': 'Accounting',
    'description': """
    Modulo que agrega la facturación electrónica a los invoices de odoo

    apt-get install python-m2crypto
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/invoice_facturae.xml',
        'views/invoice_pdf_report.xml',
    ],
}