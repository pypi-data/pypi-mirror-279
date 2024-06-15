from typer.testing import CliRunner

from importlib import metadata

from exiffusion import cli

APP_NAME = "ExifFusion"
APP_VERSION = metadata.version("exiffusion")


runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{APP_NAME} v{APP_VERSION}\n" in result.stdout
