"""
Módulo de busca adversarial - Implementa o algoritmo Minimax com podas Alfa-Beta
"""

import time
from jogo import EstadoJogo

class BuscaAdversarial:
    """Implementa busca Minimax com poda Alfa-Beta"""
    
    def __init__(self, profundidade_maxima=4, tempo_limite=None):
        """
        Inicializa o algoritmo de busca
        
        Args:
            profundidade_maxima: Profundidade máxima da árvore de busca
            tempo_limite: Tempo limite em segundos (None = sem limite)
        """
        self.profundidade_maxima = profundidade_maxima
        self.tempo_limite = tempo_limite
        self.inicio_busca = None
        self.nos_explorados = 0
        self.cortes_alfa = 0
        self.cortes_beta = 0
    
    def tempo_esgotado(self):
        """Verifica se o tempo limite foi atingido"""
        if self.tempo_limite is None:
            return False
        return (time.time() - self.inicio_busca) >= self.tempo_limite
    
    def melhor_movimento(self, estado, lado):
        """
        Encontra o melhor movimento usando Minimax com poda Alfa-Beta
        
        Args:
            estado: EstadoJogo atual
            lado: 'o' ou 'c'
        
        Returns:
            Tupla (tipo, posicoes) representando o melhor movimento
        """
        self.inicio_busca = time.time()
        self.nos_explorados = 0
        self.cortes_alfa = 0
        self.cortes_beta = 0
        
        # Usa busca iterativa por profundidade crescente
        melhor_mov = None
        melhor_valor = float('-inf')
        
        # Tenta com profundidades crescentes
        for prof in range(1, self.profundidade_maxima + 1):
            if self.tempo_esgotado():
                break
            
            movimentos = estado.gerar_movimentos(lado)
            
            if not movimentos:
                return None
            
            # Ordena movimentos para melhorar poda (capturas primeiro para onça)
            movimentos = self._ordenar_movimentos(estado, lado, movimentos)
            
            alfa = float('-inf')
            beta = float('+inf')
            
            for movimento in movimentos:
                if self.tempo_esgotado():
                    break
                
                novo_estado = estado.aplicar_movimento(lado, movimento)
                
                # Minimax com poda alfa-beta
                valor = self._minimax(
                    novo_estado,
                    prof - 1,
                    alfa,
                    beta,
                    False,  # Próximo nível é MIN
                    lado
                )
                
                if valor > melhor_valor:
                    melhor_valor = valor
                    melhor_mov = movimento
                
                alfa = max(alfa, valor)
        
        return melhor_mov
    
    def _minimax(self, estado, profundidade, alfa, beta, maximizando, lado_max):
        """
        Algoritmo Minimax com poda Alfa-Beta
        
        Args:
            estado: Estado atual do jogo
            profundidade: Profundidade restante
            alfa: Valor alfa para poda
            beta: Valor beta para poda
            maximizando: True se é nó MAX, False se é MIN
            lado_max: Lado que está maximizando ('o' ou 'c')
        
        Returns:
            Valor heurístico do estado
        """
        self.nos_explorados += 1
        
        # Condições de parada
        if self.tempo_esgotado():
            return self._avaliar(estado, lado_max)
        
        if profundidade == 0 or estado.eh_terminal():
            return self._avaliar(estado, lado_max)
        
        lado_atual = lado_max if maximizando else ('c' if lado_max == 'o' else 'o')
        movimentos = estado.gerar_movimentos(lado_atual)
        
        # Se não há movimentos, avalia o estado
        if not movimentos:
            return self._avaliar(estado, lado_max)
        
        # Ordena movimentos para melhorar poda
        movimentos = self._ordenar_movimentos(estado, lado_atual, movimentos)
        
        if maximizando:
            valor = float('-inf')
            for movimento in movimentos:
                if self.tempo_esgotado():
                    break
                
                novo_estado = estado.aplicar_movimento(lado_atual, movimento)
                valor = max(valor, self._minimax(
                    novo_estado, profundidade - 1, alfa, beta, False, lado_max
                ))
                
                alfa = max(alfa, valor)
                if beta <= alfa:
                    self.cortes_beta += 1
                    break  # Poda Beta
            
            return valor
        else:
            valor = float('+inf')
            for movimento in movimentos:
                if self.tempo_esgotado():
                    break
                
                novo_estado = estado.aplicar_movimento(lado_atual, movimento)
                valor = min(valor, self._minimax(
                    novo_estado, profundidade - 1, alfa, beta, True, lado_max
                ))
                
                beta = min(beta, valor)
                if beta <= alfa:
                    self.cortes_alfa += 1
                    break  # Poda Alfa
            
            return valor
    
    def _ordenar_movimentos(self, estado, lado, movimentos):
        """
        Ordena movimentos para melhorar eficiência da poda
        Movimentos mais promissores primeiro
        """
        def prioridade(mov):
            tipo, posicoes = mov
            score = 0
            
            if lado == 'o':
                # Onça: prioriza capturas
                if tipo == 's':
                    num_capturas = len(posicoes) - 1
                    score += 1000 * num_capturas
                    
                    # Prioriza capturas múltiplas
                    if num_capturas > 1:
                        score += 500
                
                # Prioriza movimentos para o centro
                destino = posicoes[-1]
                ld, cd = destino
                dist_centro = abs(ld - 4) + abs(cd - 3)
                score -= dist_centro * 10
            
            else:  # Cachorros
                # Prioriza avançar (descer no tabuleiro)
                origem, destino = posicoes
                lo, co = origem
                ld, cd = destino
                
                if ld > lo:  # Avançando
                    score += 50
                
                # Prioriza movimentos em direção à onça
                pos_onca = estado.posicao_onca()
                if pos_onca:
                    ol, oc = pos_onca
                    dist_antes = abs(lo - ol) + abs(co - oc)
                    dist_depois = abs(ld - ol) + abs(cd - oc)
                    
                    if dist_depois < dist_antes:
                        score += 30
            
            return -score  # Negativo para ordenação decrescente
        
        return sorted(movimentos, key=prioridade)
    
    def _avaliar(self, estado, lado):
        """
        Função de avaliação heurística do estado
        
        Args:
            estado: Estado do jogo a avaliar
            lado: Lado que está maximizando
        
        Returns:
            Valor heurístico (positivo favorece 'lado', negativo favorece oponente)
        """
        # Verifica vitória
        vencedor = estado.vencedor()
        if vencedor == lado:
            return 10000
        elif vencedor is not None:
            return -10000
        
        if lado == 'o':
            return self._avaliar_onca(estado)
        else:
            return self._avaliar_cachorros(estado)
    
    def _avaliar_onca(self, estado):
        """Avalia o estado do ponto de vista da onça"""
        score = 0
        
        # 1. Número de cachorros capturados (mais importante)
        num_cachorros = estado.contar_cachorros()
        cachorros_capturados = 14 - num_cachorros
        score += cachorros_capturados * 500
        
        # Bônus se está perto de ganhar
        if num_cachorros <= 11:
            score += (11 - num_cachorros) * 200
        
        # 2. Mobilidade da onça (número de movimentos possíveis)
        movimentos_onca = estado.gerar_movimentos('o')
        score += len(movimentos_onca) * 10
        
        # 3. Posição central da onça
        pos_onca = estado.posicao_onca()
        if pos_onca:
            l, c = pos_onca
            # Favorece posições centrais e avançadas
            centralidade = 5 - abs(c - 3)  # Quanto mais perto da coluna 3, melhor
            avanco = l  # Quanto maior a linha, melhor (mais avançado)
            
            score += centralidade * 15
            score += avanco * 8
        
        # 4. Oportunidades de captura
        capturas_disponiveis = sum(1 for mov in movimentos_onca if mov[0] == 's')
        score += capturas_disponiveis * 100
        
        # Penaliza se está encurralada
        if len(movimentos_onca) <= 2:
            score -= 100
        if len(movimentos_onca) == 0:
            score -= 5000
        
        # 5. Densidade de cachorros ao redor (menos é melhor para onça)
        if pos_onca:
            cachorros_proximos = 0
            for vizinho in EstadoJogo.ADJACENCIAS.get(pos_onca, []):
                if estado.tabuleiro.get(vizinho) == 'c':
                    cachorros_proximos += 1
            score -= cachorros_proximos * 20
        
        return score
    
    def _avaliar_cachorros(self, estado):
        """Avalia o estado do ponto de vista dos cachorros"""
        score = 0
        
        # 1. Número de cachorros vivos (preservar cachorros)
        num_cachorros = estado.contar_cachorros()
        score += num_cachorros * 300
        
        # Penaliza fortemente se perdeu muitos cachorros
        if num_cachorros <= 11:
            score -= (11 - num_cachorros) * 400
        
        # 2. Restrição de mobilidade da onça
        movimentos_onca = estado.gerar_movimentos('o')
        score += (20 - len(movimentos_onca)) * 50
        
        # Bônus grande se onça está imobilizada
        if len(movimentos_onca) == 0:
            score += 10000
        elif len(movimentos_onca) <= 2:
            score += 500
        
        # 3. Cerco à onça (cachorros próximos)
        pos_onca = estado.posicao_onca()
        if pos_onca:
            cachorros_proximos = 0
            posicoes_adjacentes_ocupadas = 0
            
            for vizinho in EstadoJogo.ADJACENCIAS.get(pos_onca, []):
                if estado.tabuleiro.get(vizinho) == 'c':
                    cachorros_proximos += 1
                    posicoes_adjacentes_ocupadas += 1
                elif estado.tabuleiro.get(vizinho) == 'o':
                    pass
                else:
                    posicoes_adjacentes_ocupadas += 0
            
            score += cachorros_proximos * 80
            
            # Bônus se está formando um cerco
            total_adjacentes = len(EstadoJogo.ADJACENCIAS.get(pos_onca, []))
            if total_adjacentes > 0:
                proporcao_cercada = cachorros_proximos / total_adjacentes
                score += proporcao_cercada * 200
        
        # 4. Formação defensiva (cachorros agrupados)
        posicoes_cachorros = estado.posicoes_cachorros()
        conexoes = 0
        for pos in posicoes_cachorros:
            for vizinho in EstadoJogo.ADJACENCIAS.get(pos, []):
                if estado.tabuleiro.get(vizinho) == 'c':
                    conexoes += 1
        score += conexoes * 5
        
        # 5. Posicionamento avançado dos cachorros
        for pos in posicoes_cachorros:
            l, c = pos
            if l >= 4:  # Cachorros nas linhas avançadas
                score += (l - 3) * 15
        
        return score
    
    def obter_estatisticas(self):
        """Retorna estatísticas da última busca"""
        return {
            'nos_explorados': self.nos_explorados,
            'cortes_alfa': self.cortes_alfa,
            'cortes_beta': self.cortes_beta,
            'tempo_decorrido': time.time() - self.inicio_busca if self.inicio_busca else 0
        }
