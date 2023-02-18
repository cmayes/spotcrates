# (Unreleased)

# Version 0.4.0

## Updated

- Changed "overplayed" to use a prefix pattern rather than a single list to account for 
    the 10K playlist size limit.

# Version 0.3.1

## Added

- Implicit and explicit `all` filter
  - Filters for any field containing the filter string
  - `all:spotify` looks for "spotify" in any field
    - `spotify` without the `all` qualifier is equivalent
- Added "spotify_id" field to results


# Version 0.3.0

## Added 

- `playlist-list` command
  - `-f` filter option
  - `-s` sort option

# 2022-12-18

## Added

- created common.py for common logic.

- Create a target playlist if it doesn't exist.
