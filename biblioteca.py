# BIBLIOTECA COMUNITÁRIA - PÁGINA VIRADA
import biblioteca_funcoes as f

f.limparTela()

acervo = f.carregarAcervo()

while True:
    f.exibirMenu()

    try:
        opcao = int(input("Digite sua opção: "))

        match opcao:
            case 1:
                f.cadastrarLivro(acervo)
            case 2:
                f.buscarEExibirLivro(acervo)
            case 3:
                f.registrarEmprestimoDevolucao(acervo)
            case 4:
                f.exibirEstatisticas(acervo)
            case 5:
                f.limparTela()
                print("Até logo! A Biblioteca Página Virada agradece a visita :)")
                break
            case _:
                f.limparTela()
                print("Opção inválida, tenta de novo.")
                f.enterParaContinuar()

    except ValueError:
        print("Só aceitamos número.")
        f.enterParaContinuar()
