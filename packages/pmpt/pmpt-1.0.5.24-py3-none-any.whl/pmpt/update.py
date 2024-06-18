import requests
from moyanlib import jsons
from tqdm import tqdm
import dill
import os
from .util import dirs, console

packageNum = 0


def getSourceID(url):
    """
    获取源id
    """
    return url["id"]  # 取前八位


class Index:
    def __init__(self, indexurl):
        self.packageList = {}
        self.IndexURL = indexurl["url"]
        self.number = 0
        self.priority = indexurl["priority"]

    def addPackage(self, name):
        self.packageList[name] = "1"
        self.number += 1


def getIndex(url):
    global packageNum
    try:
        req = requests.get(url["url"])  # 请求HTML
    except Exception:
        console.print("[red]Unable to connect to source[/red]")
        return False
    HTMLIndex = req.text

    ClassIndex = Index(url)

    console.print("🔍 Parsing HTML index...")
    for line in tqdm(HTMLIndex.split("\n")):
        # 提取并筛选标签
        line_list = line.split(">")
        if len(line_list) > 1 and "<a " in line:
            package_name = line_list[1].split("<")[0]

            ClassIndex.addPackage(package_name)  # 添加包

    console.print("Total number of packages:", str(ClassIndex.number))
    packageNum += ClassIndex.number
    console.print('📚 Saving index..."')
    dill.dump(
        ClassIndex, open(f"{dirs.user_data_dir}/Index/{getSourceID(url)}.pidx", "wb")
    )
    return True


def getAllIndex():
    """
    SourceList = [
        'https://pypi.tuna.tsinghua.edu.cn/simple',
        'https://mirrors.bfsu.edu.cn/pypi/web/simple/'
    ]
    """
    SourceList = jsons.load(
        open(os.path.join(dirs.user_config_dir, "Source.json"))
    )  # 加载源列表
    if len(SourceList) < 1:
        console.print("❌ [red]You have not configured any sources.[/red]")
        exit(1)

    for source in SourceList:  # 遍历源列表
        console.print("📚 Downloading index from", source["url"] + "...")
        sta = getIndex(source)
        if sta:
            console.print("✅ [green]Index downloaded successfully![/green]")
        else:
            console.print("❌ [red]Index download failed.[/red]")
    # print(packageNum)
