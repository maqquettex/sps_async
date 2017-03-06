import re
import sqlalchemy as sa
from sqlalchemy import select, insert
from sqlalchemy.schema import CreateTable
from asyncpgsa import pg
import asyncpg


meta = sa.MetaData()

artist = sa.Table(
    'artist', meta,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('name', sa.String(200), nullable=False),

)

song = sa.Table(
    'song', meta,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('artist_id', sa.ForeignKey('artist.id'), nullable=False),
    sa.Column('title', sa.String(200), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),

)


async def create_tables_sql(app):

    for name, table in meta.tables.items():
        async with pg.transaction() as conn:
            try:
                await conn.execute(CreateTable(table))
            except asyncpg.exceptions.DuplicateTableError:
                pass


async def get_songs(artist_id=None, artists_to_text=None, notext=None):
    query = song.select()

    if artist_id:
        query = query.where(song.c.artist_id == artist_id)

    results = []
    async with pg.query(query) as cursor:
        async for row in cursor:
            results.append({
                'artist': row.artist_id,
                'title': row.title,
                'id': row.id,
                'text': row.id,
            })

    if artists_to_text is True:
        all_artists = dict()
        async with pg.query(artist.select()) as cursor:
            async for row in cursor:
                all_artists[row.id] = row.name

        for song in results:
            song['artist'] = all_artists[song['artist']]

    if notext is True:
        for song in results:
            song.pop('text')

    return results

async def get_single_song(song_id, artist_to_text=None):
    query = song.select().where(song.c.id == song_id)
    result_song = dict()
    async with pg.query(query) as cursor:
        async for row in cursor:
            result_song.update({
                'artist': row.artist_id,
                'title': row.title,
                'id': row.id,
                'text': row.text
            })
    if result_song == {}:
        return None

    if artist_to_text:
        artist_query = artist.select().where(artist.c.id == result_song['artist'])
        async with pg.query(artist_query) as cursor:
            async for row in cursor:
                result_song['artist'] = row.name
    return result_song


async def get_all_artists():
    query = select([artist.c.id, artist.c.name]).select_from(artist)
    return query
