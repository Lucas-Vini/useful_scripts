import unicodedata

letras_um_ponto = ['e', 'a', 'i', 'o', 'n', 'r', 't', 'l', 's', 'u']
letras_dois_pontos = ['d', 'g']
letras_tres_pontos = ['b', 'c', 'm', 'p']
letras_cinco_pontos = ['f', 'h', 'v']
letras_oito_pontos = ['j', 'x']
letras_treze_pontos = ['q', 'z']
banco_de_palavras = ["Abacaxi", "Manada", "mandar", "porta", "mesa", "Dado",
                     "Mangas", "Já", "coisas", "radiografia", "matemática",
                     "Drogas", "prédios", "implementação", "computador",
                     "balão", "Xícara", "Tédio", "faixa", "Livro", "deixar",
                     "superior", "Profissão", "Reunião", "Prédios", "Montanha",
                     "Botânica", "Banheiro", "Caixas", "Xingamento",
                     "Infestação", "Cupim", "Premiada", "empanada", "Ratos",
                     "Ruído", "Antecedente", "Empresa", "Emissário", "Folga",
                     "Fratura", "Goiaba", "Gratuito", "Hídrico", "Homem",
                     "Jantar", "Jogos", "Montagem", "Manual", "Nuvem", "Neve",
                     "Operação", "Ontem", "Pato", "Pé", "viagem", "Queijo",
                     "Quarto", "Quintal", "Solto", "rota", "Selva", "Tatuagem",
                     "Tigre", "Uva", "Último", "Vitupério", "Voltagem",
                     "Zangado", "Zombaria", "Dor"]

def normalizar_palavra(palavra):
    '''Remove acentos, cedilha e deixa tudo em letra minúscula'''
    palavra = unicodedata.normalize("NFKD", palavra)
    palavra = palavra.encode('ascii', 'ignore')
    palavra = palavra.decode("utf-8")
    palavra = palavra.lower()
    return palavra

def formar_palavras(letras_disponiveis):
    '''Retorna as palavras do banco de palavras que são possíveis
    formar com as letras disponiveis'''
    palavras_formadas = []
    for palavra in banco_de_palavras:
        palavra = normalizar_palavra(palavra)
        if conferir_letras(letras_disponiveis, palavra):
            palavras_formadas.append(palavra)
    return palavras_formadas

def conferir_letras(letras_disponiveis, palavra):
    '''Retorna True se for possível formar a palavra com as letras disponiveis,
    caso contrário, retorna False'''
    for letra in palavra:
        if letra in letras_disponiveis:
            letras_disponiveis = letras_disponiveis.replace(letra, '', 1)
        else:
            return False
    return True

def checar_pontuação(palavra, posicao_bonus):
    '''Retorna a pontuação da palavra informada, levando em consideração a
    posição bônus escolhida pelo usuário'''
    pontuacao = 0
    posicao = 1
    for letra in palavra:
        if posicao == posicao_bonus:
            bonus = 2
        else:
            bonus = 1        
        if letra in letras_um_ponto:
            pontuacao += 1*bonus
        elif letra in letras_dois_pontos:
            pontuacao += 2*bonus
        elif letra in letras_tres_pontos:
            pontuacao += 3*bonus
        elif letra in letras_cinco_pontos:
            pontuacao += 5*bonus
        elif letra in letras_oito_pontos:
            pontuacao += 8*bonus
        elif letra in letras_treze_pontos:
            pontuacao += 13*bonus
        posicao += 1
    return pontuacao

