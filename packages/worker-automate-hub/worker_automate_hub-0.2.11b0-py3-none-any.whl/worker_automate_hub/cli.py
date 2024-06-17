from rich import emoji
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from typer import Context, Exit, Option, Typer

from worker_automate_hub import __version__

from .config import settings
from .core.so_manipulation import make_configuration_file

console = Console()
app = Typer()


def funcion_help(flag):
    if flag:
        print(__version__)
        raise Exit(code=0)


def function_configure(flag):
    if flag:
        configuration = make_configuration_file()
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

Existem 4 subcomandos disponíveis para essa aplicação

- [b]list[/]: Fornece, em tela, uma árvore com todas as aplicações e ambientes cadastrados no Vault
- [b]get[/]: Fornece os secrets cadastrados em uma aplicação. Este retorno pode ser em tela ou arquivo
- [b]update[/]: Envia uma nova coleção de ENV para uma determinada aplicação [red](Uso restrito, somente TL e SRE)[/]
- [b]compare[/]: Compara o ENV de uma aplicação em 2 ambientes

[b]Exemplos de uso:[/]
 [b][blue]LIST[/][/]
    [green][b]abin[/][/] [b]list[/]

 [b][blue]GET[/][/]
    [green][b]abin[/][/] [b]get[/] --app api-auth --env dev --proj sim [magenta](para retorno em tela use [green][b]--no-file[/][/])[/]

 [b][blue]UPDATE[/][/]
    [green][b]abin[/][/] [b]update[/] --app api-auth --env dev --proj sim --file .env [magenta](para atualizar outro secret use [green][b]--secret NOME[/][/])[/]

 [b][blue]COMPARE[/][/]
    [green][b]abin[/][/] [b]compare[/] --app api-auth --env qa,dev --proj sim

---
[b]Help:[/]
 [b]Para mais informações[/]
    [green][b]abin[/][/] --help

 [b]Para ver a versão instalada[/]
    [green][b]abin[/][/] --version

 [b]Para gerar o arquivo de configuração[/]
    [green][b]abin[/][/] --configure

 [b]Para informações detalhadas
    [blue][link=https://github.com/SIM-Rede/abin-sim/tree/main]Repo no GIT SIM[/][/] | [blue][link=https://pypi.org/project/abin-sim/]Publicação no PyPI[/][/]
"""
    if ctx.invoked_subcommand:
        return
    console.print(message)

