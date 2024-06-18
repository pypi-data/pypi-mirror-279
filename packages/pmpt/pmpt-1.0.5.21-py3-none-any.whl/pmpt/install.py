from . import util
import requests
from rich.table import Table
from urllib import parse


def search(name):
    for Index in util.loadIndex():
        dt = Index.packageList.get(name, None)
        if dt:
            try:
                rurl = parse.urljoin(Index.IndexURL, name)
                r = requests.get(rurl)
            except:
                continue
            else:
                if r.status_code != 200:
                    continue
            return Index.IndexURL


def main(
    packlist, upgrade, reads, force_reinstall, ignore_requires_python, yes, command
):
    console = util.console
    if reads:  # 从文件读取列表
        f = open(packlist[0])
        packlist = f.read().split("\n")

    packsInfo = {}
    with console.status("🚀🔍 Searching for package information...") as status:
        # 创建表格
        table = Table(show_header=True, header_style="bold")
        table.add_column("Package Name", width=20, style="bold")
        table.add_column("Package Source", width=20, style="green")

        for rawpack in packlist:  # 解析指定了版本的包名
            if "==" in rawpack:
                pack = rawpack.split("==")[0]
            elif ">=" in rawpack:
                pack = rawpack.split(">=")[0]
            elif "<=" in rawpack:
                pack = rawpack.split("<=")[0]
            elif "<" in rawpack:
                pack = rawpack.split("<")[0]
            elif ">" in rawpack:
                pack = rawpack.split(">")[0]
            else:
                pack = rawpack

            result = search(pack.lower())  # 转小写并获取源地址
            packsInfo[pack] = [result, rawpack]

    canInstallPack = []
    for k, v in packsInfo.items():
        if not v[0]:
            table.add_row(k, "[red]Not found[red]")
        else:
            table.add_row(k, v[0])
            canInstallPack.append(k)
    console.print(table)

    if len(canInstallPack) < 1:
        console.print("❌ [red]There are no packages available for installation.[red]")
        exit(1)

    console.print("📦 Packages to be installed:")
    console.print(" ".join(canInstallPack))

    while True:  # 是否允许安装
        if yes:
            break

        ye = console.input("Proceed with installation? [Y/n]: ")

        if ye.lower() == "y":
            break
        elif ye.lower() == "n":
            console.print("🛑 [red]User canceled the installation.[/red]")
            exit(1)
        else:
            continue

    console.print("🛠️ Initiating pip installation...")
    for pack in canInstallPack:

        # 构建命
        args = ["-i", packsInfo[pack][0]]  # 指定源

        if upgrade:  # 升级
            args.append("-U")
        if force_reinstall:  # 强制重新安装
            args.append("--force-reinstall")
        if ignore_requires_python:  # 忽略Python版本
            args.append("--ignore-requires-python")

        args.append(packsInfo[pack][1])
        with console.status("🚀 [green]Installing...[/green]") as status:
            ret = util.runpip("install", args, command)  # 运行pip

        if ret.returncode != 0:  # 是否执行完毕
            console.print("❌ [red]Installation failed.[/red]")
            exit(1)
        console.print(f"✅ [green]Installation successful for {pack}[/green]")
