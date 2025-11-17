"""
Jogador de IA para o Jogo da Onça
Utiliza Minimax com poda Alfa-Beta para decidir os movimentos
"""

import sys
import tabuleiro
from jogo import EstadoJogo
from busca import BuscaAdversarial

def main():
    """Programa principal do jogador IA"""
    
    # Conecta com o controlador do campo
    tabuleiro.conectar(sys.argv)
    
    # Determina o lado do jogador
    lado_meu = tabuleiro.lado_jogador
    
    print(f"IA iniciada jogando como: {lado_meu}", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    
    profundidade = 5
    tempo_limite = 30  # 30 segundos por jogada
    
    busca = BuscaAdversarial(profundidade_maxima=profundidade, tempo_limite=tempo_limite)
    
    contador_jogadas = 0
    historico_posicoes = []  # Rastreia últimas N posições para detectar repetições
    MAX_HISTORICO = 10  # Quantidade de posições para rastrear
    
    while True:
        # Recebe o estado atual do jogo
        buf = tabuleiro.receber()
        
        # Separa os elementos da string recebida
        parts = buf.split('\n', 2)
        lado_confirma = parts[0]
        mov_adv_str = parts[1]
        tabuleiro_str = parts[2]
        
        contador_jogadas += 1
        
        print(f"\n{'=' * 50}", file=sys.stderr)
        print(f"Jogada #{contador_jogadas}", file=sys.stderr)
        print(f"Meu lado: {lado_meu}", file=sys.stderr)
        print(f"Movimento adversário: {mov_adv_str}", file=sys.stderr)
        
        # Cria o estado do jogo a partir do tabuleiro recebido
        estado = EstadoJogo(tabuleiro_str)
        
        # Debug: mostra tabuleiro parseado
        print(f"DEBUG - Tabuleiro parseado: {len(estado.tabuleiro)} posições", file=sys.stderr)
        
        if estado.eh_terminal():
            vencedor = estado.vencedor()
            print(f"Jogo terminado! Vencedor: {vencedor}", file=sys.stderr)
            tabuleiro.enviar(f"{lado_meu} n\n")
            break
        
        # Mostra informações do estado
        num_cachorros = estado.contar_cachorros()
        pos_onca = estado.posicao_onca()
        print(f"Cachorros restantes: {num_cachorros}", file=sys.stderr)
        print(f"Posição da onça: {pos_onca}", file=sys.stderr)
        
        movs_teste = estado.gerar_movimentos(lado_meu)
        print(f"DEBUG - Movimentos possíveis: {len(movs_teste)}", file=sys.stderr)
        
        # Busca o melhor movimento
        print(f"Buscando melhor movimento (profundidade={profundidade})...", file=sys.stderr)
        
        melhor_movimento = busca.melhor_movimento(estado, lado_meu)
        
        # Mostra estatísticas da busca
        stats = busca.obter_estatisticas()
        print(f"Nós explorados: {stats['nos_explorados']}", file=sys.stderr)
        print(f"Cortes alfa: {stats['cortes_alfa']}", file=sys.stderr)
        print(f"Cortes beta: {stats['cortes_beta']}", file=sys.stderr)
        print(f"Tempo: {stats['tempo_decorrido']:.2f}s", file=sys.stderr)
        
        # Converte o movimento para string
        if melhor_movimento:
            movimento_str = estado.movimento_para_string(lado_meu, melhor_movimento)
            print(f"Movimento escolhido: {movimento_str}", file=sys.stderr)
        else:
            # Sem movimentos possíveis
            movimento_str = f"{lado_meu} n"
            print("Sem movimentos possíveis!", file=sys.stderr)
        
        # Envia o movimento
        tabuleiro.enviar(movimento_str + '\n')
        
        print("=" * 50, file=sys.stderr)

if __name__ == "__main__":
    main()
