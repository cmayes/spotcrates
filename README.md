# Spotcrates
## A set of tools for finding and managing music on Spotify

![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/cmayes/3c8214e2bd942821496440b93acd3582/raw/covbadge.json)

# Installation

(TODO: Add detailed instructions once uploaded to PyPI)

# Commands

The installation script puts the command `spotcrates` in your Python environment
(e.g. `/.pyenv/shims/spotcrates`). The command `spotcrates commands` lists all of the 
commands available along with a short description of each.

Note that Spotcrates will accept the shortest unique command substring, so for example you can run
`spotcrates sub` for the `subscriptions` command.

## daily
`spotcrates daily` collects the contents of the "Daily Mix" playlists, filters them 
against an exclusion list ("Overplayed" by default), and adds them to the end of 
a target list ("Now" by default).

## subscriptions
`spotcrates subscriptions` adds new tracks from configured playlists to the target playlist, 
filtering for excluded entries. Three days is the default maximum age for a track to be 
considered "new."

## list-playlists
`spotcrates list-playlists` lists playlists' name, owner, track count, and description.
The command accepts `-f` for filter expressions and `-s` for sort expressions. (TODO: 
add description of filter and search expressions and link to it here)

### Search Patterns

The command `list-playlists` accepts search filters passed via the `-f` option. Multiple
filter expressions are separated by commas.

#### Search Examples

`spotcrates li -f jazz`

List playlists where any field contains the string "jazz" (case-insensitive)

```
PLAYLIST NAME                    SIZE  ID                       OWNER            DESCRIPTION
Jazz Piano Classics              100   37i9dQZF1DX5q7wCXFrkHh   spotify          The classic piano recordings in Jazz. Cover: Oscar Peterson
Acid Jazz                        90    37i9dQZF1DWXHghfFFOaS6   spotify          Where hip-hop and soul meets jazz. Cover: Digable Planets
Jazz Funk                        6     61Q9DgzF3f1ULr3i1uRyUy   cmayes3          
Acid Jazz                        3     1h6rEPX9qRpBCBbjuAysMz   cmayes3          
General Jazz                     513   1j6ndSnyYn6oUlnwpGiRWc   cmayes3          
Jazz Funk (Instrumental)         272   4xRrCdkn4r5lrDOElek5oC   1226030890       
Instrumental Acid Jazz Mix       50    37i9dQZF1EIgnEnn8SKPjM   spotify          Instrumental Acid Jazz music picked just for you
State of Jazz                    100   37i9dQZF1DX7YCknf2jT6s   spotify          New jazz for open minds. Cover: Walter Smith III
Jazz-Funk                        200   37i9dQZF1DWUb0uBnlJuTi   spotify          Jazz. But funky. Cover: Takuya Kuroda
Jazz                             1     6VH2cw8n115fbQ7Ls2wzdR   cmayes3          
FaLaLaLaLa GREAT BIG Christmas V 4051  6A2Kj9cWUpuu0UcEbWVf5E   kingofjingaling  Over 170 hours of classic Christmas music. The focus is on classic Christma
```

`spotcrates li -f o:spotify,n:rise`

List playlists where the owner contains `spotify` and name contains `rise`.

```
PLAYLIST NAME                    SIZE  ID                       OWNER            DESCRIPTION
Rise                             230   37i9dQZF1DWUOhRIDwDB7M   spotify          Positive and uplifting ambient instrumental tracks.
```

`spotcrates li -f n:ends:villains`

List playlists where name ends with `villains`.

```
PLAYLIST NAME                    SIZE  ID                       OWNER            DESCRIPTION
classical music for villains     66    0zkl7eKzuUit1QRPVKtga2   225uye2hek5id23t 
```

#### Search Fields

The default search field is `all`.

- spotify_id
- playlist_name
- size
- owner
- playlist_description
- all: Search any/all of the above fields.

#### Search Types

The default search type is `contains`.

- contains
- equals
- starts
- ends
- greater
- less
- greater_equal
- less_equal

### Sort Patterns

The command `list-playlists` accepts sort filters passed via the `-s` option. Multiple
sort expressions are separated by commas.

#### Sort Examples

`spotcrates li -f n:jazz -s name`

Name contains `jazz`; sort by name ascending.

```
PLAYLIST NAME                    SIZE  ID                       OWNER            DESCRIPTION
Acid Jazz                        90    37i9dQZF1DWXHghfFFOaS6   spotify          Where hip-hop and soul meets jazz. Cover: Digable Planets
Acid Jazz                        3     1h6rEPX9qRpBCBbjuAysMz   cmayes3          
General Jazz                     513   1j6ndSnyYn6oUlnwpGiRWc   cmayes3          
Instrumental Acid Jazz Mix       50    37i9dQZF1EIgnEnn8SKPjM   spotify          Instrumental Acid Jazz music picked just for you
Jazz                             1     6VH2cw8n115fbQ7Ls2wzdR   cmayes3          
Jazz Funk                        6     61Q9DgzF3f1ULr3i1uRyUy   cmayes3          
Jazz Funk (Instrumental)         272   4xRrCdkn4r5lrDOElek5oC   1226030890       
Jazz Piano Classics              100   37i9dQZF1DX5q7wCXFrkHh   spotify          The classic piano recordings in Jazz. Cover: Oscar Peterson
Jazz-Funk                        200   37i9dQZF1DWUb0uBnlJuTi   spotify          Jazz. But funky. Cover: Takuya Kuroda
State of Jazz                    100   37i9dQZF1DX7YCknf2jT6s   spotify          New jazz for open minds. Cover: Walter Smith III
```

`spotcrates li -f jazz,size:ge:100 -s size:desc`

Any field contains `jazz`; size is greater than or equal to 100, sort by size descending.

```
PLAYLIST NAME                    SIZE  ID                       OWNER            DESCRIPTION
FaLaLaLaLa GREAT BIG Christmas V 4051  6A2Kj9cWUpuu0UcEbWVf5E   kingofjingaling  Over 170 hours of classic Christmas music. The focus is on classic Christma
General Jazz                     513   1j6ndSnyYn6oUlnwpGiRWc   cmayes3          
Jazz Funk (Instrumental)         272   4xRrCdkn4r5lrDOElek5oC   1226030890       
Jazz-Funk                        200   37i9dQZF1DWUb0uBnlJuTi   spotify          Jazz. But funky. Cover: Takuya Kuroda
Jazz Piano Classics              100   37i9dQZF1DX5q7wCXFrkHh   spotify          The classic piano recordings in Jazz. Cover: Oscar Peterson
State of Jazz                    100   37i9dQZF1DX7YCknf2jT6s   spotify          New jazz for open minds. Cover: Walter Smith III
```

#### Sort Types

The default sort type is `ascending`, i.e. a-z.

- ascending
- descending

## randomize
`spotcrates randomize (playlist1) (playlist2)...` randomizes the playlists with the given names, 
IDs, or in the given collections. 

## copy
`spotcrates copy (source) (dest)` copies a playlist into a new playlist. You may optionally specify 
a destination playlist name; the default is to name the destination based on the source name with
the general form `f"{source_name}-{count:02d}"`.

## commands
`spotcrates commands` displays a summary of the available commands.