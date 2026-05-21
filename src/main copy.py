import flet as ft
from utils.db import has_password, get_password

APP_NAME = "PassReset"

def main(page: ft.Page):
    """Punto de entrada de la app"""
    
    page.title = APP_NAME
    #page.theme_mode = ft.ThemeMode.DARK
    page.theme_mode = ft.Colors.BLUE_700
    page.window.width = 400
    page.window.height = 600
    
    current_master_key = {"key": None}
    current_password = {"pass": None}
    
    def go_home():
        page.clean()
        # Botón Iniciar Reset
        def on_reset_click(e):
            if current_master_key.get("key"):
                current_password["pass"] = get_password(current_master_key["key"])
            # Ir a reset
            page.clean()
            from views.reset import reset_view
            reset_view(page, go_home, current_password.get("pass") or "test")
        
        # Botón Cambiar Clave
        def on_settings_click(e):
            page.clean()
            from views.settings import settings_view
            settings_view(page, go_home)
        
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        page.add(
            ft.Text(APP_NAME, size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Text("─────────────", text_align=ft.TextAlign.CENTER),
            ft.Container(height=20),
            ft.Button("🔄 Iniciar Reset", width=300, on_click=on_reset_click),
            ft.Container(height=10),
            ft.Button("⚙ Cambiar Clave", width=300, on_click=on_settings_click, mode=ft.ButtonMode.OUTLINE),
            ft.Container(height=20),
            ft.Text("● Conectado", size=12, color=ft.Colors.GREEN)
        )
    
    def go_setup():
        page.clean()
        
        master_key_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
        status_text = ft.Text("● Desconectado", size=12, color=ft.Colors.RED)
        
        def on_save_click(e):
            key = master_key_field.value
            if not key or len(key) < 8:
                master_key_field.error_text = "Mínimo 8 caracteres"
                page.update()
                return
            
            from utils.db import init_db, save_password
            init_db()
            save_password(key, "myPassw0rd*1")
            current_master_key["key"] = key
            go_home()
        
        #page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        page.add(
            ft.Column([
                ft.Text(APP_NAME, size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Container(expand=TRUE),
                ft.Column([master_key_field], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Button("GUARDAR", width=250, on_click=on_save_click),
                ft.Container(expand=TRUE),
                status_text
            ]),
        )
    
    # Verificar BD
    if has_password():
        go_home()
    else:
        go_setup()

ft.app(target=main)