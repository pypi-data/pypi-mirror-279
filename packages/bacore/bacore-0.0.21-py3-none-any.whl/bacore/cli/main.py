"""BACore CLI entrypoint module."""
from bacore.cli import create, serve, test, upgrade
from typer import Typer

app = Typer(rich_markup_mode="rich", add_completion=False)
app.add_typer(create.app, name="create", help="Create a project")
app.add_typer(serve.app, name="serve", help="Serve documentation")
app.add_typer(test.app, name="test", help="test...")
app.add_typer(upgrade.app, name="upgrade", help="Upgrade")
