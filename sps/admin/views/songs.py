import aiohttp_jinja2
from api.db import song, artist
from aiohttp import web


class SongsAdminView:

    base_url = '/songs'

    @staticmethod
    def add_routes(app, prefix=None):
        base_url = SongsAdminView.base_url
        if prefix:
            base_url = '/' + prefix + base_url

        app.router.add_get(base_url, SongsAdminView.list, name='admin_songs_list')
        app.router.add_get(base_url + '/{id}', SongsAdminView.retrieve, name='admin_songs_retrieve')
        #app.router.add_post(base_url, SongsAdminView.create, name='admin_songs_create')
        #app.router.add_post(base_url + '/{id}', SongsAdminView.update, name='admin_songs_update')
        #app.router.add_delete(base_url + '/{id}', SongsAdminView.delete, name='admin_songs_delete')

    @staticmethod
    @aiohttp_jinja2.template('admin/song/list.html')
    async def list(request):
        q = song.select()

        all_artists = {}
        async with request.app['pool'].acquire() as conn:
            for row in await conn.fetch(artist.select()):
                all_artists[row.id] = row.name

        results = []
        async with request.app['pool'].acquire() as conn:
            for row in await conn.fetch(q):
                results.append({
                    'artist_id': row.artist_id,
                    'artist_name': all_artists[row.artist_id],
                    'title': row.title,
                    'id': row.id,
                    'text': row.id,
                })

        return {
            'songs': results
        }

    @staticmethod
    @aiohttp_jinja2.template('admin/song/retrieve.html')
    async def retrieve(request):
        id = int(request.match_info['id'])
        q = song.select().where(song.c.id == id)
        async with request.app['pool'].transaction() as conn:
            song_row = await conn.fetchrow(q)

        artists = []
        async with request.app['pool'].acquire() as conn:
            for row in await conn.fetch(artist.select()):
                artists.append({
                    'id': row.id,
                    'name': row.name
                })

        return {
            'song': {
                'artist_id': song_row.artist_id,
                'title': song_row.title,
                'id': song_row.id,
                'text': song_row.text
            },
            'artists': artists
        }


