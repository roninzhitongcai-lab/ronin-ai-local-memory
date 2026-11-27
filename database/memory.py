"""Build or read Ronin's SQLite index using only the Python standard library."""
import argparse
import os
import sqlite3
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "ronin.sqlite3"
ROOT_DOCS = ("USER.md", "SOUL.md", "AGENTS.md")
FOLDERS = ("projects", "tasks", "knowledge")


def build():
    paths = [ROOT / name for name in ROOT_DOCS]
    for folder in FOLDERS:
        paths.extend(sorted((ROOT / folder).glob("*.md")))
    with tempfile.TemporaryDirectory(dir=DB.parent) as temp:
        candidate = Path(temp) / DB.name
        conn = sqlite3.connect(candidate)
        try:
            with conn:
                conn.execute("CREATE TABLE documents(path TEXT PRIMARY KEY, body TEXT NOT NULL)")
                conn.executemany(
                    "INSERT INTO documents VALUES (?, ?)",
                    ((p.relative_to(ROOT).as_posix(), p.read_text(encoding="utf-8")) for p in paths),
                )
            if conn.execute("PRAGMA integrity_check").fetchone() != ("ok",):
                raise RuntimeError("数据库完整性检查失败")
        finally:
            conn.close()
        os.replace(candidate, DB)


def main():
    parser = argparse.ArgumentParser(description="Ronin 个人记忆库")
    parser.add_argument("--owner", required=True, choices=["ronin"])
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("build")
    sub.add_parser("list")
    sub.add_parser("read").add_argument("path")
    args = parser.parse_args()
    if args.action == "build":
        build()
        return
    conn = sqlite3.connect(DB.as_uri() + "?mode=ro", uri=True)
    try:
        if args.action == "list":
            for (path,) in conn.execute("SELECT path FROM documents ORDER BY path"):
                print(path)
        else:
            row = conn.execute("SELECT body FROM documents WHERE path = ?", (args.path,)).fetchone()
            if row is None:
                parser.exit(1, "未找到该文件\n")
            print(row[0], end="")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
