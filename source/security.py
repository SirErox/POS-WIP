import bcrypt
#para hashear una contraseña
def hashear_contra(contraseña):
    return bcrypt.hashpw(contraseña.encode('utf-8'),bcrypt.gensalt())
#para verificar una contraseña
def verificar_contra(contraseña,hash_almacenado):
    return bcrypt.checkpw(contraseña.encode('utf-8'),hash_almacenado)