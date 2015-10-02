import urwid
import asyncio
from anime_widgets import AnimeList

palette = [
        (None,  'light gray', 'black'),
        ('heading', 'black', 'light gray'),
        ('line', 'black', 'light gray'),
        ('options', 'dark gray', 'black'),
        ('focus heading', 'white', 'dark red'),
        ('focus line', 'black', 'dark red'),
        ('focus options', 'black', 'light gray'),
        ('selected', 'white', 'dark blue')]
focus_map = {
        'heading': 'focus heading',
        'options': 'focus options',
        'line': 'focus line'}

if __name__ == '__main__':
    anime_list = AnimeList()
    evl = urwid.AsyncioEventLoop(loop=asyncio.get_event_loop())
    loop = urwid.MainLoop(anime_list.top, event_loop=evl, palette=palette)
    loop.run()
