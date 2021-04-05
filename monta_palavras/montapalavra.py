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
