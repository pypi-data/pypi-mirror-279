# SPDX-FileCopyrightText: 2024-present Mark Hall <mark.hall@open.ac.uk>
#
# SPDX-License-Identifier: MIT
"""TM352 CLI Application."""

from rich import print
from typer import Typer

from tm352_app.__about__ import __version__
from tm352_app.vce import app as vce_app

app = Typer()
app.add_typer(vce_app, name="vce")


@app.command()
def version() -> None:
    """Output the current application version."""
    print(__version__)
