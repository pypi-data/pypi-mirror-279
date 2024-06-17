from pyqqq.executors.hook import HookExecutor
from qupiato.cli.utils import create_and_upload_to_gcs_bucket, get_token, ws_api_call, get_version, get_agent, encode_secret, search_strategies, get_user, pull_strategy, publish_strategy
import asyncio
import click
import datetime as dtm
import importlib
import os
import qupiato.cli.config as c
import re
import subprocess
import sys
import yaml


@click.group()
def main():
    pass


@main.command()
@click.argument('entryfile')
@click.option('--publish', '-p', is_flag=True, help="Publish the strategy to the public repository")
def deploy(entryfile, publish):
    """Deploy strategy

    ENTRYFILE is the file to deploy
    """
    if not os.path.exists(entryfile):
        click.echo(f"File {entryfile} does not exist")
        return

    # if strategy name is not specified, use the filename without extension
    strategy_name = os.path.splitext(os.path.basename(entryfile))[0]

    # replace all uppercase letters with lowercase
    strategy_name = strategy_name.lower()
    # replace all non-alphabets with hyphens
    strategy_name = re.sub(r'[^a-z0-9]', '-', strategy_name)
    # replace underbars with hyphens
    strategy_name = re.sub(r'_', '-', strategy_name)
    # remove leading and trailing hyphens
    strategy_name = strategy_name.strip('-')

    if not re.match(f'[a-z0-9-]', strategy_name):
        click.echo("Invalid strategy name")
        return

    click.echo(f"Deploying {entryfile} as {strategy_name}")

    asyncio.run(deploy_strategy(entryfile, strategy_name, publish))


async def deploy_strategy(entryfile, strategy_name, publish):
    click.echo(f"Uploading {entryfile} to GCS bucket")
    secret = encode_secret()
    zipfile = create_and_upload_to_gcs_bucket()

    req = {
        "action": "deploy",
        "strategy_name": strategy_name,
        "token": get_token(),
        "zipfile": zipfile,
        "entryfile": entryfile,
        "agent": {
            **get_agent()
        },
        "secret": secret,
        "publish": publish
    }

    async for line in ws_api_call(req):
        if 'text' in line:
            click.echo(line['text'])

    if publish:
        try:
            publish_strategy(entryfile, strategy_name, zipfile)
            click.echo(f"Publishing {entryfile} as {strategy_name} to public repository")
        except Exception as e:
            click.echo(e)

@main.command()
def list():
    """ List deployed strategies """

    asyncio.run(list_strategies())


async def list_strategies():
    req = {
        "action": "list",
        "token": get_token(),
    }

    async for r in ws_api_call(req):
        if 'data' not in r:
            continue

        if len(r['data']) == 0:
            click.echo("No strategies deployed")
            return

        data = r['data']

        name_width = __calc_column_width(data, 'name', "DEPLOYMENT ID")
        strategy_width = __calc_column_width(data, 'strategy_name', "STRATEGY NAME")
        status_width = __calc_column_width(data, 'status', "STATUS")

        click.echo(f"{'DEPLOYMENT ID':<{name_width}} {'STRATEGY NAME':<{strategy_width}} {'STATUS':<{status_width}} CREATED AT")

        for e in data:
            created_at = dtm.datetime.fromtimestamp(e['created_at']/1000).strftime('%Y-%m-%d %H:%M:%S')
            click.echo(f"{e['name']:<{name_width}} {e['strategy_name']:<{strategy_width}} {e['status']:<{status_width}} {created_at}")


def __calc_column_width(arr, key, title, margin=2):
    max_len = max(len(x[key]) for x in arr)
    max_len = max(max_len, len(title))
    return max_len + margin


@main.command()
@click.argument('deployment_id')
def delete(deployment_id):
    """ Delete a deployed strategy """

    asyncio.run(delete_strategy(deployment_id))


async def delete_strategy(deployment_id):
    req = {
        "action": "delete",
        "deployment_id": deployment_id,
        "token": get_token(),
        "agent": {
            **get_agent()
        }
    }

    async for line in ws_api_call(req):
        if 'text' in line:
            click.echo(line['text'])


