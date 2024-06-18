from flask import Flask, render_template, jsonify, redirect
from . import util
import os
from flask_caching import Cache

current_dir = os.path.dirname(__file__)

app = Flask(
    __file__,
    template_folder=os.path.join(current_dir, "data"),
    static_folder=os.path.join(current_dir, "data", "statics"),
)

config = {  # some Flask specific configs
    "CACHE_TYPE": "FileSystemCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 600,
    "CACHE_DIR": util.dirs.user_cache_dir,
}
app.config.from_mapping(config)
cache = Cache(app)


def run():
    app.run(port=14536)


@app.route("/")
@cache.cached(timeout=36000)
def index():
    return render_template("index.html")


@app.route("/package/<name>")
def package(name):
    return redirect("https://pypi.org/project/" + name)


@app.route("/api/list")
@cache.cached(timeout=600)
def api_list():
    listv = util.runpip("freeze", out=False)
    outlist = []
    for line in iter(listv.stdout.readline, b""):

        line = line.decode("utf-8").strip()  # 将字节转换为字符串并去除换行符
        if "==" not in line or line[0] == "#":
            continue
        lineList = line.split("==")
        lineDict = {"name": lineList[0], "ver": lineList[1]}
        outlist.append(lineDict)
    return jsonify(outlist)
