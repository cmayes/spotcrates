from appdirs import user_config_dir, user_cache_dir, user_data_dir, user_state_dir
import sqlite3
from sqlite3 import Error

print(f"Cache dir: ${user_cache_dir('spotcrates')}")
print(f"Config dir: ${user_config_dir('spotcrates')}")
print(f"Data dir: ${user_data_dir('spotcrates')}")
print(f"State dir: ${user_state_dir('spotcrates')}")


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(r"/home/cmayes/.local/share/spotcrates/spotcrates.db")
