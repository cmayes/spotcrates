#!/usr/bin/env python

"""
CLI runner for Spotify automation.
"""

import sys
import argparse
import logging

__author__ = 'cmayes'

import spotipy

from spotcrates.playlists import Playlists

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

COMMANDS = ['daily']

COMMAND_DESCRIPTION = f"""
{'COMMAND NAME':<16} DESCRIPTION
{'daily':<16} Add "Daily Mix" entries to the end of the target playlist, filtering for excluded entries.
"""

def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)

def print_commands():
    """Prints available commands."""
    print(COMMAND_DESCRIPTION)

def get_spotify_handle():
    cache_handler = spotipy.cache_handler.CacheFileHandler()
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler, scope=["playlist-modify-private",
                                                                                   "playlist-read-private"])
    return spotipy.Spotify(auth_manager=auth_manager)


def append_daily_mix():
    sp = get_spotify_handle()

    playlists = Playlists(sp)
    playlists.append_daily_mix()


def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = argparse.ArgumentParser()
    # parser.add_argument("-i", "--input_rates", help="The location of the input rates file",
    #                     default=DEF_IRATE_FILE, type=read_input_rates)
    parser.add_argument("command", metavar='COMMAND',
                        help=f"The command to run (one of {','.join(COMMANDS)})")
    args = None
    try:
        args = parser.parse_args(argv)
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, 2

    return args, 0


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != 0:
        return ret

    command = args.command.lower()

    if command == 'daily':
        append_daily_mix()
    elif command == 'commands':
        print_commands()
    else:
        print(f"Invalid command '{args.command}'.  Valid commands: {','.join(COMMANDS)}")
        return 1

    return 0  # success


if __name__ == '__main__':
    status = main()
    sys.exit(status)
