from aiohttp import web


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
    def list(request):
        return web.json_response({'type': 'LIST'})

    @staticmethod
    def retrieve(request):
        return web.json_response({'type':'RETRIEVE'})

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



