from source.database.database import SessionLocal
from source.database.models import Auditoria
from datetime import datetime

def registrar_accion(usuario_id, accion, descripcion=None):
    """
    Registra una acción en la tabla de auditoría.

    :param usuario_id: ID del usuario que realiza la acción.
    :param accion: Descripción breve de la acción realizada.
    :param descripcion: Detalles adicionales sobre la acción.
    """
    session = SessionLocal()
    try:
        nuevo_evento = Auditoria(
            usuario_id=usuario_id,
            accion=accion,
            descripcion=descripcion,
            fecha=datetime.now()
        )
        session.add(nuevo_evento)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
