# Sistema de Monitoramento Ergonômico em Tempo Real

`PPC-CC: PUC Poços de Caldas - Ciência da Computação`
`Disciplina: Visão Computacional e Realidade Misturada`
`2021 - Semestre 1`

## Integrantes

- Gabriel Henrique Custodio
- João Eduardo Lino Quinteiro
- Vitor Hugo Granato Moreira do Prado

## Professor

- Will Ricardo dos Santos Machado

---

## Problema

No cenário contemporâneo de trabalho e estudo digital, a permanência prolongada e contínua de indivíduos em frente aos computadores gerou uma crise silenciosa relacionada à ergonomia e à saúde física. A falta de mecanismos automatizados e não invasivos para monitorar o comportamento dos usuários gera desafios críticos em três frentes principais:

* **Distúrbios Osteomusculares relacionados ao Trabalho (DORT):** Durante sessões extensas de uso do computador, os usuários frequentemente adotam posturas corporais nocivas de forma inconsciente — como a inclinação excessiva do tronco em direção à tela, desalinhamentos laterais, assimetria nos ombros e a posição corcunda. A ausência de alertas ou feedbacks instantâneos faz com que essas posições prejudiciais sejam mantidas por horas, resultando em dores crônicas, fadiga muscular e lesões a longo prazo.
* **Falta de Visibilidade sobre Produtividade e Foco:** Instituições de ensino e ambientes corporativos enfrentam dificuldades para mensurar, de forma passiva e precisa, o tempo real de engajamento e a permanência efetiva de estudantes ou colaboradores em frente às estações de trabalho. Os métodos tradicionais dependem de estimativas manuais falhas ou de métricas computacionais imprecisas (como a mera movimentação do mouse ou pressionar de teclas), que não refletem a real presença física do indivíduo.
* **Ausência de Validação Científica em Soluções de Rastreamento:** Grande parte das ferramentas comerciais ou experimentais de monitoramento de usuários carece de metodologias de validação estatística rigorosas integradas ao seu ciclo de uso. Isso torna complexo medir cientificamente a precisão e a confiabilidade de sistemas classificatórios quando expostos a ruídos do mundo real (como movimentos naturais e rápidos do cotidiano).

### Contexto de Aplicação

O ecossistema em que esse problema se manifesta compreende estações de trabalho e estudo convencionais em ambientes domésticos, acadêmicos ou corporativos. Do ponto de vista de infraestrutura e hardware, o cenário limita-se ao uso de dispositivos de captura de vídeo comuns e de baixo custo (webcams integradas ou periféricas via USB), sem a disponibilidade de sensores de profundidade caros ou estúdios de biometria dedicados. 

O contexto exige uma solução que atue em tempo real, respeite a privacidade do usuário e opere em segundo plano de forma totalmente passiva, sem interromper o fluxo de atenção do indivíduo com comandos intrusivos. Academicamente, a pesquisa se posiciona na intersecção entre a ergonomia do trabalho e o campo da Visão Computacional, demandando a aplicação de validação estatística para avaliar com rigor científico o comportamento observado.

---

## Objetivo

Este projeto consiste em um sistema inteligente de monitoramento postural e de presença utilizando Visão Computacional. Através da biblioteca **MediaPipe (Pose Landmarker)** e **OpenCV**, o sistema analisa a estrutura corporal do usuário em tempo real via webcam para identificar desvios ergonômicos comuns e acompanhar o tempo de foco do usuário.

O sistema também conta com uma ferramenta de validação analítica (Gabarito via teclado), permitindo gerar uma **Matriz de Confusão** e um **Relatório de Classificação** (`scikit-learn`) ao final de cada sessão para medir cientificamente a precisão do algoritmo.

---

## 🎯 Aplicações Possíveis

Com base nos recursos de monitoramento e análise de pose desenvolvidos, o sistema pode ser aplicado de forma prática nos seguintes cenários:

* **Controle de Produtividade:** Monitoramento automatizado do tempo de uso e análise aprofundada do comportamento do usuário dentro de ambientes computacionais corporativos ou acadêmicos.
* **Monitoramento de Tempo:** Medição de alta precisão do tempo real de permanência do usuário em frente ao computador, permitindo mapear e analisar padrões de uso ao longo do dia.
* **Análise de Comportamento:** Identificação detalhada de hábitos de uso e rotinas comportamentais estabelecidas pelo usuário durante as suas sessões focadas de trabalho ou estudo.
* **Detecção de Postura Inadequada:** Identificação instantânea e automatizada de posições corporais incorretas ou prejudiciais à saúde ergonômica durante o período de uso do computador.

---

## 🚀 Funcionalidades

