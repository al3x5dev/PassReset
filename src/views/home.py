import flet as ft
from . import hero, footer, reset, settings


def render(page):
    page.clean()
    """Menú principal de la app"""
    
    def go_reset(e):
        return reset.render(page)
    def go_settings(e):
        return settings.render(page)
    
    page.add(
        ft.Row([
            ft.Column([
                hero.render(),
                ft.Container(),
                ft.Button('🔄 RESTABLECER', on_click=go_reset),
                ft.Button('🔑 CAMBIAR CONTRASEÑA', on_click=go_settings),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True)
        ], expand=True),
        footer.render()
    )