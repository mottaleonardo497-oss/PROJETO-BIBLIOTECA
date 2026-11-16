# =============== FUNÇÕES DO PROGRAMA BIBLIOTECA COMUNITÁRIA ===============
from rich import print
import os
import json
import emoji

ARQUIVO_DADOS = "acervo.json"


# Função que limpa a tela do terminal.
def limparTela():
    os.system('cls')


# Função que permite o usuário digitar ENTER para o programa continuar.
def enterParaContinuar():
    input("\nDigite ENTER para continuar...")


# Função que gera e retorna o código do livro (FUNÇÃO OBRIGATÓRIA - fatiamento de string).
# Regra escolhida pela equipe: 3 primeiras letras do título + 3 primeiras letras do
# ÚLTIMO NOME digitado pelo usuário no campo autor + 2 últimos dígitos do ano.
# Se o autor tiver só um nome (ex: "Homero"), a última palavra é o próprio nome,
# então a regra continua funcionando sem tratamento especial.
def geradorCodigo(titulo, autor, ano_lancamento):
    titulo_limpo = titulo.replace(" ", "").upper()
    palavras_autor = autor.strip().split()
    sobrenome = palavras_autor[-1].upper()

    codigo = titulo_limpo[:3] + sobrenome[:3] + str(ano_lancamento)[-2:]
    return codigo


# Função que gera uma mensagem/emoji específico para cada gênero do livro.
def geraMensagemGenero(genero):
    opcao = genero[:3].upper()
    match opcao:
        case "ROM":
            mensagem_genero = emoji.emojize(f"{genero} :beating_heart:")
        case "TER":
            mensagem_genero = emoji.emojize(f"{genero} :ghost:")
        case "FIC":
            mensagem_genero = emoji.emojize(f"{genero} :alien:")
        case "INF":
            mensagem_genero = emoji.emojize(f"{genero} :teddy_bear:")
        case "AVE":
            mensagem_genero = emoji.emojize(f"{genero} :cowboy_hat_face:")
        case "COM":
            mensagem_genero = emoji.emojize(f"{genero} :rolling_on_the_floor_laughing:")
        case _:
            mensagem_genero = emoji.emojize(f"{genero} :books:")

    return mensagem_genero


# Função que pede e verifica se o ano digitado é válido.
def pedeEVerificaAnoValido():
    while True:
        try:
            ano = int(input("DIGITE O ANO DE PUBLICAÇÃO: "))
            return ano
        except ValueError:
            print("Só aceitamos números.")


# Função que cadastra todas as informações de um livro.
def cadastrarLivro(acervo):
    limparTela()

    print("[bold green]-=@ CADASTRO DE LIVRO @=-[/bold green]\n")

    titulo = input("DIGITE O TÍTULO DO LIVRO: ").strip().title()
    autor = input("DIGITE O AUTOR DO LIVRO: ").strip().title()
    genero = input("DIGITE O GÊNERO DO LIVRO (Romance, Terror, Ficção, Infantil...): ").strip().capitalize()
    ano_lancamento = pedeEVerificaAnoValido()

    codigo = geradorCodigo(titulo, autor, ano_lancamento)
    mensagem_genero = geraMensagemGenero(genero)

    novo_livro = {"codigo": codigo,
                  "titulo": titulo,
                  "autor": autor,
                  "genero": genero,
                  "mensagem_genero": mensagem_genero,
                  "ano_lancamento": ano_lancamento,
                  "status": "disponível",
                  "emprestado_para": None}

    acervo.append(novo_livro)
    salvarAcervo(acervo)

    print(f"\nLivro cadastrado com sucesso! Código gerado: [bold red]{codigo}[/bold red]")
    enterParaContinuar()


# Função que exibe o menu de opções para o usuário.
def exibirMenu():
    limparTela()
    print("=" * 40)
    print("""      [bold green]-=@ BIBLIOTECA PÁGINA VIRADA @=-[/bold green]

Escolha uma opção para continuar:

    1-Cadastrar livro
    2-Buscar livro por código
    3-Registrar empréstimo / devolução
    4-Ver estatísticas do acervo
    5-Sair
    """)
    print("=" * 40)


# Função que busca um livro pelo código (FUNÇÃO OBRIGATÓRIA - retorna o livro ou None).
def buscarLivroPorCodigo(acervo, codigo):
    for i in range(len(acervo)):
        if acervo[i]["codigo"] == codigo:
            return acervo[i]
    return None


