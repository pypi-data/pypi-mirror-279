import requests
from . import util
from moyanlib import jsons
from .install import search
import os

console = util.console


def main(name, allinfo, api_url):
    if not search(name):
        console.print("❌ [red]The package does not exist[/red]")
        exit()

    if not api_url:
        api_url = open(os.path.join(util.dirs.user_config_dir, "api.url")).read()

    req = requests.get(api_url.format(name))
    if req.status_code == 404:
        console.print(404)
        console.print("❌ [red]The package does not exist[/red]")
        exit()
    elif req.status_code != 200:
        console.print("❌ [red]Server Error![/red]")
        console.print("[red]Error Code: " + str(req.status_code) + "[/red]")
        exit()

    packageInfo = jsons.loads(req.text)
    if not allinfo:
        print("Package Name:", packageInfo["info"]["name"])
        print("Version:", packageInfo["info"]["version"])
        print("Author:", packageInfo["info"]["author"])
        print("Summary:", packageInfo["info"]["summary"])
        print("Keywords:", packageInfo["info"]["keywords"])
        print("License:", packageInfo["info"]["license"])
        if packageInfo["info"]["requires_dist"]:
            print("Dependent Library:", ", ".join(packageInfo["info"]["requires_dist"]))
    elif allinfo:
        for k, v in packageInfo["info"].items():
            print(f"{k}: {v}")
