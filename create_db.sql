-- ENTITIES

CREATE TABLE USERS (
    login TEXT,
    name TEXT,
    company TEXT,
    location TEXT,
    scanned BOOLEAN,
    PRIMARY KEY (login)
);

CREATE TABLE ORGS (
    login TEXT,
    name TEXT,
    location TEXT,
    PRIMARY KEY (login)
);

CREATE TABLE REPOS (
    owner TEXT,
    name TEXT,
    FOREIGN KEY(owner) REFERENCES USERS(login),
    PRIMARY KEY (owner, name)
);

-- RELATIONSHIPS

CREATE TABLE FOLLOW (
    follower TEXT,
    followee TEXT,
    FOREIGN KEY(follower) REFERENCES USERS(login),
    FOREIGN KEY(followee) REFERENCES USERS(login),
    PRIMARY KEY (follower, followee)
);

CREATE TABLE STAR (
    user TEXT,
    repo_owner TEXT,
    repo_name TEXT,
    FOREIGN KEY(user) REFERENCES USERS(login),
    FOREIGN KEY(repo_owner, repo_name) REFERENCES REPOS(owner, name),
    PRIMARY KEY (user, repo_owner, repo_name)
);

CREATE TABLE MEMBER (
    user TEXT,
    org TEXT,
    FOREIGN KEY(user) REFERENCES USERS(login),
    FOREIGN KEY(org) REFERENCES ORGS(login),
    PRIMARY KEY (user, org)
);
