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
        app.router.add_post(base_url, SongsApiView.create, name='songs_create')
        app.router.add_post(base_url + '/{id}', SongsApiView.update, name='songs_update')
        app.router.add_delete(base_url + '/{id}', SongsApiView.delete, name='songs_delete')


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

    @staticmethod
    def create(request):
        # db.song.insert().values(
        #     artist_id=int(post_data['artist']),
        #     title=post_data['title'],
        #     text=post_data['text'],
        # )
        redirect_url = request.app.router['songs_list'].url()
        return web.HTTPFound(redirect_url)

    @staticmethod
    def update(request):
        redirect_url = request.app.router['songs_list'].url()
        return web.HTTPFound(redirect_url)

    @staticmethod
    def delete(request):
        redirect_url = request.app.router['songs_list'].url()
        return web.HTTPFound(redirect_url)



