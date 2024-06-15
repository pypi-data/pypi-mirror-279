from unconscious import _unconscious
import asyncio
import threading
import typer


VERSION = "0.1.0"


def get_version():
    return VERSION


async def async_rust_server():
    await _unconscious.rust_server()


def typer_cli_app_function():
    app = typer.Typer()

    @app.command()
    def serve():
        asyncio.run(async_rust_server())

    @app.command()
    def version():
        version = get_version()
        typer.echo(version)

    @app.callback(invoke_without_command=True)
    def main(ctx: typer.Context):
        if ctx.invoked_subcommand is None:
            typer.echo("No command specified. Starting the server.")
            asyncio.run(async_rust_server())

    # run the app but if no command is given, print the help message
    app()


def rust_server_cli():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_rust_server())


class Client:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.run_server)
        self.thread.start()

    def run_server(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.main())

    async def main(self):
        await _unconscious.rust_server()

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
