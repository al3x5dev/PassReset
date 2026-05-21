import flet as ft
from utils.image import getImage

def render():
    return ft.Column([
        ft.Image(getImage('15087926.png'),width=95, height=95),
        ft.Text('PassReset',size=22,weight=ft.FontWeight.W_600),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)