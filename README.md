# Árvore de Natal ASCII 3D

## Versão web para compartilhar

A pasta `web` contém a versão para navegador, sem dependências ou etapa de compilação. Usa Canvas, geometria procedural, normais de superfície, iluminação direcional e brilho. Inclui pausa, reinício, compartilhamento e download de imagem, com layout responsivo e respeito à preferência por movimento reduzido. A distribuição dos pontos varia em relação ao Python, mantendo o mesmo estilo e sequência.

Para testar localmente: `python -m http.server 8000 --directory web` e abra http://localhost:8000. Na Vercel, importe este repositório; `vercel.json` define `web` como diretório público. Os arquivos Python continuam disponíveis na raiz.

## Versão 2 — iluminação

Luz direcional fixa acima e à esquerda. As normais (orientações das superfícies) giram com os objetos: cada face dos presentes recebe luz diferente, os ramos têm lado claro e lado escuro, e as bolas e fitas recebem reflexos. O interior dos ramos e a base das caixas são mais escuros. Lâmpadas emissivas e um halo suave de brilho completam o efeito. É iluminação estilizada, sem traçado de raios ou sombras projetadas entre objetos.

Recriação independente baseada no reel https://www.instagram.com/reel/DfoWsojSWA2/ de dwcminh.ascii. Não é o código original: o vídeo mostra apenas fragmentos. A geometria, animação e renderização deste pacote foram implementadas do zero.

## Executar

Instale Python 3.10 ou mais recente. Abra o terminal na pasta extraída e execute:

```powershell
python -m pip install -r requirements.txt
python christmas_tree.py
```

No Windows também pode abrir `iniciar.bat`. Na primeira execução ele instala as dependências, com acesso à internet.

## Visual e sequência

Fundo escuro, neve de caracteres, chão em perspectiva, árvore com ramos verdes e neve branca, rotação 3D contínua, festão dourado, bolas, lâmpadas piscando, presentes com fitas, estrela dourada e mensagem de Natal. A árvore aparece de baixo para cima; os enfeites surgem entre 6 e 9 segundos, presentes entre 9 e 11, estrela aos 12 e mensagem aos 13. Depois a cena continua girando.

Espaço pausa; R reinicia; S salva captura.png na pasta do script; Esc sai. Fechar a janela também encerra.

O código do editor exibido na parte inferior do reel não faz parte da animação. Esta versão não inclui a gravação musical. A disposição exata dos caracteres, fontes e objetos pode diferir da referência.

## Captura sem abrir janela

```powershell
python christmas_tree.py --capture preview.png --time 18.9
```

Altere COLS, ROWS, CW e CH no início do script para ajustar a resolução. As cores também ficam no início. A frase está em Animation.frame. Os objetos e tempos de surgimento ficam em build_scene.
