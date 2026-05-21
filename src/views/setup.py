import flet as ft
from utils.db import init_db, save_password
from . import footer, hero


def render(page,current_master_key, go_home):
    page.clean()

    info_text = ft.Text('Especifiqué contraseña actual de su sesión')
    master_key_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    btn_save = ft.Button("💾 REGISTRAR", on_click=None, disabled=True)

    def on_text_change(e):
        valido = len(master_key_field.value or "") >= 8
        btn_save.disabled = not valido
        
        if valido:
            btn_save.on_click = on_save_click
        else:
            btn_save.on_click = None
        
        #info_text.value = ''
        page.update()

    master_key_field.on_change = on_text_change

    def on_save_click(e):
        key = master_key_field.value

        init_db()
        save_password(key)
        current_master_key["key"] = key
        go_home()

    page.add(
        ft.Row(controls=[
            ft.Column([
                hero.render(),
                ft.Container(height=20),
                info_text,
                master_key_field,
                btn_save,
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centra horizontal
            #alignment=ft.MainAxisAlignment.CENTER,               # centra vertical
            expand=True,  )
        ], expand=True),
        footer.render()
    )
