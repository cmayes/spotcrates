class Playlist:
    def __init__(self):
        self.description
        self.image_links
        self.is_public
        self.name
        self.owner
        # might be useful for refreshes: does this stay the same if there are no changes?
        self.snapshot_id
        self.spotify_id
        self.tracks

class Track:
    def __init__(self):
        self.added_at
        self.added_by
        self.album
        self.disc_number
        self.duration
        # International Standard Recording Code
        self.isrc
        self.popularity
        self.spotify_id
        self.track_number
        # Is this ever not "track?"
        self.type
        # Maybe that short clip on mobile
        self.video_thumbnail

class Album:
    def __init__(self):
        self.added_at
        self.images
        # International Standard Recording Code
        self.isrc
        self.name
        self.release_date
        self.spotify_id
        self.total_tracks
        # Is this ever not "album?"
        self.type

class Artist:
    def __init__(self):
        self.added_at
        self.images
        self.name
        self.spotify_id
        # Is this ever not "artist?"
        self.type

class Image:
    def __init__(self):
        self.height
        self.url
        self.width

        "episode": false,
        "explicit": false,
        "external_ids": {
            "isrc": "USF096625790"
        },
        "external_urls": {
            "spotify": "https://open.spotify.com/track/5Hbd5ZazhinrRP6mS5XaR1"
        },
        "href": "https://api.spotify.com/v1/tracks/5Hbd5ZazhinrRP6mS5XaR1",
        "id": "5Hbd5ZazhinrRP6mS5XaR1",
        "is_local": false,
        "name": "Flute Thing",
        "popularity": 33,
        "preview_url": "https://p.scdn.co/mp3-preview/2b735d2598fa4a9b89ab5cc47c995cd185d2f8a8?cid=1b9a197c02e449e0b42aef69c2dc98ef",
        "track": true,
        "track_number": 7,
        "type": "track",
        "uri": "spotify:track:5Hbd5ZazhinrRP6mS5XaR1"
    },
    "video_thumbnail": {
        "url": null
    }
},