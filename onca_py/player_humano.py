import sys
import tabuleiro

def mostrar_tutorial(lado):
    print("\n" + "═" * 70)
    print("                    TUTORIAL - COMO JOGAR")
    print("═" * 70)
    
    print("\n📋 FORMATO DOS MOVIMENTOS:\n")
    
    print("1️⃣  MOVIMENTO SIMPLES (m):")
    print("   Sintaxe: m linha_origem coluna_origem linha_destino coluna_destino")
    print("   Exemplo: m 3 3 4 3")
    print("   ➜ Move sua peça de (linha 3, coluna 3) para (linha 4, coluna 3)\n")
    
    if lado == 'o':
        print("2️⃣  SALTO/CAPTURA (s) - Apenas para Onça:")
        print("   Sintaxe: s num_saltos linha1 col1 linha2 col2 ... linhaN colN")
        print("   Exemplo: s 1 4 3 6 3")
        print("   ➜ Onça em (4,3) SALTA para (6,3), capturando cachorro em (5,3)\n")
        
        print("   Salto Múltiplo:")
        print("   Exemplo: s 2 4 3 6 3 4 5")
        print("   ➜ Faz 2 saltos: (4,3)→(6,3)→(4,5), capturando 2 cachorros\n")
    
    print("3️⃣  PASSAR A VEZ (n):")
    print("   Sintaxe: n")
    print("   ➜ Use quando não houver movimentos válidos\n")
    
    print("═" * 70)
    print("\n🎯 DICAS:\n")
    print("• As LINHAS vão de 1 (topo) a 7 (base)")
    print("• As COLUNAS vão de 1 (esquerda) a 5 (direita)")
    print("• Observe o tabuleiro mostrado antes de cada jogada")
    print("• O símbolo 'o' = Onça, 'c' = Cachorro, '-' = Vazio")
    
    if lado == 'o':
        print("\n🐆 VOCÊ É A ONÇA:")
        print("• Capture 5+ cachorros para VENCER (deixar 9 ou menos)")
        print("• Você pode saltar sobre cachorros para capturá-los")
        print("• Pode fazer múltiplos saltos em sequência")
    else:
        print("\n🐕 VOCÊ É OS CACHORROS:")
        print("• Cerque a onça (sem movimentos) para VENCER")
        print("• Você NÃO pode capturar a onça")
        print("• Trabalhe em equipe para bloquear os caminhos da onça")
    
    print("\n" + "═" * 70 + "\n")
    input("Pressione ENTER para começar o jogo...")
    print("\n")

def mostrar_tabuleiro(tabuleiro_str):
    linhas = tabuleiro_str.strip().split('\n')
    
    print("\n" + "┌" + "─" * 68 + "┐")
    print("│" + " " * 22 + "TABULEIRO ATUAL" + " " * 31 + "│")
    print("├" + "─" * 68 + "┤")
    
    print("│      " + "     ".join([f"Col{i}" for i in range(1, 6)]) + "     │")
    print("│      " + "     ".join([f"  {i}  " for i in range(1, 6)]) + "     │")
    
    for idx, linha in enumerate(linhas):
        if idx == 0:
            print("│      " + linha + " " * 36 + "│")
        elif idx == 8:
            print("│      " + linha + " " * 36 + "│")
        else:
            linha_num = idx
            print(f"│ L{linha_num}   {linha}" + " " * 36 + "│")
    
    print("└" + "─" * 68 + "┘\n")

