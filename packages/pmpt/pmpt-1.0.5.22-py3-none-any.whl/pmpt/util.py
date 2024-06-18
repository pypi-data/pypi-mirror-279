# pylint:disable=W0622
import os
from subprocess import Popen
import sys
import dill
from rich.console import Console
from loguru import logger
import subprocess
from moyanlib import jsons
import time
import datetime
from platformdirs import PlatformDirs

dirs = PlatformDirs("PMPT", "MoYan")
IndexList = []
console = Console()


def getVer(baseVar):
    if os.environ.get('GITHUB_ACTIONS', None):
        baseVar = (
            baseVar + '.' + os.environ.get('GITHUB_RUN_NUMBER')
        )  
    logger.info("PMPT " + baseVar)
    return baseVar


logger.remove()
logger.add(
    os.path.join(dirs.user_data_dir, "log.log"),
    level="TRACE",
)

__version__ = getVer("1.0.5")


def init():

    os.makedirs(dirs.user_data_dir, exist_ok=True)
    os.makedirs(os.path.join(dirs.user_data_dir, "Index"), exist_ok=True)
    os.makedirs(dirs.user_config_dir, exist_ok=True)
    os.makedirs(dirs.user_cache_dir, exist_ok=True)
    if not os.path.exists(os.path.join(dirs.user_config_dir, "Source.json")):
        open(os.path.join(dirs.user_config_dir, "Source.json"), "w").write("[]")
        from . import source

        source.add('https://pypi.org/simple',1)

    if not os.path.exists(os.path.join(dirs.user_config_dir, "api.url")):
        open(os.path.join(dirs.user_config_dir, "api.url"), "w").write(
            "https://pypi.org/pypi/{}/json"
        )


def bubbleSort(arr):
    for i in range(1, len(arr)):
        for j in range(0, len(arr) - i):
            if arr[j]["priority"] < arr[j + 1]["priority"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def loadIndex():
    """
    加载索引
    """
    today = datetime.datetime.today()
    if today.month == 4 and today.day == 1:
        console.print(
            "😱😱😱 [red]Oh no, your indexes have all been eaten by a python snake.[/red]"
        )
        time.sleep(2.3)
        console.print(
            "😄 [green]But after our life-and-death struggle, I managed to retrieve all of your indexes.[/green]"
        )
    sourceList = jsons.load(open(os.path.join(dirs.user_config_dir, "Source.json")))
    sourceList = bubbleSort(sourceList)
    for source in sourceList:
        if not os.path.exists(
            os.path.join(dirs.user_data_dir, "Index", source["id"] + ".pidx")
        ):
            logger.warning(source["url"] + "没有索引")
            console.print(
                f'⚠️ [yellow]{source["url"]} did not create an index.[/yellow]'
            )
            continue
        logger.debug(source)
        IndexFile = dill.load(
            open(
                os.path.join(dirs.user_data_dir, "Index", source["id"] + ".pidx"), "rb"
            )
        )  # 加载索引
        yield IndexFile


def runpip(command, other=None, dbg=False, out=True) -> Popen:
    """
    运行pip
    """
    logger.trace("调用runpip")
    if not other:
        other = []
    baseCommand = [sys.executable, "-m", "pip"]
    baseCommand.append(command)

    Command = baseCommand + other
    if dbg:
        console.print("Command to be run:", " ".join(Command))
    logger.debug(
        " ",
    )
    runClass = Popen(Command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if out:
        for line in iter(runClass.stdout.readline, b""):
            # 在这里你可以对每一行输出进行处理
            line = line.decode("utf-8").strip()  # 将字节转换为字符串并去除换行符
            console.print(line)
        if runClass.returncode != 0:
            console.print(runClass.stderr.read().decode())
        runClass.communicate()
    else:
        runClass.wait()
    return runClass
