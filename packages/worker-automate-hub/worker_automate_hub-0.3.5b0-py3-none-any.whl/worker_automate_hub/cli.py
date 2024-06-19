import asyncio
import importlib.metadata

from rich import emoji
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from typer import Context, Exit, Option, Typer

from run import run_application

# from ..config import settings
from .core.so_manipulation import make_configuration_file

console = Console()
app = Typer()


def funcion_help(flag):
    if flag:
        print(importlib.metadata.version('worker-automate-hub'))
        raise Exit(code=0)


def function_configure(flag):
    if flag:
        configuration = make_configuration_file()
        console.print(configuration['Message'])
        raise Exit(code=0)


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
    version: bool = Option(False, callback=funcion_help, is_flag=True),
    configure: bool = Option(False, callback=function_configure, is_flag=True),
):
    message = """
[b]Worker[/] - Grupo Argenta

Forma de uso: [b]worker [SUBCOMANDO] [ARGUMENTOS][/]

Existem 3 subcomandos disponíveis para essa aplicação

- [b]run[/]: Inicializa o Worker na máquina atual e começa a solicitar trabalho para o orquestrador.
- [b]validate[/]: Verifica se o Worker atual está configurado corretamente e pronto para ser inicializado.
- [b]assets[/]: Realiza a limpeza e depois download na pasta assets de todos arquivos utilizado pelo worker durante execução.

[b]Exemplos de uso:[/]
 [b][blue]RUN[/][/]
    [green][b]worker[/][/] [b]run[/]

 [b][blue]VALIDATE[/][/]
    [green][b]worker[/][/] [b]validate[/]

---

[b]Help:[/]
 [b]Para mais informações[/]
    [green][b]worker[/][/] --help

 [b]Para ver a versão instalada[/]
    [green][b]worker[/][/] --version

 [b]Para gerar o arquivo de configuração[/]
    [green][b]worker[/][/] --configure

 [b]Para informações detalhadas
    [blue][link=https://github.com/SIM-Rede/worker-automate-hub]Repo no GIT Argenta[/][/] | [blue][link=https://pypi.org/project/worker-automate-hub/]Publicação no PyPI[/][/]
"""
    if ctx.invoked_subcommand:
        return
    console.print(message)


@app.command()
def run():
    asyncio.run(run_application())
