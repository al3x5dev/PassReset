import os
import logging
import ctypes

logger = logging.getLogger(__name__)

_ERROR_CODES = {
    0: "Cambio exitoso",
    86: "Contraseña actual incorrecta",
    1326: "Usuario o contraseña incorrectos",
    1331: "Cuenta deshabilitada",
    1907: "La contraseña no cumple la política de seguridad (longitud, caracteres o historial)",
    2221: "Usuario no encontrado",
    2242: "La contraseña ha expirado",
    2246: "No se permite el mismo password (historial de contraseñas)",
    2249: "Debe cambiar la contraseña",
    2691: "El servidor no está disponible",
}

def get_system_user():
    username = os.environ.get('USERNAME', '')
    userdomain = os.environ.get('USERDOMAIN', '')
    return username, userdomain

def change_ad_password(password_actual: str, password_nuevo: str) -> dict:
    username, userdomain = get_system_user()
    logger.info("change_ad_password: usuario=%s, dominio=%s", username, userdomain)

    try:
        netapi32 = ctypes.windll.netapi32
        netapi32.NetUserChangePassword.argtypes = [
            ctypes.c_wchar_p,
            ctypes.c_wchar_p,
            ctypes.c_wchar_p,
            ctypes.c_wchar_p,
        ]
        netapi32.NetUserChangePassword.restype = ctypes.c_long

        status = netapi32.NetUserChangePassword(
            userdomain,
            username,
            password_actual,
            password_nuevo,
        )

        if status == 0:
            logger.info("Password cambiado exitosamente")
            return {'success': True, 'message': 'Password cambiado exitosamente'}

        error_msg = _ERROR_CODES.get(status, f"Error código {status}")
        logger.error("NetUserChangePassword falló: %s", error_msg)
        return {'success': False, 'message': error_msg}

    except Exception as e:
        logger.error("Error al llamar NetUserChangePassword: %s", e)
        return {'success': False, 'message': str(e)}
