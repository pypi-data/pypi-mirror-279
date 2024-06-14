
from .req import get
from .reqBoo import getBoo

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

def ass():
    return get('ass')

def boobs():
    return get('boobs')

def ahegao():
    return get('ahegao')

def bdsm():
    return get('bdsm')

def bondage():
    return get('bdsm')

def cum():
    return get('cum')

def hentai():
    return get('hentai')

def femdom():
    return get('femdom')

def doujin():
    return getBoo('doujinshi')

def maid():
    return get('maid')

def orgy():
    return getBoo('orgy')

def panties():
    return get('panties')

def wallpapers():
    return get('nsfwwallpapers')

def mobileWallpapers():
    return get('nsfwmobilewallpapers')

def netorare():
    return getBoo('netorare animated_gif')

def cuckold():
    return get('netorare')

def gifs():
    return get('gifs')

def gif():
    return get('gif')

def blowjob():
    return get('blowjob')

def feet():
    return get('feet')

def pussy():
    return get('pussy')

def uglyBastard():
    return getBoo('ugly_man')

def uniform():
    return getBoo('school_uniform sex')

def gangbang():
    return get('gangbang')

def foxgirl():
    return get('foxgirl')

def cumslut():
    return get('cumslut')

def glasses():
    return get('glasses')

def thighs():
    return getBoo('thighs gif')

def tentacles():
    return get('tentacles animated_gif')

def masturbation():
    return get('masturbation')

def school():
    return getBoo('school sex')

def yuri():
    return get('yuri')

def zettaiRyouiki():
    return get('zettaiRyouiki')

def zettairyouiki():
    return get('zettaiRyouiki')

def succubus():
    return getBoo("demon_girl animated_gif")
