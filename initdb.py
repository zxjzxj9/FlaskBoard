
#/usr/bin/env python

# This script is aimed at create a database for forum systems
# written by zxj

import psycopg2 as pg2
import sys

print "Warning! All data will be erased in database!"
print "continue (y/n)?"

if not raw_input().strip()=="y":
    sys.exit()

# Connect the forum database 
db = pg2.connect(dbname = "forum")
c = db.cursor()


c.execute("SELECT * FROM pg_catalog.pg_tables WHERE tablename = %s;", ("users",))

if c.fetchone():
    print "Table user exists, drop this table..."
    c.execute("DROP TABLE users;")

print "Create table users..."

c.execute('''CREATE TABLE users(
                      uid serial primary key,
                      name varchar(255),
                      nickname varchar(255),
                      salt varchar(255),
                      password varchar(255),
                      email varchar(255),
                      verilink varchar(255),
                      avatar varchar(255),
                      verified boolean,
                      priv integer,
                      last_login timestamptz,
                      sessionid varchar(255),
                      expireat timestamptz
                      );
          ''')

print "Table create success..."

#################

c.execute("SELECT * FROM pg_catalog.pg_tables WHERE tablename = %s;", ("topics",))

if c.fetchone():
    print "Table topics exists, drop this table..."
    c.execute("DROP TABLE topics;")

print "Create table topics..."
c.execute('''CREATE TABLE topics(
                tid serial primary key,
                name varchar(255),
                admin integer,
                color varchar(7),
                last_post integer
                );
          ''')

print "Table create success..."
###############

c.execute("SELECT * FROM pg_catalog.pg_tables WHERE tablename = %s;", ("posts",))

if c.fetchone():
    print "Table posts exists, drop this table..."
    c.execute("DROP TABLE posts;")

print "Create table posts..."
c.execute('''CREATE TABLE posts(
                tid serial primary key,
                title varchar(255),
                content varchar,
                color varchar(7),
                author integer,
                last_modified timestamptz
                );
          ''')

print "Table create success..."

############

c.execute("SELECT * FROM pg_catalog.pg_tables WHERE tablename = %s;", ("follows",))
if c.fetchone():
    print "Table follows exists, drop this table..."
    c.execute("DROP TABLE follows;")

print "Create table follows..."
c.execute('''CREATE TABLE follows(
              tid serial primary key,
              content varchar,
              author integer,
              last_modified timestamptz
              );
          ''')
print "Table create success..."

db.commit()
c.close()
db.close()
