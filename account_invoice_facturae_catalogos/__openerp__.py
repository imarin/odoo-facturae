{
    'name': "Agrega menu de catálogos",
    'version': '1.0',
    'author': "X8BIT SA DE CV",
    'category': 'Localization/Mexico',
    'depends': ['account'],
    'description': """
    Agrega menu de catálogos
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/catalogos.xml',
    ],
    'installable': True,
    'auto_install': False,
}