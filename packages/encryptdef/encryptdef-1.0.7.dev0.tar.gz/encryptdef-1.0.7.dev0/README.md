
<p align="center">
  <a href="https://github.com/AyslanBatista/encryptdef">
    <img src="https://raw.githubusercontent.com/AyslanBatista/encryptdef/main/assets/logo_encryptdef.jpg" alt="encryptdef" style="width: 80%; height: auto;">
  </a>
</p>

<p align="center">
<a href="https://github.com/AyslanBatista/encryptdef/actions/workflows/main.yml" target="_blank">
    <img src="https://github.com/AyslanBatista/encryptdef/actions/workflows/main.yml/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/AyslanBatista/encryptdef" > 
    <img src="https://codecov.io/gh/AyslanBatista/encryptdef/branch/main/graph/badge.svg?token=JW21dkelbB"/> 
</a>
<a href="https://app.codacy.com/gh/AyslanBatista/encryptdef/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade">
  <img src="https://app.codacy.com/project/badge/Grade/9671954a158345898198c1419212a271">
</a>
<a href="https://github.com/AyslanBatista/encryptdef?tab=Unlicense-1-ov-file#readme" target="_blank">
    <img src="https://img.shields.io/badge/license-MIT-007EC7.svg?color=%2334D058" alt="License">
</a>
</p>

---
**Encryptdef** é uma ferramenta de linha de comando em Python para encriptar e desencriptar dados e arquivos de forma segura, utilizando criptografia de última geração e uma chave de criptografia fornecida pelo usuário. Proteja suas informações confidenciais e arquivos importantes contra acesso não autorizado com o Encryptdef.

### Como Funciona

Encryptdef utiliza o método de criptografia **AES GCM (Galois/Counter Mode)** com chave derivada pelo algoritmo **Scrypt**, fornecendo uma camada de segurança robusta para seus dados.

#### Detalhes Técnicos
- **AES (Advanced Encryption Standard)**: Algoritmo de criptografia seguro e amplamente utilizado.
- **GCM (Galois/Counter Mode)**: Modo de operação que oferece confidencialidade e integridade dos dados.
- **Scrypt**: Função de derivação de chave resistente a ataques de força bruta, intensiva em memória e computacionalmente cara.

## Instalação

```bash
$ pip install encryptdef
```
<code><b>Importante: Mantenha a chave de encriptação em segredo e não a perca. Sem a chave correta, não será possível desencriptar os dados ou arquivos.</b></code>

## Como usar:
#### Modo CLI

```bash
$ encryptdef --help
```
- Você pode encriptar e desencriptar textos e arquivos usando os argumentos `encrypt` e `decrypt`.
- Para trabalhar com textos, use `--message=`.
- Para trabalhar com arquivos, use `--file=`.
 
- Você pode informar a chave que está dentro de um arquivo usando `--keyfile=`. Caso você não passe o argumento, será solicitado a chave:
```bash
$ encryptdef encrypt --message="testando"
🔑 DIGITE A CHAVE DE ENCRIPTAÇÃO:

🔒 [D A D O S -- E N C R I P T A D O S] 🔒

🔒 ENCRIPTADO: ZOvi7HOjsx4=*hsyuvGWe3i+QFehOCgC/ZA==*Bx0nvNmsg5RR0frUZENoKA==*P7uzyE4dfTAKPqBcHooOow==

```

#### Modo Interativo
```bash
$ encryptdef
```
![](https://raw.githubusercontent.com/AyslanBatista/encryptdef/main/assets/encryptdef_interativo.gif)