* **Detecção Automática de Presença/Ausência:** Identifica se o usuário está em frente ao PC ou se a cadeira está vazia.
* **Calibração Anatômica Inicial:** Nos primeiros 30 frames, o sistema calcula uma média móvel da postura do usuário para adaptar os limites à sua anatomia e distância da câmera.
* **Filtro de Ruído Temporal (Delay de 3s):** Evita falsos positivos. Movimentos rápidos e naturais (como pegar uma garrafa de água ou se coçar) deixam o HUD em estado de *Aviso (Laranja)*. O alerta de *Postura Inadequada (Vermelho)* só é validado se o usuário permanecer na posição incorreta por mais de 3 segundos seguidos.
* **Análise Ergonômica:**
    * Postura Corcunda (baseada na distância proporcional entre ombros e olhos).
    * Tronco muito baixo (aproximação excessiva da tela).
    * Corpo desalinhado lateralmente.
    * Ombros inclinados/assimétricos.
* **Métricas Acadêmicas:** Gera automaticamente o relatório de classificação (`Precision`, `Recall`, `F1-Score`) e salva o gráfico da `Matriz de Confusão` em formato `.png` ao encerrar.

---

## ⚙️ Funcionamento do Sistema

O fluxo de execução do sistema baseia-se em quatro etapas principais operadas de forma contínua:

1. **Captura de Vídeo:** A webcam realiza a captura das imagens em tempo real utilizando a biblioteca OpenCV.
2. **Processamento:** Os frames capturados são convertidos para o espaço de cores RGB para que possam ser processados corretamente pelo MediaPipe.
3. **Detecção de Pose:** O algoritmo realiza a identificação automatizada de pontos-chave (*landmarks*) do corpo humano. Para otimização e escopo do projeto, o sistema foca estritamente nos marcos anatômicos superiores, detectando as posições do **nariz** e dos **ombros** do usuário.
4. **Exibição:** Um esqueleto virtual contendo as conexões anatômicas detectadas é desenhado sobre o corpo do usuário na interface gráfica.

---

## 🔧 Adaptações e customizações do Projeto

Para atender ao escopo ergonômico e de monitoramento em desktops, a implementação original foi customizada com as seguintes lógicas:

* **Foco na Parte Superior:** O algoritmo foi configurado para priorizar a análise de pontos relacionados à cabeça (como o nariz), ombros e cotovelos do usuário.
* **Detecção de Presença:** A presença do usuário em frente à estação de trabalho é validada apenas através da identificação simultânea dos pontos-chave com um nível mínimo de confiança estabelecido.
* **Contagem de Tempo:** O cronômetro de foco é iniciado automaticamente assim que a presença é detectada, sendo pausado instantaneamente no momento em que o usuário sai do campo de visão da webcam.
* **Exibição de Informações:** O tempo acumulado de permanência e os indicadores de estado são renderizados e exibidos em tempo real diretamente no HUD da tela de vídeo.

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:
* **Python** (Testado em versões a partir do 3.10; ambiente atual baseado no Python 3.14).
* Uma ou mais webcams conectadas (integrada, USB ou emuladores como DroidCam/Iriun).

---

## 🔧 Passo a Passo para Instalação e Execução

Siga as instruções abaixo para configurar e rodar o projeto em qualquer computador:

### 1. Clonar ou Baixar o Projeto
Baixe os arquivos do projeto para a máquina local e abra o terminal (ou prompt de comando) na pasta raiz do código.

### 2. Instalar as Dependências
Com o ambiente virtual ativo, instale todas as bibliotecas necessárias executando:

```bash
pip install opencv-python mediapipe numpy scikit-learn labels matplotlib
```

### 3. Baixar o Modelo do MediaPipe (.task)
O MediaPipe necessita do arquivo de pesos do modelo de Machine Learning para rodar localmente.

Arquivo oficial do Pose Landmarker presente nesse projeto, caso haja algum erro baixe o arquivo oficial do Pose Landmarker (versão Heavy ou Full) diretamente da documentação do MediaPipe.

Nomeie o arquivo ou garanta que ele possua a palavra pose no nome e a extensão .task (Exemplo: pose_landmarker_full.task).

Cole o arquivo baixado na mesma pasta onde o script sistema_tempo_real.py está localizado. O código buscará o modelo automaticamente.

### 4. Executar o Sistema
Agora basta iniciar o script principal:

```bash
python sistema_tempo_real.py
```

🎮 Comandos do Sistema (Mapeamento do Teclado)
Durante a execução da câmera, você pode interagir com o sistema usando o teclado para alimentar o gabarito real da Matriz de Confusão:

[1] -> Define o estado real atual como: POSTURA CORRETA

[2] -> Define o estado real atual como: POSTURA INCORRETA

[0] -> Define o estado real atual como: CADEIRA VAZIA / AUSENTE

[q] -> SAIR do sistema, encerrar a câmera e gerar automaticamente os gráficos e relatórios na tela.

---

### 5. Criar e Ativar o Ambiente Virtual (venv)
Caso haja conflito entre as dependências isoladas e versões, crie e ative um ambiente virtual executando os comandos abaixo:

**No Windows:**
```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
venv\Scripts\activate

# Executar
python sistema_tempo_real.py
```
---

## Links de Implementação de Referência
O projeto utilizará como base a seguinte implementação disponível publicamente:

Repositório GitHub:
```bash
https://github.com/devDurgeshK/poseEstimationModule
```
Vídeo de apoio:

```bash
https://www.youtube.com/watch?v=riuU9uH7av8
```
---
