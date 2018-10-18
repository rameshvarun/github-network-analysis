import os
import sqlite3

if __name__ == "__main__":
    initialize = not os.path.isfile("data.db")
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    if initialize:
        c.execute("""
            CREATE TABLE USERS (username TEXT PRIMARY_KEY, scanned BOOLEAN);
        """)

        c.execute("""
            CREATE TABLE REPO (
                username TEXT,
                reponame TEXT,
                PRIMARY KEY (username, reponame)
            );
        """)

        c.execute("""
            CREATE TABLE FOLLOW (
                follower TEXT,
                followee TEXT,
                FOREIGN KEY(follower) REFERENCES USERS(username),
                FOREIGN KEY(followee) REFERENCES USERS(username),
                PRIMARY KEY (follower, followee)
            );
        """)

        conn.commit()
