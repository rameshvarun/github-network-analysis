#!/usr/bin/env python3

import os
import sqlite3
import requests_cache

from github import Github


def insert_user(conn, user):
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO USERS VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            user.login,
            user.name,
            user.company,
            user.location,
            user.followers,
            user.type,
            False,
        ),
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


def insert_member(conn, user, org):
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO MEMBER VALUES (?, ?)", (user.login, org.login))
    conn.commit()


def mark_as_scanned(conn, gh_user):
    c = conn.cursor()
    c.execute("UPDATE USERS SET scanned = 1 WHERE login = ?", (gh_user.login,))
    conn.commit()


def get_unscanned_users(conn):
    return [
        row[0]
        for row in c.execute(
            """SELECT login FROM USERS
               WHERE scanned = 0 AND type = 'User'
               ORDER BY followers DESC
               LIMIT 5"""
        ).fetchall()
    ]


if __name__ == "__main__":
    requests_cache.install_cache("requests-cache", expire_after=5 * 60)
    gh = Github(os.environ["GITHUB_OAUTH_TOKEN"])

    initialize = not os.path.isfile("data.db")
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    if initialize:
        for command in open("create_db.sql").read().split(";"):
            c.execute(command)
        conn.commit()

        insert_user(conn, gh.get_user("nat"))

    while True:
        for user in get_unscanned_users(conn):
            print(f"Scanning user {user}...")
            gh_user = gh.get_user(user)

            print("> Organizations...")
            for org in gh_user.get_orgs():
                insert_user(conn, org)
                insert_member(conn, gh_user, org)

            print("> Followers...")
            for follower in gh_user.get_followers():
                insert_user(conn, follower)
                insert_follow(conn, follower, gh_user)

            print("> Following...")
            for followee in gh_user.get_following():
                insert_user(conn, followee)
                insert_follow(conn, gh_user, followee)

            print("> Repos...")
            for repo in gh_user.get_repos():
                insert_repo(conn, repo)

            print("> Stars...")
            for repo in gh_user.get_starred():
                insert_user(conn, repo.owner)
                insert_repo(conn, repo)
                insert_star(conn, gh_user, repo)

            mark_as_scanned(conn, gh_user)
            requests_cache.core.remove_expired_responses()
