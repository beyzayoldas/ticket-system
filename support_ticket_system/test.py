from weasyprint import HTML
HTML(string='<h1>Merhaba Dünya</h1>').write_pdf('test.pdf')
