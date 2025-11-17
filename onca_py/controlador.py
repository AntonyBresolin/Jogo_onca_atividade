import redis
import sys
import time

MAXSTR = 512
MAXINT = 16
OUTRO = lambda l: 'c' if l == 'o' else 'o'
POS = lambda l, c: (l) * 8 + (c)
ABS = lambda x: abs(x)

def inicia(args):
    if len(args) < 4:
        print("Formato: python controlador.py lado jogadas tempo [ip porta]")
        print("  lado: 'o' ou 'c' para indicar quem começa")
        print("  jogadas: número máximo de jogadas")
        print("  tempo: limite em segundos por jogada (0 para sem limite)")
        print("  ip: (opcional) IP do servidor redis (padrão: 127.0.0.1)")
        print("  porta: (opcional) Porta do servidor redis (padrão: 10001)")
        sys.exit(1)

    lado = args[1]
    jogadas = int(args[2])
    tempo = args[3]
    ip = args[4] if len(args) > 4 else "127.0.0.1"
    porta = int(args[5]) if len(args) > 5 else 10001

    try:
        redis_context = redis.Redis(host=ip, port=porta, db=0)
        redis_context.ping()
    except redis.exceptions.ConnectionError as e:
        print(f"Erro ao conectar com o servidor redis: {e}")
        sys.exit(1)
    
    return redis_context, lado, jogadas, tempo

def parse(jogada_str):
    parts = jogada_str.strip().split()
    if not parts:
        return None, None, None, None, None
    
    lado = parts[0]
    tipo = parts[1]
    
    if lado not in ['c', 'o'] or tipo not in ['n', 'm', 's']:
        return None, None, None, None, None

    mov_l, mov_c = [], []
    num_mov = 0
    
    if tipo == 'm':
        num_mov = 1
        try:
            for i in range(2, 6, 2):
                mov_l.append(int(parts[i]))
                mov_c.append(int(parts[i+1]))
        except (ValueError, IndexError):
            return None, None, None, None, None
    elif tipo == 's':
        try:
            num_mov = int(parts[2])
            if num_mov < 1: return None, None, None, None, None
            
            idx = 3
            for _ in range(num_mov + 1):
                mov_l.append(int(parts[idx]))
                mov_c.append(int(parts[idx+1]))
                idx += 2
        except (ValueError, IndexError):
            return None, None, None, None, None
            
    return lado, tipo, num_mov, mov_l, mov_c

def pos_valida(l, c):
    if not (1 <= l <= 7 and 1 <= c <= 5): return False
    if l == 6 and c in [1, 5]: return False
    if l == 7 and c in [2, 4]: return False
    return True

def mov_possivel(tipo, lo, co, ld, cd):
    if not pos_valida(lo, co) or not pos_valida(ld, cd): return False
    
    distl, distc = ABS(lo - ld), ABS(co - cd)
    if distl == 0 and distc == 0: return False

    if tipo == 'm':
        if lo == 7 and distl == 0: return distc == 2
        if distl > 1 or distc > 1: return False
        if (lo + co) % 2 != 0 and (distl + distc) > 1: return False
        if lo == 5 and ld == 6 and co != 3: return False
        if lo == 6 and co % 2 == 0:
            if ld == 5 and cd != 3: return False
            if ld == 7 and cd == 3: return False
        return True
    elif tipo == 's':
        if lo == 7 and distl == 0: return distc == 4
        if distl in [0, 1] or distc in [0, 1] or (distl + distc) > 4: return False
        if (lo + co) % 2 != 0 and (distl + distc) > 2: return False
        if lo == 5 and ld == 7 and co != 3: return False
        if lo == 6 and ld == 4 and ((co == 2 and cd != 4) or (co == 4 and cd != 2)): return False
        if lo == 7 and cd != 3: return False
        return True
        
    return False

