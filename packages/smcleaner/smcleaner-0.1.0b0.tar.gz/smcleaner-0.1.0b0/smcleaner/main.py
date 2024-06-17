import typer


app = typer.Typer()


@app.command()
def it_works():
    """
    Tells that it works.
    """
    typer.echo("It works!")
