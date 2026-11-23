"""Run Alpha Library on the command line.

Example:
    python main.py --db my_library.db
"""
import argparse
from library.database import connect
from library.ui import LibraryCLI


def main():
    parser = argparse.ArgumentParser(description="Alpha Library Management System")
    parser.add_argument("--db", default="alpha_library.db", help="SQLite database path")
    args = parser.parse_args()
    conn = connect(args.db)
    try:
        LibraryCLI(conn).run()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
