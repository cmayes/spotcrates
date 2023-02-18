import logging
from typing import List, Set, Dict, Optional

from spotipy import Spotify

from spotcrates.common import batched, get_all_items
from spotcrates.filters import FieldName, filter_list, sort_list

config_defaults = {
    "daily_mix_prefix": "Daily Mix",
    "daily_mix_target": "Now",
    "daily_mix_exclude_prefix": "Overplayed",
}


class PlaylistException(Exception):
    pass


class Playlists:
    def __init__(self, spotify: Spotify, config: Optional[Dict] = None):
        self.spotify = spotify
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.config = self._process_config(config)

    def get_all_playlists(self) -> List[Dict]:
        return get_all_items(self.spotify, self.spotify.current_user_playlists())

    def list_all_playlists(self, sort_fields=None, filters=None) -> List[Dict]:
        playlist_entries = []
        for playlist in self.get_all_playlists():
            playlist_entries.append(
                {
                    FieldName.SPOTIFY_ID: playlist["id"],
                    FieldName.PLAYLIST_NAME: playlist["name"],
                    FieldName.SIZE: playlist["tracks"]["total"],
                    FieldName.OWNER: playlist["owner"]["id"],
                    FieldName.PLAYLIST_DESCRIPTION: playlist["description"],
                }
            )

        if not sort_fields and not filters:
            return playlist_entries

        processed_entries = playlist_entries
        if filters:
            processed_entries = filter_list(processed_entries, filters)

        if sort_fields:
            processed_entries = sort_list(processed_entries, sort_fields)

        return processed_entries

    def append_daily_mix(self):
        dailies = []
        target_list = None
        exclude_lists = []
        daily_mix_prefix = self.config.get("daily_mix_prefix")
        daily_mix_target = self.config.get("daily_mix_target")
        daily_mix_exclude_prefix = self.config.get("daily_mix_exclude_prefix")
        for playlist in self.get_all_playlists():
            list_name = playlist["name"]
            if list_name:
                if list_name.startswith(daily_mix_prefix):
                    dailies.append(playlist)
                elif list_name == daily_mix_target:
                    target_list = playlist
                elif list_name.startswith(daily_mix_exclude_prefix):
                    exclude_lists.append(playlist)

        # TODO: Optionally create if it doesn't exist
        if not target_list:
            me = self.spotify.me()

            target_list = self.spotify.user_playlist_create(
                me["id"], daily_mix_target, public=False
            )

        # user_playlist_add_tracks(user, playlist_id, tracks, position=None)
        if not dailies:
            self.logger.warning(
                f"No daily mixes found with the prefix '{daily_mix_prefix}'"
            )

        exclude_ids = self._get_playlist_track_ids(target_list["id"])

        for exclude_list in exclude_lists:
            exclude_ids.update(self._get_playlist_track_ids(exclude_list["id"]))

        add_tracks = []
        orig_daily_count = 0
        for daily in dailies:
            daily_items = self._get_playlist_tracks(daily["id"])
            orig_daily_count += len(daily_items)
            add_tracks.extend(
                [
                    daily_item
                    for daily_item in daily_items
                    if daily_item["track"]["id"] not in exclude_ids
                ]
            )

        self.logger.info(
            f"{len(add_tracks)} to add from an original count of {orig_daily_count}"
        )
        if add_tracks:
            self._add_tracks_to_playlist(target_list, add_tracks)
        else:
            self.logger.warning("No daily songs to add")

    def _get_playlist_track_ids(self, *args: str) -> Set[str]:
        track_ids = set()
        for playlist_id in args:
            # TODO: See about paring down to just the ID via "fields" param
            playlist_items = get_all_items(
                self.spotify, self.spotify.playlist_items(playlist_id)
            )
            track_ids.update(
                {playlist_item["track"]["id"] for playlist_item in playlist_items}
            )

        return track_ids

    def _get_playlist_tracks(self, *args: str) -> List[dict]:
        tracks = []
        for playlist_id in args:
            # TODO: See about paring down to just the ID via "fields" param
            tracks.extend(
                get_all_items(self.spotify, self.spotify.playlist_items(playlist_id))
            )

        return tracks

    def _add_tracks_to_playlist(self, target_list, add_tracks):
        track_ids = {add_song["track"]["id"] for add_song in add_tracks}

        for id_batch in batched(track_ids, 100):
            self.logger.debug(f"Batch size: {len(id_batch)}")
            self.spotify.playlist_add_items(target_list["id"], id_batch)

    @staticmethod
    def _process_config(config: Optional[Dict]) -> Dict:
        processed_config = {}

        source_config = {}
        if config:
            source_config = config

        for key, default_value in config_defaults.items():
            processed_config[key] = source_config.get(key, default_value)

        return processed_config