def validar_entrada(entrada, lado):
    partes = entrada.strip().split()
    
    if not partes:
        return False, "❌ Entrada vazia! Digite um movimento."
    
    tipo = partes[0]
    
    if tipo == 'n':
        return True, "✓ Movimento válido (passar a vez)"
    
    if tipo == 'm':
        if len(partes) != 5:
            return False, f"❌ Movimento simples precisa de 4 números: m linha_orig col_orig linha_dest col_dest"
        try:
            l1, c1, l2, c2 = int(partes[1]), int(partes[2]), int(partes[3]), int(partes[4])
            if not (1 <= l1 <= 7 and 1 <= c1 <= 5 and 1 <= l2 <= 7 and 1 <= c2 <= 5):
                return False, "❌ Posições devem estar entre: linhas 1-7, colunas 1-5"
            return True, "✓ Formato válido"
        except ValueError:
            return False, "❌ Use apenas números após 'm'"
    
    if tipo == 's':
        if lado != 'o':
            return False, "❌ Apenas a ONÇA pode fazer saltos/capturas!"
        if len(partes) < 4:
            return False, "❌ Salto precisa de: s num_saltos linha1 col1 linha2 col2 ..."
        try:
            num_saltos = int(partes[1])
            if len(partes) != 2 + (num_saltos + 1) * 2:
                return False, f"❌ Para {num_saltos} saltos, precisa de {(num_saltos + 1) * 2} coordenadas"
            return True, "✓ Formato válido"
        except ValueError:
            return False, "❌ Número de saltos deve ser um inteiro"
    
    return False, f"❌ Tipo de movimento inválido '{tipo}'. Use: m, s ou n"

def obter_movimento(lado):
    while True:
        print("─" * 70)
        if lado == 'o':
            prompt = "🐆 SUA JOGADA (Onça) > "
        else:
            prompt = "🐕 SUA JOGADA (Cachorros) > "
        
        entrada = input(prompt).strip().lower()
        
        valido, mensagem = validar_entrada(entrada, lado)
        if not valido:
            print(f"\n{mensagem}")
            print("💡 Digite 'ajuda' para ver exemplos\n")
            if entrada == 'ajuda':
                mostrar_exemplos(lado)
            continue
        
        print(f"{mensagem}\n")
        return entrada

def mostrar_exemplos(lado):
    print("\n" + "═" * 70)
    print("                      EXEMPLOS DE MOVIMENTOS")
    print("═" * 70 + "\n")
    
    print("MOVIMENTO SIMPLES:")
    print("  m 3 3 4 3    ➜ Move de (linha 3, col 3) para (linha 4, col 3)")
    print("  m 2 1 3 2    ➜ Move de (linha 2, col 1) para (linha 3, col 2)")
    print("  m 4 3 4 4    ➜ Move de (linha 4, col 3) para (linha 4, col 4)\n")
    
    if lado == 'o':
        print("SALTO/CAPTURA (Onça):")
        print("  s 1 4 3 6 3      ➜ Salta de (4,3) para (6,3)")
        print("  s 2 4 3 6 3 4 5  ➜ Salta (4,3)→(6,3)→(4,5)\n")
    
    print("PASSAR A VEZ:")
    print("  n            ➜ Não move nenhuma peça\n")
    
    print("═" * 70 + "\n")

def main():
    tabuleiro.conectar(sys.argv)
    lado = tabuleiro.lado_jogador
    
    print("\n" + "╔" + "═" * 68 + "╗")
    if lado == 'o':
        print("║" + " " * 20 + "VOCÊ ESTÁ JOGANDO COMO ONÇA 🐆" + " " * 18 + "║")
    else:
        print("║" + " " * 17 + "VOCÊ ESTÁ JOGANDO COMO CACHORROS 🐕" + " " * 15 + "║")
    print("╚" + "═" * 68 + "╝")
    
    mostrar_tutorial(lado)
    
    contador_jogadas = 0
    
    while True:
        buf = tabuleiro.receber()
        parts = buf.split('\n', 2)
        lado_confirma = parts[0]
        mov_adv_str = parts[1]
        tabuleiro_str = parts[2]
        
        contador_jogadas += 1
        
        print("\n" + "╔" + "═" * 68 + "╗")
        print(f"║  JOGADA #{contador_jogadas:<4}" + " " * 57 + "║")
        print("╚" + "═" * 68 + "╝")
        
        if mov_adv_str.strip() != f"{lado} n":
            adv_lado = 'Onça' if lado == 'c' else 'Cachorros'
            print(f"\n🎮 Movimento do adversário ({adv_lado}): {mov_adv_str}")
        else:
            print(f"\n⏭️  Primeira jogada - você começa!")
        
        mostrar_tabuleiro(tabuleiro_str)
        movimento = obter_movimento(lado)
        movimento_formatado = f"{lado} {movimento}\n"
        tabuleiro.enviar(movimento_formatado)
        
        print("✅ Movimento enviado! Aguardando resposta...\n")

if __name__ == "__main__":
    main()
