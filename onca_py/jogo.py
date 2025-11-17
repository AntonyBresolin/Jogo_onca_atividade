"""
Módulo de modelagem do Jogo da Onça como problema de busca adversarial.
Implementa a representação do estado do jogo, geração de movimentos e validação.
"""

class EstadoJogo:
    """Representa o estado do jogo da Onça"""
    
    # Adjacências do tabuleiro - mapa de posições válidas e suas conexões
    ADJACENCIAS = {
        (1, 1): [(1, 2), (2, 1), (2, 2)],
        (1, 2): [(1, 1), (1, 3), (2, 1), (2, 2), (2, 3)],
        (1, 3): [(1, 2), (1, 4), (2, 2), (2, 3), (2, 4)],
        (1, 4): [(1, 3), (1, 5), (2, 3), (2, 4), (2, 5)],
        (1, 5): [(1, 4), (2, 4), (2, 5)],
        
        (2, 1): [(1, 1), (1, 2), (2, 2), (3, 1), (3, 2)],
        (2, 2): [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)],
        (2, 3): [(1, 2), (1, 3), (1, 4), (2, 2), (2, 4), (3, 2), (3, 3), (3, 4)],
        (2, 4): [(1, 3), (1, 4), (1, 5), (2, 3), (2, 5), (3, 3), (3, 4), (3, 5)],
        (2, 5): [(1, 4), (1, 5), (2, 4), (3, 4), (3, 5)],
        
        (3, 1): [(2, 1), (2, 2), (3, 2), (4, 1), (4, 2)],
        (3, 2): [(2, 1), (2, 2), (2, 3), (3, 1), (3, 3), (4, 1), (4, 2), (4, 3)],
        (3, 3): [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)],
        (3, 4): [(2, 3), (2, 4), (2, 5), (3, 3), (3, 5), (4, 3), (4, 4), (4, 5)],
        (3, 5): [(2, 4), (2, 5), (3, 4), (4, 4), (4, 5)],
        
        (4, 1): [(3, 1), (3, 2), (4, 2), (5, 1), (5, 2)],
        (4, 2): [(3, 1), (3, 2), (3, 3), (4, 1), (4, 3), (5, 1), (5, 2), (5, 3)],
        (4, 3): [(3, 2), (3, 3), (3, 4), (4, 2), (4, 4), (5, 2), (5, 3), (5, 4)],
        (4, 4): [(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), (5, 5)],
        (4, 5): [(3, 4), (3, 5), (4, 4), (5, 4), (5, 5)],
        
        (5, 1): [(4, 1), (4, 2), (5, 2)],
        (5, 2): [(4, 1), (4, 2), (4, 3), (5, 1), (5, 3), (6, 2)],
        (5, 3): [(4, 2), (4, 3), (4, 4), (5, 2), (5, 4), (6, 2), (6, 3), (6, 4)],
        (5, 4): [(4, 3), (4, 4), (4, 5), (5, 3), (5, 5), (6, 4)],
        (5, 5): [(4, 4), (4, 5), (5, 4)],
        
        (6, 2): [(5, 2), (5, 3), (6, 3), (7, 1)],
        (6, 3): [(5, 3), (6, 2), (6, 4), (7, 1), (7, 3), (7, 5)],
        (6, 4): [(5, 3), (5, 4), (6, 3), (7, 5)],
        
        (7, 1): [(6, 2), (6, 3), (7, 3)],
        (7, 3): [(6, 2), (6, 3), (6, 4), (7, 1), (7, 5)],
        (7, 5): [(6, 3), (6, 4), (7, 3)],
    }
    
    def __init__(self, tabuleiro_str=None):
        """Inicializa o estado do jogo a partir de uma string do tabuleiro"""
        if tabuleiro_str is None:
            # Tabuleiro inicial
            self.tabuleiro = self._tabuleiro_inicial()
        else:
            self.tabuleiro = self._parse_tabuleiro(tabuleiro_str)
    
    def _tabuleiro_inicial(self):
        """Retorna o tabuleiro na configuração inicial"""
        tab = {}
        # Cachorros iniciais
        for l in range(1, 4):
            for c in range(1, 6):
                if (l, c) in self.ADJACENCIAS:
                    tab[(l, c)] = 'c'
        # Onça no centro
        tab[(3, 3)] = 'o'
        
        # Posições vazias
        for l in range(4, 8):
            for c in range(1, 6):
                if (l, c) in self.ADJACENCIAS:
                    tab[(l, c)] = '-'
        
        return tab
    
    def _parse_tabuleiro(self, tabuleiro_str):
        """Converte string do tabuleiro para dicionário"""
        tab = {}
        linhas = tabuleiro_str.strip().split('\n')
        
        for l_idx, linha in enumerate(linhas):
            if l_idx == 0 or l_idx >= 8:  # Ignora bordas
                continue
            
            l = l_idx  # linha 1-7
            c = 1  # coluna começa em 1
            
            for char in linha:
                if char == '#':  # Ignora bordas
                    continue
                elif char in ['o', 'c', '-', ' ']:
                    if (l, c) in self.ADJACENCIAS:
                        if char == ' ':
                            tab[(l, c)] = '-'
                        else:
                            tab[(l, c)] = char
                    c += 1
        
        return tab
    
    def copiar(self):
        """Cria uma cópia do estado atual"""
        novo = EstadoJogo()
        novo.tabuleiro = self.tabuleiro.copy()
        return novo
    
    def contar_cachorros(self):
        """Conta quantos cachorros ainda estão no tabuleiro"""
        return sum(1 for peca in self.tabuleiro.values() if peca == 'c')
    
    def posicao_onca(self):
        """Retorna a posição da onça"""
        for pos, peca in self.tabuleiro.items():
            if peca == 'o':
                return pos
        return None
    
    def posicoes_cachorros(self):
        """Retorna lista de posições dos cachorros"""
        return [pos for pos, peca in self.tabuleiro.items() if peca == 'c']
    
    def eh_terminal(self):
        """Verifica se o estado é terminal (alguém ganhou)"""
        if self.contar_cachorros() <= 9:
            return True
        
        movs_onca = self.gerar_movimentos('o')
        if not movs_onca:
            return True
        
        return False
    
    def vencedor(self):
        """Retorna o vencedor ('o', 'c') ou None se não há vencedor ainda"""
        if self.contar_cachorros() <= 9:
            return 'o'
        
        if not self.gerar_movimentos('o'):
            return 'c'
        
        return None
    
    def gerar_movimentos(self, lado):
        """Gera todos os movimentos possíveis para um lado"""
        if lado == 'o':
            return self._gerar_movimentos_onca()
        else:
            return self._gerar_movimentos_cachorros()
    
    def _gerar_movimentos_cachorros(self):
        """Gera todos os movimentos possíveis para os cachorros"""
        movimentos = []
        
        for pos in self.posicoes_cachorros():
            l, c = pos
            for vizinho in self.ADJACENCIAS.get(pos, []):
                if self.tabuleiro.get(vizinho) == '-':
                    lv, cv = vizinho
                    distl, distc = abs(l - lv), abs(c - cv)
                    
                    if (l + c) % 2 != 0 and (distl + distc) > 1:
                        continue
                    
                    movimentos.append(('m', [(l, c), vizinho]))
        
        return movimentos
    
    def _gerar_movimentos_onca(self):
        """Gera todos os movimentos possíveis para a onça"""
        movimentos = []
        pos_onca = self.posicao_onca()
        
        if not pos_onca:
            return movimentos
        
        l, c = pos_onca
        
        for vizinho in self.ADJACENCIAS.get(pos_onca, []):
            if self.tabuleiro.get(vizinho) == '-':
                lv, cv = vizinho
                distl, distc = abs(l - lv), abs(c - cv)
                
                if (l + c) % 2 != 0 and (distl + distc) > 1:
                    continue 
                
                movimentos.append(('m', [(l, c), vizinho]))
        
        saltos = self._gerar_saltos_recursivos(pos_onca, set(), [pos_onca])
        movimentos.extend(saltos)
        
        return movimentos
    
    def _gerar_saltos_recursivos(self, pos_atual, capturados, caminho):
        """Gera saltos recursivos da onça (pode capturar múltiplos cachorros)"""
        saltos = []
        l, c = pos_atual
        
        for vizinho in self.ADJACENCIAS.get(pos_atual, []):
            lv, cv = vizinho
            
            if self.tabuleiro.get(vizinho) != 'c':
                continue
            
            if vizinho in capturados:
                continue
            
            dl, dc = lv - l, cv - c
            destino = (lv + dl, cv + dc)
            
            if destino not in self.ADJACENCIAS:
                continue
            if self.tabuleiro.get(destino) != '-':
                continue
            
            if not self._salto_valido(pos_atual, vizinho, destino):
                continue
            
            novo_caminho = caminho + [destino]
            novos_capturados = capturados | {vizinho}
            
            saltos.append(('s', novo_caminho.copy()))
            
            saltos_continuados = self._gerar_saltos_recursivos(
                destino, novos_capturados, novo_caminho
            )
            saltos.extend(saltos_continuados)
        
        return saltos
    
    def _salto_valido(self, origem, meio, destino):
        """
        Verifica se um salto é geometricamente válido
        IMPORTANTE: Segue a lógica do controlador.py, que tem limitações específicas
        """
        lo, co = origem
        lm, cm = meio
        ld, cd = destino
        
        if lm != (lo + ld) // 2 or cm != (co + cd) // 2:
            return False
        
        distl = abs(ld - lo)
        distc = abs(cd - co)
        
        if lo == 7 and ld == 7:
            return distc == 4 and distl == 0
        
        if distl == 2 and distc == 2:
            if (lo + co) % 2 != 0:
                return False
            if lo == 5 and ld == 7 and co != 3:
                return False
            if lo == 6 and ld == 4:
                if (co == 2 and cd != 4) or (co == 4 and cd != 2):
                    return False
            if ld == 7 and cd != 3:
                return False
            return True
        
        return False
    
    def aplicar_movimento(self, lado, movimento):
        """Aplica um movimento e retorna um novo estado"""
        novo_estado = self.copiar()
        tipo, posicoes = movimento
        
        if tipo == 'm':
            origem, destino = posicoes
            novo_estado.tabuleiro[origem] = '-'
            novo_estado.tabuleiro[destino] = lado
        
        elif tipo == 's':
            origem = posicoes[0]
            novo_estado.tabuleiro[origem] = '-'
            
            for i in range(1, len(posicoes)):
                pos_anterior = posicoes[i - 1]
                pos_atual = posicoes[i]
                
                lp, cp = pos_anterior
                la, ca = pos_atual
                lm, cm = (lp + la) // 2, (cp + ca) // 2
                
                novo_estado.tabuleiro[(lm, cm)] = '-'
            
            destino = posicoes[-1]
            novo_estado.tabuleiro[destino] = 'o'
        
        return novo_estado
    
    def movimento_para_string(self, lado, movimento):
        """Converte um movimento para o formato de string esperado"""
        tipo, posicoes = movimento
        
        if tipo == 'm':
            origem, destino = posicoes
            lo, co = origem
            ld, cd = destino
            return f"{lado} m {lo} {co} {ld} {cd}"
        
        elif tipo == 's':
            num_saltos = len(posicoes) - 1
            coords = ' '.join(f"{l} {c}" for l, c in posicoes)
            return f"{lado} s {num_saltos} {coords}"
        
        return f"{lado} n"
    
    def para_string(self):
        """Converte o estado para string no formato do controlador"""
        linhas = []
        linhas.append("#######")
        
        for l in range(1, 8):
            linha = "#"
            for c in range(1, 6):
                if (l, c) in self.tabuleiro:
                    linha += self.tabuleiro[(l, c)]
                else:
                    if l == 6 and c in [1, 5]:
                        linha += " "
                    elif l == 7 and c in [2, 4]:
                        linha += " "
                    else:
                        linha += "-"
            linha += "#"
            linhas.append(linha)
        
        linhas.append("#######")
        return "\n".join(linhas) + "\n"
    
    def hash_posicao(self):
        """Retorna um hash único da posição do tabuleiro para detectar repetições"""
        posicoes_ordenadas = tuple(sorted(
            (pos, peca) for pos, peca in self.tabuleiro.items() if peca != '-'
        ))
        return hash(posicoes_ordenadas)
