Implementar em python, C ou C++ o algoritmo MINIMAX com podas
alfa-beta para encontrar a melhor jogada para o Jogo da Onça a cada
estado do jogo.  (https://pt.wikipedia.org/wiki/Jogo_da_onça)

A implementação deve separar em módulos de código fonte indemendentes:

- o procedimento que interage com o jogador adversário e mantém o
  estado atualizado do tabuleiro;

- o procedimento de busca que executa o algoritmo MINIMAX com podas
  alfa-beta e decide pela ação mais adequada;

- a modelagem do jogo como um problema de busca adversarista no espaço
  de estados;

- a função de estimativa de recompença caso seja necessária.

O tabuleiro do jogo possui 7 linhas e 5 colunas organizadas segundo o
diagrama que segue. Os pontos marcados com * indicam as 31 posições
válidas para as peças do jogo. As linhas tracejadas indicam as
direções possíveis para os movimentos das peças entre as posições
válidas. As linhas estabelecem a relação de adjacência entre as
posições válidas. Por exemplo, a segunda posição da quinta linha (5,2)
não está conectada com a posição (6,2). Apesar de serem duas posições
válidas, não há uma linha tracejada que permita a movimentação direta
de uma para a outra. O mesmo ocorre entre as posições (1,2) e (2,3).

  1    2    3    4    5
1 *----*----*----*----*
  |\   |   /|\   |   /|
  | \  |  / | \  |  / |
  |  \ | /  |  \ | /  |
  |   \|/   |   \|/   |
2 *----*----*----*----*
  |   /|\   |   /|\   |
  |  / | \  |  / | \  |
  | /  |  \ | /  |  \ |
  |/   |   \|/   |   \|
3 *----*----*----*----*
  |\   |   /|\   |   /|
  | \  |  / | \  |  / |
  |  \ | /  |  \ | /  |
  |   \|/   |   \|/   |
4 *----*----*----*----*
  |   /|\   |   /|\   |
  |  / | \  |  / | \  |
  | /  |  \ | /  |  \ |
  |/   |   \|/   |   \|
5 *----*----*----*----*
           /|\
          / | \
         /  |  \
        /   |   \ 
6      *----*----*
      /     |     \
     /      |      \
    /       |       \
   /        |        \
7 *---------*---------* 

O jogo é assimétrico, 14 cães competem contra uma única onça. O
objetivo do jogador que controla a onça é retirar 5 cães do tabuleiro,
o objetivo do jogador que controla os cães é imobilizar a onça. O
jogador que alcançar antes seu objetivo vence o jogo. A configuração
inicial do tabuleiro é dada pelo seguinte posicionamento das 15 peças
no tabuleiro. Os cães, representados pela letra 'c', ocupam as
posições (1,1), (1,2), (1,3), (1,4), (1,5), (2,1), (2,2), (2,3),
(2,4), (2,5), (3,1), (3,2), (3,4) e (3,5). A onça, representada pela
letra 'o', inicia na posição (3,3) do tabuleiro.

Tabuleiro inicial:

  1    2    3    4    5
1 c----c----c----c----c
  |\   |   /|\   |   /|
  | \  |  / | \  |  / |
  |  \ | /  |  \ | /  |
  |   \|/   |   \|/   |
2 c----c----c----c----c
  |   /|\   |   /|\   |
  |  / | \  |  / | \  |
  | /  |  \ | /  |  \ |
  |/   |   \|/   |   \|
3 c----c----o----c----c
  |\   |   /|\   |   /|
  | \  |  / | \  |  / |
  |  \ | /  |  \ | /  |
  |   \|/   |   \|/   |
4 *----*----*----*----*
  |   /|\   |   /|\   |
  |  / | \  |  / | \  |
  | /  |  \ | /  |  \ |
  |/   |   \|/   |   \|
5 *----*----*----*----*
           /|\
          / | \
         /  |  \
        /   |   \ 
6      *----*----*
      /     |     \
     /      |      \
    /       |       \
   /        |        \
7 *---------*---------* 

O jogador que controla a onça sempre inicia o jogo. Os dois jogadores
se revesam movendo apenas uma peça de cada vez. Um cão pode se mover
para uma posição adjacente que esteja desocupada. A onça, além de se
mover como os cães, pode saltar sobre um ou mais cães, retirando esses
do tabuleiro. Um salto da onça sobre um cão, pode ser realizado se o
cão estiver numa posição adjacente à da onça e a posição seguinte, na
mesma direção, estiver desocupada. O movimento de salto, quando
possível, não é obrigatório.

As ações decididas pelo seu programa seram enviadas em formato texto
para o jogador adverário. O formato para a ação de movimento simples
é:

<peça> m <linha orig> <coluna orig> <linha dest> <coluna dest>

A ação de salto da onça segue o formato:

o s <n> <linha orig> <coluna orig> <sequência de destinos>

sendo <n> o número de saltos consecutivoe e <sequência de destinos>
dado por:

<linha dest 1> <coluna dest 1> ... <linha dest n> <coluna dest n>

Por exemplo, a seguinte sequência de ações

o m 3 3 4 3
c m 3 5 4 4
o m 4 3 5 3
c m 3 1 4 1
o s 3 5 3 3 5 3 3 3 1

remove 3 cães das posições (4,4), (3,4) e (3,2), resultando na
seguinte configuração do tabuleiro:

  1    2    3    4    5
1 c----c----c----c----c
  |\   |   /|\   |   /|
  | \  |  / | \  |  / |
  |  \ | /  |  \ | /  |
  |   \|/   |   \|/   |
2 c----c----c----c----c
  |   /|\   |   /|\   |
  |  / | \  |  / | \  |
  | /  |  \ | /  |  \ |
  |/   |   \|/   |   \|
3 o----*----*----*----*
  |\   |   /|\   |   /|
  | \  |  / | \  |  / |
  |  \ | /  |  \ | /  |
  |   \|/   |   \|/   |
4 c----*----*----*----*
  |   /|\   |   /|\   |
  |  / | \  |  / | \  |
  | /  |  \ | /  |  \ |
  |/   |   \|/   |   \|
5 *----*----*----*----*
           /|\
          / | \
         /  |  \
        /   |   \ 
6      *----*----*
      /     |     \
     /      |      \
    /       |       \
   /        |        \
7 *---------*---------* 