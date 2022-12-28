import json

from spotcrates.filters import FieldName


def file_json(file_loc):
    with open(file_loc, 'r') as playlist_list_handle:
        return json.load(playlist_list_handle)


def load_playlist_listing_file(file_loc):
    raw_data = file_json(file_loc)
    playlist_entries = []
    for playlist in raw_data:
        desc_entry = {FieldName.PLAYLIST_NAME: playlist["name"], FieldName.SIZE: playlist["tracks"]["total"],
                      FieldName.OWNER: playlist["owner"]["id"],
                      FieldName.PLAYLIST_DESCRIPTION: playlist["description"]}
        playlist_entries.append(desc_entry)
    return playlist_entries
