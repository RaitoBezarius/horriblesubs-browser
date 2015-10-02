import urwid
import asyncio
from fetcher import AnimeCollector
from fetcher import Anime

class IndefiniteProgressBar(urwid.Text):

    def __init__(self):
        super(IndefiniteProgressBar, self).__init__("Loading")
        self.loop = asyncio.get_event_loop()

        self.step = 0
        self.delay = 0.1

        self.loop.call_later(self.delay, self.update_random_progress)

    def update_random_progress(self):
        self.set_text("{}".format(self.text) + '.' * (self.step + 1))
        self.step = (self.step + 1) % 3
        self.loop.call_later(self.delay, self.update_random_progress)

class LatestAnimeList(urwid.WidgetWrap):

    def __init__(self, collector):
        self.collector = collector
        self.title = urwid.Padding(urwid.Text("Latest animes"), 'center', 'pack')
        self.listbox = urwid.ListBox(urwid.SimpleFocusListWalker([urwid.Padding(IndefiniteProgressBar(), 'center', ('relative', 50))]))
        self.frame = urwid.Frame(self.listbox, self.title)

        super(LatestAnimeList, self).__init__(self.frame)
        asyncio.ensure_future(self.collector.reload_latest()).add_done_callback(self.anime_fetched)

    def pad_anime(self, anime):
        return urwid.Padding(anime, 'center', 'pack')

    def anime_fetched(self, future):
        animes = list(map(self.pad_anime, map(wrap_anime, self.collector.animes)))
        self.listbox = urwid.ListBox(urwid.SimpleFocusListWalker([urwid.Divider()] + animes))
        self.frame.body = self.listbox

def wrap_anime(anime):
    text = '{anime.title} - {anime.episode} {anime.release_date}'.format(anime=anime)
    return urwid.AttrMap(urwid.SelectableIcon(text, cursor_position=0), '', focus_map='selected')

class AnimeList:

    def __init__(self):
        self.collector = AnimeCollector()
        self.top = self.center_widget(urwid.LineBox(LatestAnimeList(self.collector)))

    def center_widget(self, w):
        return urwid.Filler(urwid.Padding(w, 'center', 50), 'middle', 30)