# Função que imprime a ficha completa de um livro.
def exibirFichaLivro(livro):
    limparTela()
    print("[gray]=[/gray]" * 30)
    print("[bold green]INFORMAÇÕES DO LIVRO:[/bold green]")

    if livro is None:
        print("\nNenhum livro encontrado com esse código.")
    else:
        if livro["status"] == "disponível":
            status_texto = "Disponível"
        else:
            status_texto = f"Emprestado para {livro['emprestado_para']}"

        print(f"""
[bold red]{livro["codigo"]}[/bold red]

TÍTULO: {livro["titulo"]}
AUTOR: {livro["autor"]}
GÊNERO: {livro["mensagem_genero"]}
ANO DE PUBLICAÇÃO: {livro["ano_lancamento"]}
STATUS: {status_texto}""")

    print("[gray]=[/gray]" * 30)
    enterParaContinuar()


# Função que busca um livro pelo código digitado e exibe sua ficha.
def buscarEExibirLivro(acervo):
    limparTela()
    codigo = input("DIGITE O CÓDIGO DO LIVRO: ").strip().upper()
    livro = buscarLivroPorCodigo(acervo, codigo)
    exibirFichaLivro(livro)


# Função que registra o empréstimo ou a devolução de um livro.
def registrarEmprestimoDevolucao(acervo):
    limparTela()
    codigo = input("DIGITE O CÓDIGO DO LIVRO: ").strip().upper()
    livro = buscarLivroPorCodigo(acervo, codigo)

    if livro is None:
        print("Código não encontrado no acervo.")
    else:
        if livro["status"] == "disponível":
            nome = input("Digite o nome de quem está pegando o livro emprestado: ").strip().title()
            livro["status"] = "emprestado"
            livro["emprestado_para"] = nome
            print(f"\nLivro emprestado para {nome} com sucesso!")
        else:
            resposta = input(
                f"Este livro já está emprestado para {livro['emprestado_para']}. "
                "Deseja registrar a devolução? (S/N): "
            ).strip().upper()

            if resposta == "S":
                livro["status"] = "disponível"
                livro["emprestado_para"] = None
                print("\nDevolução registrada com sucesso!")
            else:
                print("\nNenhuma alteração foi feita.")

        salvarAcervo(acervo)

    enterParaContinuar()


# Função que calcula as estatísticas do acervo (FUNÇÃO OBRIGATÓRIA - retorna um dicionário).
def calcularEstatisticas(acervo):
    total = len(acervo)

    if total == 0:
        return {"total": 0,
                "disponiveis": 0,
                "emprestados": 0,
                "por_genero": {},
                "genero_mais_comum": None}

    disponiveis = 0
    emprestados = 0
    por_genero = {}

    for livro in acervo:
        if livro["status"] == "disponível":
            disponiveis += 1
        else:
            emprestados += 1

        genero = livro["genero"]
        if genero in por_genero:
            por_genero[genero] += 1
        else:
            por_genero[genero] = 1

    maior_contagem = 0
    empatados = []

    for genero in por_genero:
        if por_genero[genero] > maior_contagem:
            maior_contagem = por_genero[genero]
            empatados = [genero]
        elif por_genero[genero] == maior_contagem:
            empatados.append(genero)

    # Ponto de decisão da equipe: em caso de empate no gênero mais comum,
    # todos os gêneros empatados são retornados numa lista.
    if len(empatados) == 1:
        genero_mais_comum = empatados[0]
    else:
        genero_mais_comum = empatados

    return {"total": total,
            "disponiveis": disponiveis,
            "emprestados": emprestados,
            "por_genero": por_genero,
            "genero_mais_comum": genero_mais_comum}


# Função que exibe as estatísticas do acervo na tela.
def exibirEstatisticas(acervo):
    limparTela()
    print("[gray]=[/gray]" * 30)
    print("[bold green]ESTATÍSTICAS DO ACERVO:[/bold green]\n")

    stats = calcularEstatisticas(acervo)

    if stats["total"] == 0:
        print("O acervo ainda está vazio. Cadastre um livro primeiro!")
    else:
        print(f"TOTAL DE LIVROS: {stats['total']}")
        print(f"DISPONÍVEIS: {stats['disponiveis']}")
        print(f"EMPRESTADOS: {stats['emprestados']}")

        print("\nLIVROS POR GÊNERO:")
        for genero in stats["por_genero"]:
            print(f"  {genero}: {stats['por_genero'][genero]}")

        print()
        if isinstance(stats["genero_mais_comum"], list):
            generos_empatados = ", ".join(stats["genero_mais_comum"])
            print(f"GÊNERO(S) COM MAIS LIVROS (empate): {generos_empatados}")
        else:
            print(f"GÊNERO COM MAIS LIVROS: {stats['genero_mais_comum']}")

    print("[gray]=[/gray]" * 30)
    enterParaContinuar()


# Função que carrega o arquivo .json do acervo (FUNÇÃO OBRIGATÓRIA - retorna a lista).
def carregarAcervo():
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


# Função que salva o acervo no arquivo .json (FUNÇÃO OBRIGATÓRIA - retorna True/False).
def salvarAcervo(acervo):
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(acervo, arquivo, ensure_ascii=False, indent=4)
        return True
    except OSError:
        return False
