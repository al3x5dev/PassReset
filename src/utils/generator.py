def generatePass(base="IInfo*2024"):
    """Generar contraseñas secuenciales que incrementan su longitud.
    Primera: base, luego base+0, base+01, base+012, ... etc."""
    passwords = []
    for i in range(13):
        if i == 0:
            passwords.append(base)
        else:
            passwords.append(base + ''.join(str(d) for d in range(i)))
    return passwords

def verify_password_stored(base="IInfo*2024"):
    """Retorna la primera contraseña del ciclo (la que se usará temporalmente)"""
    return generatePass(base)[0]
