# pylint:disable=W0611
import datetime
import webbrowser
import time
import os
import sys
import click
from moyanlib import jsons
from rich.table import Table
from . import update as updates
from . import util
from . import source as sou
from . import environment as environ
from . import install as installs
from . import search as searchs
from . import web as webs


@click.group()
def cli():
    today = datetime.datetime.today()
    if today.month == 9 and today.day == 28:
        webbrowser.open("https://ys.mihoyo.com/")
        util.console.print("[green]Genshin！activate！[/green]")
        time.sleep(0.7)
        util.console.print("[green]You all must download Genshin Impact.[/green]")
        time.sleep(0.7)
        util.console.print("Then don't use PMPT.", style="green")

    try:
        import pip
    except ImportError:
        util.logger.critical("没有pip")
        util.console.print("❌ [red]pip module not found![/red]")
        exit(1)


@cli.command(short_help="Update Package Index")
def update():
    # 调用更新函数
    updates.getAllIndex()


@cli.command(short_help="Install Python package")
@click.argument("packlist", nargs=-1, required=True)
@click.option("--upgrade", "-U", is_flag=True, default=False)
@click.option("--reads", "-r", is_flag=True, default=False)
@click.option("--force-reinstall", "-fr", is_flag=True, default=False)
@click.option("--ignore-requires-python", "-irp", is_flag=True, default=False)
@click.option("--yes", "-y", is_flag=True, default=False)
@click.option("--command", "-c", is_flag=True, default=False)
def install(*args, **kwargs):
    installs.main(*args, **kwargs)


@cli.command(name="list", short_help="List all Python packages")
def listp():
    table = Table(show_header=True)
    table.add_column("Name")
    table.add_column("Version")
    listv = util.runpip("freeze", out=False)
    for line in iter(listv.stdout.readline, b""):

        # 在这里你可以对每一行输出进行处理
        line = line.decode("utf-8").strip()  # 将字节转换为字符串并去除换行符
        if "==" not in line or line[0] == "#":
            continue
        lineList = line.split("==")
        table.add_row(lineList[0], lineList[1])
    util.console.print(table)


@cli.command()
@click.argument("name")
@click.option("--yes", "-y", is_flag=True, default=False)
def remove(name, yes):
    args = []
    if yes:
        args.append("-y")
    args.append(name)
    util.runpip("uninstall", args)


@cli.command()
@click.argument("name")
@click.option("--allinfo", "-a", is_flag=True, default=False)
@click.option("--api-url", "-u", default=None)
def search(*args, **kwargs):
    searchs.main(*args, **kwargs)


@cli.group()
def source():
    pass


@source.command()
@click.argument("url")
@click.option("--priority", "-p", default=1, type=int)
def add(*args, **kwargs):
    sou.add(*args, **kwargs)


@source.command(name="list")
def lists():
    sou.lists()


@source.command(name="remove")
@click.argument("ids", default=None, required=False)
@click.option("-y", "--yes", is_flag=True, default=False)
def removes(*args, **kwargs):
    sou.remove(*args, **kwargs)


@source.command(name="modify")
@click.argument("ids")
@click.argument("key")
@click.argument("val")
def modifys(*args, **kwargs):
    sou.modify(*args, **kwargs)


@cli.command()
def version():
    environ.main()


@cli.command()
def web():
    webs.run()


if __name__ == "__main__":
    cli()
