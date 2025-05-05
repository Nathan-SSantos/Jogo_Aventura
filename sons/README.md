Esta pasta contém todos os arquivos de áudio utilizados no jogo, como:

Música de fundo – Arquivo tocado durante o gameplay.
Efeitos sonoros – Sons para ações como ataque, coleta de moedas, dano, etc.

## Caminhos dos Arquivos
No código Python, os sons são carregados usando caminhos relativos. 
Isso significa que os arquivos devem estar exatamente dentro da pasta sons, que está no mesmo diretório do arquivo principal do jogo (main.py).

Exemplo de como o som é carregado no código:
coin_sound = pygame.mixer.Sound("C:/Users/Pc/Desktop/Jogo/sons/moeda.mp3")
pygame.mixer.music.load("C:/Users/Pc/Desktop/Jogo/sons/background.mp3") 

## Importante:
Não renomeie os arquivos de áudio sem atualizar os nomes no código.
Não mova os arquivos para fora da pasta sons, pois isso causará erro na hora de carregar os sons.
