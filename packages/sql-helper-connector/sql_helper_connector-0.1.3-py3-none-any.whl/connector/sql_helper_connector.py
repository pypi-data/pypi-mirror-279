import time

import click
import sys
import os
import subprocess
try:
    from .util import get_conn
except Exception:
    from util import get_conn


CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


@click.command()
@click.option('--db-host', default='localhost', help='Database host.')
@click.option('--db-name', help='Database name.')
@click.option('--db-user', help='Database user.')
@click.option('--db-password', help='Database password.')
@click.option('--db-port', default=5432, type=int, help='Database port.')
@click.option('--connection-id', help='Connection unique identifier.')
@click.option('--api-key', help='API key for external service.')
@click.option('--server_url', default='https://api.clustro.ai', help='clustro server url for external service.')
def handle_connection(db_host, db_name, db_user, db_password, db_port, connection_id, api_key, server_url):
    """
    Connect to a database and perform operations using the provided parameters.
    """
    # 在这里实现你的逻辑
    for option in ["db_host", "db_name", "db_user", "db_password", "db_port", "connection_id", "api_key"]:
        if not eval(option):
            click.echo(f'--{option} not provided. Type "--help" for options.')
            return

    click.echo(f"Connecting to database {db_name} at {db_host}:{db_port} with user {db_user}")
    click.echo(f"Clustro AI {connection_id=}, {api_key=}, {server_url=}")
    conn = get_conn(db_host, db_name, db_user, db_password, db_port)
    if not conn:
        click.echo(
            f"try connecting to database {db_host}, {db_name} {db_user} {db_password}, {db_port} fail, please check db info")
        return
    current_directory = CURRENT_DIRECTORY
    command = [
        'python',
        os.path.join(current_directory, 'worker_agent.py'),
        f'--worker_id={connection_id}',
        f'--api_key={api_key}',
        f'--server_url={server_url}',
        f'--db_host={db_host}',
        f'--db_name={db_name}',
        f'--db_user={db_user}',
        f'--db_password={db_password}',
        f'--db_port={db_port}'
    ]
    process = subprocess.Popen(command)
    try:
        while True:
            if process.poll() is not None:
                break
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        # On keyboard interrupt, terminate the subprocess
        process.kill()
    except Exception as e:
        print(f"{str(e)}")
        if process.poll() is None:
            process.kill()



if __name__ == '__main__':
    if len(sys.argv) == 1:
        # 当只有一个参数（即脚本名称）时，显示帮助信息并退出
        click.echo('No options provided. Type "--help" for options.')
    else:
        handle_connection()