def aplica(tabuleiro, lado, tipo, num_mov, mov_l, mov_c):
    tab_list = list(tabuleiro)
    
    if tipo == 'n': return "".join(tab_list)

    if tipo == 'm':
        l, c, ln, cn = mov_l[0], mov_c[0], mov_l[1], mov_c[1]
        if not mov_possivel('m', l, c, ln, cn): return None
        
        p, pn = POS(l, c), POS(ln, cn)
        if tab_list[p] != lado or tab_list[pn] != '-': return None
        
        tab_list[p], tab_list[pn] = '-', lado
    else: # tipo 's'
        if lado != 'o': return None
        l, c = mov_l[0], mov_c[0]
        p = POS(l, c)
        if tab_list[p] != 'o': return None

        for i in range(1, num_mov + 1):
            ln, cn = mov_l[i], mov_c[i]
            if not mov_possivel('s', l, c, ln, cn): return None
            
            pn = POS(ln, cn)
            if tab_list[pn] != '-': return None
            
            lm, cm = (l + ln) // 2, (c + cn) // 2
            pm = POS(lm, cm)
            if tab_list[pm] != 'c': return None
            
            tab_list[p], tab_list[pm], tab_list[pn] = '-', '-', 'o'
            l, c, p = ln, cn, pn
            
    return "".join(tab_list)

def vitoria(lado, tab):
    if lado == 'o':
        return tab.count('c') <= 9
    else: # lado 'c'
        for l in range(1, 8):
            for c in range(1, 6):
                if tab[POS(l, c)] == 'o':
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if mov_possivel('m', l, c, l + i, c + j) and tab[POS(l + i, c + j)] == '-':
                                return False
                            if mov_possivel('s', l, c, l + 2*i, c + 2*j) and \
                               tab[POS(l + i, c + j)] == 'c' and tab[POS(l + 2*i, c + 2*j)] == '-':
                                return False
        return True
    return False

def main():
    c, quem_joga, num_jogadas, timeout_str = inicia(sys.argv)
    timeout = int(timeout_str) if timeout_str != "0" else None
    
    vencedor = ' '
    tabuleiro = ("#######\n"
                 "#ccccc#\n"
                 "#ccccc#\n"
                 "#ccocc#\n"
                 "#-----#\n"
                 "#-----#\n"
                 "# --- #\n"
                 "#- - -#\n"
                 "#######\n")

    print(f"{num_jogadas}:\n{tabuleiro}")

    buffer = f"{quem_joga}\n{OUTRO(quem_joga)} n\n{tabuleiro}"

    while num_jogadas > 0:
        chave = f"tabuleiro_{quem_joga}"
        c.ltrim(chave, 1, 0)
        c.rpush(chave, buffer)

        ok = False
        chave_jogada = f"jogada_{quem_joga}"
        
        try:
            _, jogada_bytes = c.blpop(chave_jogada, timeout=timeout)
            jogada = jogada_bytes.decode('utf-8')
            
            lado_p, tipo_mov, num_mov, mov_l, mov_c = parse(jogada)
            
            if lado_p and quem_joga == lado_p:
                novo_tabuleiro = aplica(tabuleiro, lado_p, tipo_mov, num_mov, mov_l, mov_c)
                if novo_tabuleiro:
                    tabuleiro = novo_tabuleiro
                    ok = True
        except TypeError: # blpop returns None on timeout
            jogada = f"{quem_joga} n"

        if not ok:
            jogada = f"{quem_joga} n"

        print(f"{num_jogadas}: {jogada.strip()}")
        print(tabuleiro)

        if vitoria(quem_joga, tabuleiro):
            print(f"{num_jogadas}: vitória de {quem_joga}")
            vencedor = quem_joga
            break

        quem_joga = OUTRO(quem_joga)
        buffer = f"{quem_joga}\n{jogada.strip()}\n{tabuleiro}"
        num_jogadas -= 1

    buffer_o = f"o\nc n\n{tabuleiro}"
    c.rpush("tabuleiro_o", buffer_o)
    
    buffer_c = f"c\no n\n{tabuleiro}"
    c.rpush("tabuleiro_c", buffer_c)

    if num_jogadas == 0:
        print("empate")
    else:
        print(f"vencedor: {vencedor}")

if __name__ == "__main__":
    main()
