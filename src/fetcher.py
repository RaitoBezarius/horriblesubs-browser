import requests
import asyncio
from bs4 import BeautifulSoup

class DownloadLink:

    def __init__(self, provider, link):
        self.provider = provider
        self.link = link

class Anime:

    def __init__(self, title, episode, release_date):
        self.title = title
        self.episode = episode
        self.release_date = release_date
        self.versions = set()

        self.download_links = {}

    def __str__(self):
        return '<Anime {title} - {episode} - [{versions}]>'.format(title=self.title, episode=self.episode, versions=', '.join(self.versions))

    def add_version(self, version):
        self.versions.add(version)

    def add_link(self, version, link_type, link):
        if version not in self.download_links:
            self.download_links[version] = []

        self.download_links[version].append(DownloadLink(link_type, link))

class AnimeCollector:

    HORRIBLESUBS_LATEST_API = 'http://horriblesubs.info/lib/latest.php'

    def __init__(self):
        self.animes = set()
        self.loop = asyncio.get_event_loop()

    async def reload_latest(self):
        response = await self.loop.run_in_executor(None, requests.get, self.HORRIBLESUBS_LATEST_API)
        response.raise_for_status()

        return self.parse_response(response.text)

    async def search_links(self, term):
        response = await requests.get(self.HORRIBLESUBS_SEARCH_API, term)
        response.raise_for_status()

        return self.parse_response(response.text)

    def parse_response(self, html_data):
        try:
            soup = BeautifulSoup(html_data, 'html.parser')
            for episode in soup.find_all(attrs={'class': 'episode'}):
                entry = episode.contents[0].split(' ')

                release_date = entry[0]
                title = ' '.join(entry[1:-2])
                episode_id = entry[-1]

                anime = Anime(title, episode_id, release_date)
                for version_block in episode.contents[1]:
                    if version_block.a is None:
                        continue

                    version = version_block.a.text
                    anime.add_version(version)
                    for provider_block in version_block.find_all(attrs={'class': 'ind-link'}):
                        provider = provider_block.text
                        link = provider_block.a['href']

                        anime.add_link(version, provider, link)
                self.animes.add(anime)
        except Exception as e:
            print (e)


