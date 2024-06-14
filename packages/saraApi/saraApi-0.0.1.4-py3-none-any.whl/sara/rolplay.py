from .req import get

__version__ = '1.1.8'
class LimitExceeded(Exception):
    pass

def lewdbomb(n: int):
    if n > 20:
        raise LimitExceeded("[AKANEKO] The amound is too great than 20!")
    if n <= 0:
        n = 5
    urls = []
    for _ in range(int(n)):
        r = get('random')
        urls.append(r)
    return urls

def baka():
    return get('baka')
def kiss():
    return get('kiss')
def kill():
    return get('kill')
def spank():
    return get('spank')
def punch():
    return get('punch')
def poke():
    return get('poke')