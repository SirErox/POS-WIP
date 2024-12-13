import bcrypt
#para hashear una contraseña
def hashear_contra(contraseña):
    return bcrypt.hashpw(contraseña.encode('utf-8'),bcrypt.gensalt())
#para verificar una contraseña
def verificar_contra(contraseña,hash_almacenado):
    if isinstance(hash_almacenado, str):  # Asegurar que el hash esté en formato bytes
        hash_almacenado = hash_almacenado.encode('utf-8')
    return bcrypt.checkpw(contraseña.encode('utf-8'), hash_almacenado)
