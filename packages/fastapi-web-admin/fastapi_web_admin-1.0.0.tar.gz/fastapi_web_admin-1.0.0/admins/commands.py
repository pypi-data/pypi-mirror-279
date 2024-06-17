import os.path

import typer
from cookiecutter.main import cookiecutter
from pathlib import Path
from admins.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / 'templates'

app = typer.Typer(
    add_completion=False,
    name="FastAPI-Admin",
    help="FastAPI-Admin 构建FastAPI工程的脚手架工具",
)


@app.command(help="构建FastAPI工程", name="startproject")
def start_project(project_name: str):
    typer.echo(f"开始构建项目：{project_name}............")

    try:
        cookiecutter(
            os.path.join(TEMPLATES_DIR, 'project'),
            extra_context={'project_name': project_name, 'secret_key': get_random_secret_key(32)},
            no_input=True,
        )
    except Exception as e:
        typer.echo(f"错误：{e}")
    else:
        typer.echo("项目创建成功！ 🎉")


@app.command(help="构建FastAPI应用", name="startapp")
def start_app(app_name: str):
    typer.echo(f"开始创建APP: {app_name}............")
    try:
        cookiecutter(
            os.path.join(TEMPLATES_DIR, 'app'),
            extra_context={'app_name': app_name},
            no_input=True,
        )
    except Exception as e:
        typer.echo(f"错误：{e}")
    else:
        typer.echo("应用创建成功！ 🎉")


def main():
    app(prog_name="fastapi-admin")


if __name__ == '__main__':
    main()
