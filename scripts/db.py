
import os
import psycopg2
from psycopg2 import sql
import argparse


def create_schema(conn, schema_name):
    """
    Create schema in db specified by the conn Connection object
    """
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(
            sql.SQL(
                "CREATE SCHEMA {0};",
            ).format(
                sql.Identifier(schema_name),
            )
        )


def create_user(conn, user, password):
    """
    Alter db user if it exists
    Create a new db user if it does not exist
    """
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(
            sql.SQL(
                """
                DO $$
                BEGIN
                  IF NOT EXISTS (
                    SELECT 1
                    FROM pg_roles
                    WHERE rolname = {user_literal}
                  ) THEN
                    CREATE USER {user} WITH
                    CONNECTION LIMIT 1000
                    LOGIN ENCRYPTED PASSWORD {password};
                  ELSE
                    ALTER USER {user} WITH
                    ENCRYPTED PASSWORD {password};
                  END IF;
                END
                $$;
                """
            ).format(
                user_literal=sql.Literal(user),
                user=sql.Identifier(user),
                password=sql.Literal(password)
            )
        )


def drop_db(conn, db_name):
    """
    Force drop a database if it exists
    """
    print(f"Dropping database {db_name} if it exists ...")
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(
            sql.SQL(
                "DROP DATABASE IF EXISTS {} WITH (FORCE);"
            ).format(sql.Identifier(db_name))
        )


def create_db(conn, db_name):
    """
    Create a databasee
    """
    print(f"Creating database {db_name} ...")
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(
            sql.SQL(
                "CREATE DATABASE {};"
            ).format(sql.Identifier(db_name))
        )
