from api.db import song, artist


async def update_indexes(es, pg):

    songs = []
    query = song.select()

    async with pg.transaction() as conn:
        results = await conn.fetch(query)

    for row in results:
        songs.append({
            'artist': row.artist_id,
            'title': row.title,
            'id': row.id,
            # Should be uncommented after text search realisation
            # 'text': row.text,
        })

    all_artists = dict()
    async with pg.transaction() as conn:
        for row in await conn.fetch(artist.select()):
            all_artists[row.id] = row.name

    for s in songs:

        await es.index(
            index='library',
            doc_type='song',
            body={
                'title': s['title'].lower(),
                'artist': all_artists[s['artist']].lower(),
            },
            id=s['id']
        )

