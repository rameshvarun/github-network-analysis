#!/usr/bin/env python3

import os
import sqlite3

from github import Github


def insert_named_user(conn, gh_user):
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO USERS VALUES (?, ?, ?, ?, ?)",
        (gh_user.login, gh_user.name, gh_user.company, gh_user.location, False),
    )
    conn.commit()


def insert_follow(conn, follower, followee):
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO FOLLOW VALUES (?, ?)", (follower.login, followee.login)
    )
    conn.commit()


def insert_star(conn, user, repo):
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO STAR VALUES (?, ?, ?)",
        (user.login, repo.owner.login, repo.name),
    )
    conn.commit()


def insert_repo(conn, repo):
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO REPOS VALUES (?, ?)", (repo.owner.login, repo.name)
    )
    conn.commit()


def mark_as_scanned(conn, gh_user):
    c = conn.cursor()
    c.execute("UPDATE USERS SET scanned = TRUE WHERE login = ?", gh_user.login)
    conn.commit()


if __name__ == "__main__":
    gh = Github(os.environ["GITHUB_OAUTH_TOKEN"])

    initialize = not os.path.isfile("data.db")
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    if initialize:
        for command in open("create_db.sql").read().split(";"):
            c.execute(command)
        conn.commit()

        insert_named_user(conn, gh.get_user("rameshvarun"))

    while True:
        unscanned = [
            row[0]
            for row in c.execute("SELECT login FROM USERS WHERE scanned = 0").fetchall()
        ]

        for user in unscanned:
            gh_user = gh.get_user(user)

            for follower in gh_user.get_followers():
                insert_named_user(conn, follower)
                insert_follow(conn, follower, gh_user)

            for followee in gh_user.get_following():
                insert_named_user(conn, followee)
                insert_follow(conn, gh_user, followee)

            for repo in gh_user.get_repos():
                insert_repo(conn, repo)

            for repo in gh_user.get_starred():
                insert_named_user(conn, repo.owner)
                insert_repo(conn, repo)
                insert_star(conn, gh_user, repo)

            mark_as_scanned(conn, gh_user)
            sys.exit()
