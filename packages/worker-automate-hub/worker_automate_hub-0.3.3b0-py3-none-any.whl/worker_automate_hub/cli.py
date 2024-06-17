from rich import emoji
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from typer import Context, Exit, Option, Typer
import pkg_resources


from .config import settings
from .core.so_manipulation import make_configuration_file

console = Console()
app = Typer()


def funcion_help(flag):
    if flag:
        print(pkg_resources.get_distribution('worker-automate-hub').version)
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

Existem 2 subcomandos disponíveis para essa aplicação

- [b]run[/]: Instância o Worker na máquina atual e inicia solicitação de trabalho para o orquestrador.
- [b]validate[/]: Valida de Worker atual está configurado corretamente e pronto para ser intanciado.

[b]Exemplos de uso:[/]
 [b][blue]RUN[/][/]
    [green][b]worker[/][/] [b]run[/]

 [b][blue]VALIDATE[/][/]
    [green][b]worker[/][/] [b]validate[/]

---

[b]Help:[/]
 [b]Para mais informações[/]
    [green][b]abin[/][/] --help

 [b]Para ver a versão instalada[/]
    [green][b]abin[/][/] --version

 [b]Para gerar o arquivo de configuração[/]
    [green][b]abin[/][/] --configure

 [b]Para informações detalhadas
    [blue][link=https://github.com/SIM-Rede/worker-automate-hub]Repo no GIT Argenta[/][/] | [blue][link=https://pypi.org/project/worker-automate-hub/]Publicação no PyPI[/][/]
"""
    if ctx.invoked_subcommand:
        return
    console.print(message)

