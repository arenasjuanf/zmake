import shutil
import subprocess
from pathlib import Path

import converter


def is_project(path: Path):
    return (path / "app.json").is_file()


def mk_assets(path: Path):
    print("-- Process assets...")
    source = path / "assets"
    dest = path / "build" / "assets"

    dest.mkdir()
    to_convert = []
    for item in source.rglob("**/*"):
        delta = str(item)[len(str(source)) + 1:]
        target = dest / delta
        if item.is_dir():
            target.mkdir()
        elif item.name.endswith(".png"):
            to_convert.append((item, target))
        else:
            print(f"Copy RAW file: {delta}")
            shutil.copy(item, target)

    converter.to_tga(to_convert)


def mk_js_content(path: Path):
    print("-- Prepare JS base")

    out = ''
    for directory in [path / 'lib', path / 'src']:
        if not directory.is_dir():
            return

        for file in directory.rglob("**/*.js"):
            out += f"// source: {file}\n"
            with file.open("r") as f:
                out += f.read() + "\n"

    return out


def mk_run_uglify(content: str, params: str):
    print("Run uglifyjs...")
    command = ["uglifyjs"]
    if params != "":
        command.extend(params.split(" "))
    uglify = subprocess.run(command,
                            input=content.encode("utf8"),
                            stdout=subprocess.PIPE)
    assert uglify.returncode == 0
    return uglify.stdout.decode("utf8")


def mk_preview(path: Path):
    print("-- Prepare preview")
    subprocess.Popen(["zepp-preview", "-o", path / "dist",
                      "--gif", path / "build"]).wait()

    assert (path / "dist/preview.png").is_file()
    assert (path / "dist/preview.gif").is_file()