def comparar_pontuacoes(pontuacao_atual, maior_pontuacao):
    '''Dada duas listas, cada uma contendo no primeiro índice uma palavra e
    no segundo índice sua respectiva pontuação, compara as duas listas e
    retorna a lista com maior pontuaçao, aplicando critérios de desempate'''
    if pontuacao_atual[1] > maior_pontuacao[1]:
        maior_pontuacao[0] = pontuacao_atual[0]
        maior_pontuacao[1] = pontuacao_atual[1]
    elif pontuacao_atual[1] == maior_pontuacao[1]:
        if len(pontuacao_atual[0]) < len(maior_pontuacao[0]):
            maior_pontuacao[0] = pontuacao_atual[0]
            maior_pontuacao[1] = pontuacao_atual[1]
        elif len(pontuacao_atual[0]) == len(maior_pontuacao[0]):
            if pontuacao_atual[0] < maior_pontuacao[0]:
                maior_pontuacao[0] = pontuacao_atual[0]
                maior_pontuacao[1] = pontuacao_atual[1]
    return maior_pontuacao

def verificar_maior_pontuacao(letras_disponiveis, posicao_bonus):
    '''Dada as letras disponíveis, retorna uma tupla com a maior pontuacao e
    uma variável booleana que indica se deve procurar por mais palavras'''
    palavras_formadas = formar_palavras(letras_disponiveis)
    procurar_mais_palavras = False
    if len(palavras_formadas) > 1:
        procurar_mais_palavras = True

    maior_pontuacao = ['', 0]
    pontuacao_atual = ['', 0]
    for palavra_formada in palavras_formadas:
        pontuacao_atual[0] = palavra_formada
        pontuacao_atual[1] = checar_pontuação(palavra_formada, posicao_bonus)
        maior_pontuacao = comparar_pontuacoes(pontuacao_atual, maior_pontuacao)

    return (maior_pontuacao, procurar_mais_palavras)

def separar_letras(letras_disponiveis, palavra):
    '''Retira das letras disponiveis as letras da palavra fornecida'''
    sobraram = letras_disponiveis
    for letra in palavra:
        sobraram = sobraram.replace(letra, '', 1)
    return sobraram   

