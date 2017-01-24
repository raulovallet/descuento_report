{
'name': "Descuento Report",
'description' : "Agrega la columna descuento en el reporte sale_order y el campo suma total de los descuentos",
'version' : "1.0",
'author' : "Raul Ovalle, xmarts.com",
'depends' : ['sale'],
'data': ['views/sale_order_view.xml',
         'views/account_invoice_view.xml',
         'views/partner_category_view.xml',
         'reports/sale_order_report.xml',
         'reports/account_invoice_report.xml'
          ],
'installable' : True,
}