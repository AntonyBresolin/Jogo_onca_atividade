# Jogo da Onça - IA com Minimax

Implementação de IA para o Jogo da Onça usando algoritmo Minimax com poda Alfa-Beta.

## 🛠️ Ferramentas Necessárias

- **Windows**
- **Docker Desktop**
- **Python 3.12+**

## 📦 Instalação

1. **Clone/baixe o projeto**

2. **Instale as dependências Python:**
```bash
pip install -r onca_py/requirements.txt
```

3. **Inicie o servidor Redis:**
```bash
docker-compose up -d
```

## 🎮 Como Jogar

### IA vs IA (Assistir)
```bash
JOGAR_IA_VS_IA.bat
```
Abre 3 janelas: Controlador, IA Onça, IA Cachorros

### Você vs IA
```bash
JOGAR_IA_VS_PLAYER.bat
```
- Digite `1` para jogar como Onça
- Digite `2` para jogar como Cachorros

## 📝 Formato dos Movimentos

**Movimento Simples:**
```
m 3 3 4 3
```
Move de (linha 3, col 3) para (linha 4, col 3)

**Salto/Captura (apenas Onça):**
```
s 1 4 3 6 3
```
Salta de (4,3) para (6,3), capturando cachorro

**Passar:**
```
n
```

## 🏆 Regras

**Onça:** Capture 5+ cachorros para vencer

**Cachorros:** Cerque a onça (sem movimentos) para vencer

## 🗂️ Estrutura do Projeto

```
├── docker-compose.yml          # Configuração Redis
├── JOGAR_IA_VS_IA.bat         # Executar IA vs IA
├── JOGAR_IA_VS_PLAYER.bat     # Executar Player vs IA
├── TUTORIAL_PLAYER.txt        # Guia detalhado
├── LEIA-ME.txt               # Documentação completa
└── onca_py/
    ├── controlador.py         # Controlador do jogo
    ├── tabuleiro.py          # Interface Redis
    ├── jogo.py               # Lógica do jogo
    ├── busca.py              # Minimax + Alpha-Beta
    ├── ia_jogador.py         # IA Player
    ├── player_humano.py      # Player humano interativo
    └── requirements.txt      # Dependências
```

## ⚙️ Configuração da IA

Edite `onca_py/ia_jogador.py` (linhas 23-24):

```python
profundidade = 5        # Níveis de busca (4-6 recomendado)
tempo_limite = 30       # Segundos por jogada
```

## 🐛 Troubleshooting

**Erro de conexão Redis:**
```bash
docker-compose down
docker-compose up -d
```

**Jogo não inicia:**
- Aguarde 2-3 segundos entre abrir as janelas
- Certifique-se que o Redis está rodando

## 📊 Algoritmo

- **Minimax** com poda Alfa-Beta
- **Profundidade:** 5 níveis
- **Exploração:** 8.000 - 50.000 nós por jogada
- **Heurísticas:** Capturas, mobilidade, posicionamento

## 📄 Licença

Projeto acadêmico - Implementação de IA para Jogos

Antony Henrique Bresolin