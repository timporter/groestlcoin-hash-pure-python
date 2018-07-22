from .groestl import groestl

def groestl_hash(n, message):
    """Double groestl512 hash."""
    result = groestl(n).digest(message)
    return result #groestl(512).digest(result)[:32]
