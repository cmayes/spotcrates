import datetime

from sqlalchemy import Text, String, Boolean, Integer, DateTime, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column


class Base(DeclarativeBase):
    pass


class Playlist(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(1024))
    description: Mapped[str] = mapped_column(Text())
    images: Mapped[list["PlaylistImage"]] = relationship(back_populates="playlist")
    is_public: Mapped[bool] = mapped_column(Boolean()),
    owner: Mapped[str] = mapped_column(String(255)),
    # might be useful for refreshes: does this stay the same if there are no changes?
    snapshot_id: Mapped[str] = mapped_column(String(100)),
    spotify_id: Mapped[str] = mapped_column(String(50)),
    tracks_count: Mapped[int] = mapped_column(Integer)
    tracks_link: Mapped[str] = mapped_column(Text())
    tracks: Mapped[list["PlaylistTrack"]] = relationship(back_populates="playlist")


class PlaylistImage(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    height: Mapped[int] = mapped_column(Integer)
    width: Mapped[int] = mapped_column(Integer)
    url: Mapped[str] = mapped_column(Text)
    playlist: Mapped[["Playlist"]] = relationship(back_populates="images")


class PlaylistTrack(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    added_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    added_by: Mapped[str] = mapped_column(String(255))
    # link to album track?
    playlist: Mapped[["Playlist"]] = relationship(back_populates="tracks")


class Album(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    added_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    name: Mapped[str] = mapped_column(String(1024))
    # International Standard Recording Code
    isrc: Mapped[str] = mapped_column(String(50)),
    release_date: Mapped[datetime.date] = mapped_column(Date)
    spotify_id: Mapped[str] = mapped_column(String(50)),
    tracks_count: Mapped[int] = mapped_column(Integer)
    # Is this ever not "album?"
    album_type: Mapped[str] = mapped_column(String(30))
    # Link with image class
    images: Mapped[list["AlbumImage"]] = relationship(back_populates="album")
    tracks: Mapped[list["PlaylistTrack"]] = relationship(back_populates="album")
    artist: Mapped[["Artist"]] = relationship(back_populates="albums")


class AlbumImage(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    height: Mapped[int] = mapped_column(Integer)
    width: Mapped[int] = mapped_column(Integer)
    url: Mapped[str] = mapped_column(Text)
    album: Mapped[["Album"]] = relationship(back_populates="images")


class AlbumTrack(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    # album link
    disc_number: Mapped[int] = mapped_column(Integer)
    duration_ms: Mapped[int] = mapped_column(Integer)
    # International Standard Recording Code
    isrc: Mapped[str] = mapped_column(String(30))
    popularity: Mapped[int] = mapped_column(Integer)
    spotify_id: Mapped[str] = mapped_column(String(50)),
    track_number: Mapped[int] = mapped_column(Integer)
    # Is this ever not "track?"
    track_type: Mapped[str] = mapped_column(String(30))
    # Maybe that short clip on mobile
    video_thumbnail_url: Mapped[str] = mapped_column(Text)
    album: Mapped[["Album"]] = relationship(back_populates="tracks")


class Artist(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    added_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    # one-to-many (maybe many-to-many)
    # self.images
    name: Mapped[str] = mapped_column(String(1024))
    spotify_id: Mapped[str] = mapped_column(String(50)),
    # Is this ever not "artist?"
    artist_type: Mapped[str] = mapped_column(String(30))
    albums: Mapped[list["Album"]] = relationship(back_populates="artist")