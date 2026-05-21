import flet as ft
from utils.db import has_password
from utils.image import getImage
from utils import logs
import views as vw

APP_NAME = "PassReset"

async def main(page: ft.Page):
    """Punto de entrada de la app"""
    
    page.title = APP_NAME + ' v0.1'
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.random())
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.window.width = 400
    page.window.height = 500

    page.window.icon = getImage("favicon.ico")

    page.window.resizable=False
    page.window.maximizable = False

    page.update()                  # <-- aplica tamaño ANTES de centrar
    await page.window.center()     # <-- ahora centra con 400x500

    current_master_key = {"key": None}
    #current_password = {"pass": None}
    
    def go_home():
        vw.home.render(page)
    
    def go_setup():
        vw.setup.render(page, current_master_key, go_home)

    
    # Verificar BD
    if has_password():
        go_home()
    else:
        go_setup()


ft.run(main)