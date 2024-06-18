import subprocess
import re
from . import util
import moyanlib


def get_version(command):
    try:
        # 使用 subprocess 调用系统命令获取版本信息
        output = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True
        )
        # 使用正则表达式提取版本号
        version_match = re.search(r"(\d+\.\d+(\.\d+){0,2})", output)
        if version_match:
            return version_match.group(1)
        else:
            return "[red]False[/red]"
    except subprocess.CalledProcessError:
        return "[red]False[/red]"


def getGCCver():
    # 检查是否能执行 gcc 命令
    return get_version("gcc --version")


def getClangVer():
    # 检查是否能执行 clang 命令
    return get_version("clang --version")


def getMSVCver():
    # 检查是否能执行 cl 命令（MSVC编译器）
    return get_version("cl")


def getRustVer():
    process = subprocess.Popen(
        ["rustc --version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        rustVer = stdout.decode().split(" ")[1]
        return rustVer
    else:
        return "[red]False[/red]"


def getPIPver():
    return get_version("pip -V")


def main():
    info = moyanlib.getInfo()
    printText = f"""[white]PMPT {util.__version__}[/white]
{info['OS']['Name']} {info['OS']['Version']}
Python Version: {info['Python']['Version']}
PIP Version: [green]{getPIPver()}[/green]
GCC Version: [green]{getGCCver()}[/green]
Clang Version: [green]{getClangVer()}[/green]
MSVC Version: [green]{getMSVCver()}[/green]
Rust Version: [green]{getRustVer()}[/green]"""
    util.console.print(printText)
