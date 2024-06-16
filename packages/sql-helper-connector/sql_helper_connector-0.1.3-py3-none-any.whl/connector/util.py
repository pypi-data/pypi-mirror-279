import pg8000
import pymysql
import json
from datetime import datetime, date
import os
import click


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')  # You can adjust the format as needed
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')  # You can adjust the format as needed
        return json.JSONEncoder.default(self, obj)


def get_conn(db_host, db_name, db_user, db_password, db_port):
    # try to connect database
    conn = None
    try:
        conn = pg8000.connect(host=db_host, database=db_name, user=db_user, password=db_password,
                              port=db_port)
        return conn
    except Exception as e:
        click.echo(f"postgres server connection error {str(e)}")
        click.echo("try connect mysql server")
        try:
            conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name, port=db_port)
            return conn
        except Exception:
            click.echo(f"mysql connection error {str(e)}")
    return conn
