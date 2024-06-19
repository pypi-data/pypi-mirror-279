"""Módulo que contém os template da ferramenta"""

TEMPLATE_LOGO = r"""
[bold blue]
███████╗███╗   ██╗ ██████╗██████╗ ██╗   ██╗██████╗ ████████╗    ██████╗ ███████╗███████╗
██╔════╝████╗  ██║██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝    ██╔══██╗██╔════╝██╔════╝
█████╗  ██╔██╗ ██║██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║       ██║  ██║█████╗  █████╗
██╔══╝  ██║╚██╗██║██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║       ██║  ██║██╔══╝  ██╔══╝
███████╗██║ ╚████║╚██████╗██║  ██║   ██║   ██║        ██║       ██████╔╝███████╗██║
╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝       ╚═════╝ ╚══════╝╚═╝
[/bold blue]
"""

TEMPLATE_INFO = """
Ferramenta de linha de comando em Python para encriptar e desencriptar dados e arquivos de forma segura.

**Principais Funcionalidades:**
 - Encriptação e desencriptação de dados e arquivos.
 - Utilização de uma chave de criptografia fornecida pelo usuário.

**Como Funciona:**
Encryptdef utiliza criptografia AES GCM (Galois/Counter Mode) com chave derivada pelo algoritmo Scrypt, garantindo uma proteção robusta para seus dados.

**Nota Importante:**
> **Mantenha a chave de encriptação em segredo e não a perca. Sem a chave correta, não será possível desencriptar os dados ou arquivos.**
"""

TEMPLATE_MENU_MESSAGE_FILE = """
[bold blue][!] [M E N U  I N T E R A T I V O][/bold blue]

[bold yellow][1] 🔠 DADOS[/bold yellow]
[bold yellow][2] 📄 ARQUIVOS[/bold yellow]

[bold red][3] 🔚 SAIR[/bold red]
"""

TEMPLATE_MENU_ENCRYPT_DECRYPT = """
[bold blue][!] [E N C R I P T A Ç Ã O] / [D E C R I P T A Ç Ã O][/bold blue]

[bold yellow][1] 🔒 ENCRIPTAÇÃO[/bold yellow]
[bold yellow][2] 🔓 DECRIPTAÇÃO[/bold yellow]

[bold red][3] 🔚 SAIR[/bold red]
"""

TEMPLATE_ENCRYPT_MESSAGE = """
[bold cyan] 🔠 DIGITE O TEXTO QUE DESEJA ENCRIPTAR:[/bold cyan]"""

TEMPLATE_ENCRYPT_KEY = """\
[bold cyan] 🔑 DIGITE A CHAVE DE ENCRIPTAÇÃO:[/bold cyan]"""

TEMPLATE_DECRYPT_MESSAGE = """
[bold cyan] 🔠 DIGITE O TEXTO QUE DESEJA DECRIPTAR:[/bold cyan]"""

TEMPLATE_DECRYPT_KEY = """\
[bold cyan] 🔑 DIGITE A CHAVE DE DECRIPTAÇÃO:[/bold cyan]"""

TEMPLATE_ENCRYPT_FILE = """\
[bold cyan][file] 📄 DIGITE O NOME DO ARQUIVO QUE DESEJA ENCRIPTAR:[/bold cyan]
[bold cyan][key] 🔑 DIGITE A CHAVE DE ENCRIPTAÇÃO:[/bold cyan]
[bold cyan][new-file] 🔒📄 DIGITE UM NOVO NOME PARA O ARQUIVO ENCRIPTADO:[/bold cyan]"""

TEMPLATE_DECRYPT_FILE = """\
[bold cyan][file] 🔒📄 DIGITE O NOME DO ARQUIVO QUE DESEJA DECRIPTAR:[/bold cyan]
[bold cyan][key] 🔑 DIGITE A CHAVE DE DECRIPTAÇÃO:[/bold cyan]
[bold cyan][new-file] 📄 DIGITE UM NOVO NOME PARA O ARQUIVO DECRIPTADO:[/bold cyan]"""

TEMPLATE_CONTINUE_LEAVE = """
[bold blue] ❔ PRESSIONE ENTER PARA CONTINUAR, OU QUALQUER TECLA PARA SAIR:[/bold blue]"""

TEMPLATE_ERROR_INVALID_CHOICE = """
 ⚠  ERRO - ESCOLHA INVALÍDA. TENTA NOVAMENTE!"""

TEMPLATE_ERROR_EMPTY_FIELD = """
 ⚠  ERRO - CAMPO ESTÁ VAZIO. TENTA NOVAMENTE!
"""

TEMPLATE_ENCRYPTED = """
[bold green] 🔒 ENCRIPTADO: [italic]%s[/italic][/bold green]
"""

TEMPLATE_DECRYPTED = """
[bold green] 🔓 DECRIPTADO: [italic]%s[/italic][/bold green]
"""

TEMPLATE_ENCRYPTED_MESSAGE = """
[bold green blink] 🔒 [D A D O S -- E N C R I P T A D O S] 🔒[/bold green blink]"""

TEMPLATE_DECRYPTED_MESSAGE = """
[bold green blink] 🔓 [D A D O S -- D E C R I P T A D O S] 🔓[/bold green blink]"""

TEMPLATE_INVALID_KEY = """
 ⚠  CHAVE NÃO ECONTRADA, TENTE UMA CHAVE CORRETA!
"""

TEMPLATE_ENCRYPTED_FILE = """
[bold green blink] 🔒 [A R Q U I V O -- E N C R I P T A D O] 🔒[/bold green blink]

[bold green] 🔒📄 [italic]'%s'[/italic][/bold green]
"""

TEMPLATE_DECRYPTED_FILE = """
[bold green blink] 🔓 [A R Q U I V O -- D E C R I P T A D O] 🔓[/bold green blink]

[bold green] 📄 [italic]'%s'[/italic][/bold green]
"""

TEMPLATE_FILE_NOT_FOUND = """
 ⚠  ARQUIVO '%s' NÃO ENCONTRADO!
"""

TEMPLATE_INFO_FILE = """
[bold blue] ❕ COLOQUE O ARQUIVO NO DIRETORIO ATUAL, OU INFORME O CAMINHO EXATO DO ARQUIVO EXEMPLO: [italic]/tmp/teste.txt[/italic][/bold blue]
"""

TEMPLATE_GET_MAX_WORKERS = """
[bold magenta] 💻 Arquivo tem mais de [bold cyan]500[/bold cyan] linhas. Quantos núcleos da cpu você quer usar ([bold cyan]1-%s[/bold cyan]): [/bold magenta]"""

TEMPLATE_TASK_DESCRIPTION = """\
[yellow] Processando linhas do arquivo...
"""

TEMPLATE_ERROR_INVALID_ENCRYPTED_FORMAT = """
 ⚠  ERRO - FORMATO DE STRING CRIPTOGRAFADA INVÁLIDO!"""

TEMPLATE_TYPE_ERROR = """
 ⚠  ERRO - ESPERADO UMA STRING, OBTIDO '%s'."""

TEMPLATE_IS_DIRECTORY = """
 ⚠  ERRO - '%s' É UM DIRETÓRIO, NÃO UM ARQUIVO."""

TEMPLATE_EMPTY_FILE_ERROR = """
 ⚠  ERRO - ARQUIVO '%s' ESTÁ VAZIO."""
