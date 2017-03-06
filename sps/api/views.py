from aiohttp import web

from . import db

class SongsApiView:

    base_url = '/songs'

    @staticmethod
    def add_routes(app, prefix=None):
        if prefix:
            base_url = prefix + SongsApiView.base_url
        else:
            base_url = SongsApiView.base_url

        app.router.add_get(base_url, SongsApiView.list, name='songs_list')
        app.router.add_get(base_url +'/{id}', SongsApiView.retrieve, name='songs_retrieve')

    @staticmethod
    async def list(request):
        artist = request.rel_url.query.get('artist', '')
        artist = int(artist) if artist.isdigit() else None
        notext = True if 'notext' in request.rel_url.query else None

        artist_to_text = True if 'withnames' in request.rel_url.query else None

        songs = await db.get_songs(artist, artist_to_text, notext)
        return web.json_response(songs)

    @staticmethod
    async def retrieve(request):
        song_id = request.match_info['id']
        if song_id.isdigit():
            song_id = int(song_id)
        else:
            return web.HTTPNotFound()

        artist_to_text = True if 'withnames' in request.rel_url.query else None
        result = await db.get_single_song(song_id, artist_to_text)
        if result is None:
            return web.HTTPNotFound()
        else:
            return web.json_response(result)


class ArtistsApiView:

    base_url = '/artists'

    @staticmethod
    def add_routes(app, prefix=None):
        if prefix:
            base_url = prefix + ArtistsApiView.base_url
        else:
            base_url = ArtistsApiView.base_url

        app.router.add_get(base_url, ArtistsApiView.list, name='artists_list')
        app.router.add_get(base_url +'/{id}', ArtistsApiView.retrieve, name='artists_retrieve')

    @staticmethod
    async def list(request):
        artists = await db.get_artists()
        return web.json_response(artists)

    @staticmethod
    async def retrieve(request):
        artist_id = request.match_info['id']
        if artist_id.isdigit():
            artist_id = int(artist_id)
        else:
            return web.HTTPNotFound()

        songs = request.rel_url.query.get('songs', None)
        print(songs, 'get param')
        if songs == 'full':
            print('1')
            artist = await db.get_single_artist(
                artist_id, select_songs=True, full_songs=True
            )
        elif songs == 'true':
            print('2')
            artist = await db.get_single_artist(
                artist_id, select_songs=True
            )
        else:
            print('0')
            artist = await db.get_single_artist(artist_id)

        if artist is None:
            return web.HTTPNotFound()
        else:
            return web.json_response(artist)
