import flet as ft
from utils.db import delete_all, get_password, save_password
from . import hero, home,footer


def render(page):
    page.clean()


    def go_home():
        home.render(page)

    def validate(e):
        input1=old_pass.value or ""
        input2=new_pass.value or ""
        btn.disabled = not (len(input1)>=8 and len(input2)>=8)
        page.update()
    
    def update(e):
        save_password(new_pass.value)
        old_pass.read_only=True
        new_pass.read_only=True
        page.show_dialog(ft.SnackBar(ft.Text("Clave cambiada exitosamente"),bgcolor=ft.Colors.GREEN_700))
        e.control.visible=False
        page.update()

    btn = ft.Button('✏️ ACTUALIZAR',disabled=True, on_click=update)
    old_pass = ft.TextField(label="Clave Actual",
        password=True,
        can_reveal_password=True,
        width=300,
        value=get_password(),
        on_change=validate)
    new_pass = ft.TextField(
        label='Nueva Clave',
        password=True,
        can_reveal_password=True,
        width=300,
        on_change=validate)

    page.add(
        ft.Row([
            ft.Column([
                hero.render(),
                old_pass,
                new_pass,
                btn,
                ft.Button('🏠 IR AL INICIO', on_click=go_home)

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True)
        ], expand=True),
        footer.render()
    )