from typing import Optional

import typer

from importlib import metadata

from exiffusion.fuse import fuse_exif

APP_NAME = "ExifFusion"
APP_VERSION = metadata.version("exiffusion")

app = typer.Typer(no_args_is_help=True)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{APP_NAME} v{APP_VERSION}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    return


@app.command(no_args_is_help=True)
def fuse(
    path: str = typer.Argument(..., help="Input directory or image path."),
    output: str = typer.Argument(..., help="Output directory to store the images."),
):
    """
    Overlay Exif metadata such as timestamp and location onto images.
    """
    fuse_exif(path, output)


def cli():
    app(prog_name=APP_NAME)
