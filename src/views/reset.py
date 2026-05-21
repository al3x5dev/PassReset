import flet as ft
import asyncio
import logging
from utils.generator import generatePass
from utils.db import get_password, save_password, has_password
from utils.password import change_ad_password
from . import hero, footer, home

logger = logging.getLogger(__name__)

def render(page):
    page.clean()

    def go_home():
        home.render(page)

    btn_home = ft.Button('🏠 IR AL INICIO', on_click=go_home, disabled=True)
    input_text = ft.TextField(label='', value='', read_only=True)
    progress = ft.ProgressBar(value=0, width=300)
    status_text = ft.Text("", size=14)

    def start_cycle():
        asyncio.create_task(ciclo_reset())

    page.add(
        ft.Row([
            ft.Column([
                hero.render(),
                ft.Container(height=10),
                input_text,
                ft.Container(height=10),
                progress,
                ft.Container(height=10),
                status_text,
                ft.Container(height=10),
                btn_home,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        ], expand=True),
        footer.render()
    )

    async def ciclo_reset():
        logger.info("ciclo_reset iniciado")

        if not has_password():
            logger.error("No hay contraseña guardada en BD")
            status_text.value = "Error: no hay contraseña guardada"
            status_text.color = ft.Colors.RED_400
            page.update()
            return

        actual = get_password()
        if not actual:
            logger.error("Contraseña vacía en BD")
            status_text.value = "Error: contraseña vacía en BD"
            status_text.color = ft.Colors.RED_400
            page.update()
            return

        original = actual
        loop = asyncio.get_event_loop()
        passwords = [p for p in generatePass() if p != actual]
        if not passwords:
            status_text.value = "Error: no se pudieron generar contraseñas"
            status_text.color = ft.Colors.RED_400
            page.update()
            return

        total = len(passwords)
        logger.info("Iniciando ciclo de %d cambios", total)

        for i, pwd in enumerate(passwords):
            input_text.label = f"Cambio {i+1} de {total}"
            input_text.value = pwd
            progress.value = (i + 1) / total
            status_text.value = f"Cambiando a {pwd}..."
            status_text.color = ft.Colors.YELLOW
            page.update()

            logger.info("Cambiando a %s (paso %d/%d)...", pwd, i + 1, total)
            try:
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, change_ad_password, actual, pwd),
                    timeout=30
                )
            except asyncio.TimeoutError:
                logger.error("Timeout paso %d", i + 1)
                status_text.value = f"Error paso {i+1}: Timeout"
                status_text.color = ft.Colors.RED_400
                page.update()
                return

            if not result['success']:
                logger.error("Error paso %d: %s", i + 1, result['message'])
                status_text.value = f"Error paso {i+1}: {result['message']}"
                status_text.color = ft.Colors.RED_400
                page.update()
                return

            logger.info("Paso %d completado: %s", i + 1, pwd)
            actual = pwd
            await asyncio.sleep(1)

        status_text.value = "Revertiendo a contraseña original..."
        status_text.color = ft.Colors.YELLOW
        page.update()
        logger.info("Revirtiendo a contraseña original...")
        try:
            result = await asyncio.wait_for(
                loop.run_in_executor(None, change_ad_password, actual, original),
                timeout=30
            )
        except asyncio.TimeoutError:
            logger.error("Timeout al revertir")
            status_text.value = "Error: Timeout al revertir"
            status_text.color = ft.Colors.RED_400
            page.update()
            return

        if not result['success']:
            logger.error("Error al revertir: %s", result['message'])
            status_text.value = f"Error al revertir: {result['message']}"
            status_text.color = ft.Colors.RED_400
            page.update()
            return

        save_password(original)
        status_text.value = "Ciclo completado exitosamente"
        status_text.color = ft.Colors.GREEN_400
        btn_home.disabled = False
        page.update()
        logger.info("Ciclo de reset completado exitosamente")

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar restablecimiento"),
        content=ft.Text(
            "Se realizarán 13 cambios de contraseña consecutivos.\n"
            "Asegúrese de que su contraseña actual esté correctamente guardada.\n"
            "¿Desea continuar?",
            size=14
        ),
        actions=[
            ft.TextButton("CANCELAR", on_click=lambda e: (setattr(e.control.page.dialog, 'open', False), e.control.page.update())),
            ft.TextButton("INICIAR", on_click=lambda e: (setattr(e.control.page.dialog, 'open', False), e.control.page.update(), start_cycle())),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.dialog = dlg
    dlg.open = True
    page.update()