@main.command()
@click.argument('deployment_id')
@click.option('--follow', '-f', is_flag=True, help="Specify to stream the logs")
@click.option('--lines', '-n', default=None, help="Number of lines to show")
def logs(deployment_id, follow, lines):
    """ Show logs of a deployed strategy """

    asyncio.run(show_logs(deployment_id, follow, lines))


async def show_logs(deployment_id, follow, lines):
    req = {
        "action": "logs",
        "deployment_id": deployment_id,
        "token": get_token(),
        "follow": follow,
    }

    if lines is not None:
        try:
            req['lines'] = int(lines)
        except ValueError:
            click.echo("Invalid value for --lines")
            return

    fetching = True
    while fetching:
        async for line in ws_api_call(req):
            if 'text' in line:
                print(line['text'], end='')

        if req['follow']:
            req['lines'] = 0
            await asyncio.sleep(0.01)
        else:
            fetching = False

@main.command()
def version():
    """ Show version number and quit """
    version = get_version()
    click.echo(f"v{version}")


@main.command()
@click.argument('filename')
def run(filename):
    """ Run a strategy """

    if not os.path.exists(filename):
        click.echo(f"File {filename} does not exist")
        sys.exit(1)

    if os.path.exists("requirements.txt"):
        subprocess.run(["pip", "install", "-r", "requirements.txt"])

    app = None
    if os.path.exists("app.yaml"):
        with open("app.yaml", "r") as f:
            app = yaml.safe_load(f)

    spec = importlib.util.spec_from_file_location(os.getcwd(), filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    loop = asyncio.get_event_loop()

    if app is not None and app.get("executor") == "hook":
        task = loop.create_task(maybe_awaitable(HookExecutor(module).run()))
    else:
        if not has_callable(module, "run"):
            click.echo("Module does not have a callable run()")
            sys.exit(1)

        task = loop.create_task(maybe_awaitable(module.run()))

    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        click.echo(f"Got keyboard interrupt, cancelling tasks...")
        task.cancel()
        loop.run_until_complete(task)
    finally:
        loop.close()


async def maybe_awaitable(result):
    if asyncio.iscoroutine(result) or isinstance(result, asyncio.Future):
        return await result
    else:
        return result


def has_callable(module, name):
    try:
        return callable(getattr(module, name))
    except AttributeError:
        return False


@main.command()
@click.argument('term', required=False)
@click.option('--email', '-e', default=None, help="Specify email to search for")
def search(term, email):
    """ Search for stock investment strategies """
    params = {
        "term": term
    }
    if email is not None:
        params['email'] = email

    r = search_strategies(params)

    if r is None or 'data' not in r or len(r['data']) == 0:
        if email is not None:
            click.echo(f"Strategies not found for {email}/{term}")
        else:
            click.echo(f"Strategies not found for {term}")
        sys.exit(1)

    data = r['data']

    __format_strategies(data)


@main.command()
@click.argument('name')
def pull(name):
    """ Download an strategy from the registry """
    [email, strategy_name] = name.split('/')

    params = {
        'term': strategy_name,
        'email': email
    }
    r = search_strategies(params)

    if r is None or 'data' not in r or len(r['data']) == 0:
        click.echo("Strategy does not exists or not accessible")
        sys.exit(1)
    elif len(r['data']) > 1:
        click.echo("Strategy is ambiguous, please specify the name")
        __format_strategies(r['data'])
        sys.exit(1)

    file_name = r['data'][0]['zipfile']
    pull_strategy(strategy_name, file_name)

    click.echo(f"{name}'s download has completed")


def __format_strategies(data):
    display = []
    for e in data:
        display.append({
            'name': f"{e['email']}/{e['strategy_name']}",
            'user': e['uid'],
            'star': str(e['extra_info']['star'])
        })

    name_width = __calc_column_width(display, 'name', "NAME")
    user_width = __calc_column_width(display, 'user', "USER")
    star_width = __calc_column_width(display, 'star', "STAR")

    click.echo(f"{'NAME':<{name_width}} {'USER':<{user_width}} {'STAR':<{star_width}}")

    for e in display:
        click.echo(f"{e['name']:<{name_width}} {e['user']:<{user_width}} {e['star']:<{star_width}}")


if __name__ == '__main__':
    main()
