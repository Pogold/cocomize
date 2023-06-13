# Загружаем файл с QSS стилями

extra = {

    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',

    # Font
    'font_family': 'Montserrat',
}



qss_file = "styles/ubuntu.qss"
style_sheet = ""
with open(qss_file, "r") as f:
    style_sheet = f.read()

