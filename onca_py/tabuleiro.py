import redis
import sys

redis_client = None
lado_jogador = None

def conectar(args):
    global redis_client, lado_jogador
    if len(args) < 2:
        print("Formato: python tabuleiro.py lado [ip porta]")
        print("  lado: 'o' para onça, 'c' para cachorro")
        print("  ip: (opcional) IP do servidor redis (padrão: 127.0.0.1)")
        print("  porta: (opcional) Porta do servidor redis (padrão: 10001)")
        sys.exit(1)

    lado_jogador = args[1]
    ip = args[2] if len(args) > 2 else "127.0.0.1"
    porta = int(args[3]) if len(args) > 3 else 10001

    try:
        redis_client = redis.Redis(host=ip, port=porta, db=0)
        redis_client.ping()
    except redis.exceptions.ConnectionError as e:
        print(f"Erro ao conectar com o servidor redis: {e}")
        sys.exit(1)

def enviar(jogada):
    chave = f"jogada_{lado_jogador}"
    redis_client.rpush(chave, jogada)

def receber():
    chave = f"tabuleiro_{lado_jogador}"
    _, jogada = redis_client.blpop(chave)
    return jogada.decode('utf-8')
