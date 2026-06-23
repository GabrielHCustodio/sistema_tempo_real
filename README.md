# Sistema de Monitoramento Ergonômico em Tempo Real (PUC-MG)

Este projeto consiste em um sistema inteligente de monitoramento postural e de presença utilizando Visão Computacional. Através da biblioteca **MediaPipe (Pose Landmarker)** e **OpenCV**, o sistema analisa a estrutura corporal do usuário em tempo real via webcam para identificar desvios ergonômicos comuns e acompanhar o tempo de foco do usuário.

O sistema também conta com uma ferramenta de validação analítica (Gabarito via teclado), permitindo gerar uma **Matriz de Confusão** e um **Relatório de Classificação** (`scikit-learn`) ao final de cada sessão para medir cientificamente a precisão do algoritmo.

---

## 🚀 Funcionalidades

* **Detecção Automática de Presença/Ausência:** Identifica se o usuário está em frente ao PC ou se a cadeira está vazia.
* **Calibração Anatômica Inicial:** Nos primeiros 30 frames, o sistema calcula uma média móvel da postura do usuário para adaptar os limites à sua anatomia e distância da câmera.
* **Filtro de Ruído Temporal (Delay de 5s):** Evita falsos positivos. Movimentos rápidos e naturais (como pegar uma garrafa de água ou se coçar) deixam o HUD em estado de *Aviso (Laranja)*. O alerta de *Postura Inadequada (Vermelho)* só é validado se o usuário permanecer na posição incorreta por mais de 5 segundos seguidos.
* **Análise Ergonômica:**
    * Postura Corcunda (baseada na distância proporcional entre ombros e olhos).
    * Tronco muito baixo (aproximação excessiva da tela).
    * Corpo desalinhado lateralmente.
    * Ombros inclinados/assimétricos.
* **Métricas Acadêmicas:** Gera automaticamente o relatório de classificação (`Precision`, `Recall`, `F1-Score`) e salva o gráfico da `Matriz de Confusão` em formato `.png` ao encerrar.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:
* **Python 3.9, 3.10 ou 3.11** (Recomendado: Python 3.10).
* Uma webcam conectada (ou aplicativo de emulação como DroidCam/Iriun).

---

## 🔧 Passo a Passo para Instalação e Execução

Siga as instruções abaixo para configurar e rodar o projeto em qualquer computador:

### 1. Clonar ou Baixar o Projeto
Baixe os arquivos do projeto para a máquina local e abra o terminal (ou prompt de comando) na pasta raiz do código.

### 2. Criar e Ativar um Ambiente Virtual (Recomendado)
Para evitar conflitos com outras bibliotecas do seu computador, crie um ambiente isolado:

**No Windows:**
```bash
python -m venv venv
venv\Scripts\activate
No Linux/macOS:

Bash
python3 -m venv venv
source venv/bin/activate
3. Instalar as Dependências
Com o ambiente virtual ativo, instale todas as bibliotecas necessárias executando:

Bash
pip install opencv-python mediapipe numpy scikit-learn labels matplotlib
4. Baixar o Modelo do MediaPipe (.task)
O MediaPipe necessita do arquivo de pesos do modelo de Machine Learning para rodar localmente.

Baixe o arquivo oficial do Pose Landmarker (versão Heavy ou Full) diretamente da documentação do MediaPipe.

Nomeie o arquivo ou garanta que ele possua a palavra pose no nome e a extensão .task (Exemplo: pose_landmarker_full.task).

Cole o arquivo baixado na mesma pasta onde o script sistema_tempo_real.py está localizado. O código buscará o modelo automaticamente.

5. Executar o Sistema
Agora basta iniciar o script principal:

Bash
python sistema_tempo_real.py
🎮 Comandos do Sistema (Mapeamento do Teclado)
Durante a execução da câmera, você pode interagir com o sistema usando o teclado para alimentar o gabarito real da Matriz de Confusão:

[1] -> Define o estado real atual como: POSTURA CORRETA

[2] -> Define o estado real atual como: POSTURA INCORRETA

[0] -> Define o estado real atual como: CADEIRA VAZIA / AUSENTE

[q] -> SAIR do sistema, encerrar a câmera e gerar automaticamente os gráficos e relatórios na tela.


---

Se precisar de qualquer ajuste no texto ou quiser adicionar mais algum detalhe técnico so