def main():
    '''
    Funcionamento do programa:

    - Inicialmente é solicitado que o usuário digite as letras disponíveis. (1)

    - Para poder encerrar o programa, o usuário pode digitar apenas a letra
    "q". (2)

    - Depois o programa recebe a posição bônus para pontuar em dobro na posição
    informada de acordo com a funcionalidade extra em que é permitido escolher
    uma posição bônus. Recebe e valida a entrada, se o usuário digitar uma
    entrada inválida, é informado que deve digitar um número inteiro. (3)
    
    - Logo em seguida, as letras disponiveis informadas pelo usuário são
    normalizadas, isto é, caracteres com acentos ou cedilha são substituídos
    por suas formas sem acento e todas as letras são levadas a sua forma
    minúscula, tudo isso é realizado através da função "normalizar_palavra",
    isso é feito pois queremos desconsiderar acentos e diferenças entre letras
    maiúsculas e minúsculas. (4)

    - Feito isso, entramos em um loop que vai procurar pela palavra de maior
    pontuacao dadas as letras disponíveis, depois a palavra com maior pontuacao
    com as letras que restaram e assim por diante até de fato não for possível
    formar nenhuma palavra com as letras restantes, obdecendo a funcionalidade
    extra em que o programa é permitido responder com múltiplas palavras caso
    a pontuação seja maior. (5)

    - A procura pela palavra de maior pontuação com as letras disponíveis é
    feita pela função "verificar_maior_pontuacao". Esta função confere quais
    palavras são possíveis formar com as letras disponíveis, checa a pontuação
    de cada uma delas e seleciona a com maior pontuação aplicando os critérios
    de desmpate. Além disso ela retorna se devemos continuar no loop procurando
    por mais palavras ou não. (6)

    - Após selecionar a palavra com a maior pontuação, o programa separa as
    letras que sobraram. (7)

    - Finalmente, o programa imprime os resultados obtidos, ou seja, imprime
    a(s) palavra(s) com a(s) maior(es) pontuação(ões), a pontuação obtida e as
    letras que não foram utilizadas para formar a palavra. Há também uma
    impressão específica para casos em que nenhuma palavra foi encontrada e
    quando não sobram letras após formar a(s) palavra(s)(8)

    OBS1: Todas as funções também possuem uma docstring para facilitar o
    entendimento do funcionamento do programa.
    
    ---------------------------------------------------------------------------
    Utilização do programa:
    - Com o python instalado, abra o terminal e execute o código. Exemplo:
    "python Lucas_Vinicius_Mota_da_Silva_Desafio_Pratico.py"

    - Será solicitado que o usuário digite as letras disponíveis para esta
    partida. O usuário deve digitar as letras disponíveis. Exemplo:
     "# Digite as letras disponíveis nesta jogada: AcaBaXis"

    - Depois será solicitado que o usuário digite uma posição bônus para
    pontuar em dobro. O valor digitado deve ser um número inteiro, caso
    contrário será solicitado que o usuário digite outro valor. Exemplo:
    "# Digite a posição bônus: 2"    

    - Logo em seguida será impresso a(s) palavra(s) com maior(es) pontuação(ões)
    que era possível formar com as letras disponíveis e as letras que não foram
    utilizadas. Exemplo:
    "
    #
    # ABACAXI, palavra de 21 pontos
    # Sobraram: S
    "

    - Para encerrar a execução do programa, basta digitar "q" quando as
    letras disponíveis forem solicitadas. Exemplo:
    "# Digite as letras disponíveis nesta jogada: q"    
    
    OBS1: O programa foi desenvolvido utilizando Python na versão 3.9.3.
    OBS2: O programa utiliza o módulo "unicodedata" que é um módulo padrão do
    Python, então provavelmente não será necessário se preocupar com sua
    instalação.    
    '''
    
    #(1) - Recebe do usuário as letras disponíveis nesta jogada
    print("# Digite as letras disponíveis nesta jogada:", end=" ")
    letras_disponiveis = input()

    #(2) - Caso o usuário tenha digitado apenas "q", encerra o programa
    if letras_disponiveis == 'q':
        print("\nObrigado pela participação, até mais!")
        return False

    #(3) - Recebe e valida a posicão bônus
    valor_valido = False
    while not valor_valido:
        print("# Digite a posição bônus:", end=" ")
        try:
            posicao_bonus = int(input())
            valor_valido = True
        except:
            print("# Valor inválido. A posição bônus deve ser um número inteiro.")
    
    #(4) - Normaliza as letras disponiveis, isto é, remove acentos e cedilha
    letras_disponiveis = normalizar_palavra(letras_disponiveis)

    #(5) - Loop procurando pelas combinações de palavras com maior pontuação
    procurar_mais_palavras = True
    maiores_pontuacoes = []
    while procurar_mais_palavras:
        #(6) - Escolhe a palavra com maior pontuaçao com as letras restantes
        resultados = verificar_maior_pontuacao(letras_disponiveis,
                                               posicao_bonus)
        maiores_pontuacoes.append(resultados[0])
        procurar_mais_palavras = resultados[1]
        #(7) - Separa as letras que sobraram depois de formar uma palavra
        letras_disponiveis = separar_letras(letras_disponiveis,
                                            maiores_pontuacoes[-1][0])

                   
    #(8) - Imprime resultado
    sobraram = letras_disponiveis
    print('#', '#', sep='\n', end=' ')
    if len(maiores_pontuacoes[0][0]) > 0:
        total = 0
        for pontuacao in maiores_pontuacoes:
            if pontuacao[1] > 0:
                print(pontuacao[0].upper(), end=', ')
                total += pontuacao[1]
        print('total de ', total, ' pontos')
        if len(sobraram) > 0:
            print("# Sobraram: ", end='')
            letra_index = 1
            for letra in sobraram:
                if letra_index < len(sobraram):
                    print(letra.upper(), end=', ')
                else:
                    print(letra.upper(), end='\n\n')
                letra_index += 1
        else:
            print("")
    else:
        print("Nenhuma palavra encontrada")
        print("# Sobraram: 0\n")

    return True

if __name__ == '__main__':
    continuar_jogando = True
    while continuar_jogando:        
        continuar_jogando = main()
