import sys
from app import fetch_shoutcast, init_db

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python -m app.shoutcast <url>')
        sys.exit(1)
    init_db()
    if fetch_shoutcast(sys.argv[1]):
        print('Play stored')
    else:
        print('Failed to fetch')
