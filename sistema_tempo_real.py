import cv2
import mediapipe as mp
import numpy as np
import time
import os
import sys
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay

# =====================================================================
# CONFIGURAÇÃO DE CAMINHO LOCAL E MODELO
# =====================================================================
pasta_atual = os.path.dirname(os.path.abspath(__file__))
modelo_encontrado = None
for arquivo in os.listdir(pasta_atual):
    if arquivo.endswith('.task') and 'pose' in arquivo.lower():
        modelo_encontrado = os.path.join(pasta_atual, arquivo)
        break

if not modelo_encontrado:
    print("\n[ERRO CRÍTICO] Arquivo .task não encontrado!")
    sys.exit()

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# FILTRO ANTI-FANTASMA
options = vision.PoseLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path=modelo_encontrado),
    running_mode=vision.RunningMode.IMAGE,
    min_pose_detection_confidence=0.70, 
    min_pose_presence_confidence=0.70   
)

# =====================================================================
# EXECUÇÃO DO SISTEMA VIA TECLADO
# =====================================================================
with vision.PoseLandmarker.create_from_options(options) as landmarker:
    
    # VARREDURA DE DISPOSITIVOS DE VÍDEO
    cameras_encontradas = []
    
    # Faz uma varredura inicial usando DirectShow para ser mais rápido
    for i in range(6): # Reduzi para 6 para ir ainda mais rápido no teste inicial
        test_cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if test_cap.isOpened():
            success, _ = test_cap.read()
            if success:
                cameras_encontradas.append(i)
            test_cap.release()

    if not cameras_encontradas:
        print("\n[ERRO CRÍTICO] Nenhuma câmera foi detectada pelo sistema!")
        sys.exit()

    # LÓGICA DE SELEÇÃO MANUAL
    if len(cameras_encontradas) > 1:
        print("\n" + "="*40)
        print(" [CONFIG] MÚLTIPLAS CÂMERAS DETECTADAS")
        print("="*40)
        for cam in cameras_encontradas:
            if cam == 0:
                tipo = "Webcam Nativa do Notebook"
            elif cam == 1:
                tipo = "Webcam Externa (USB)"
            elif cam == 2:
                tipo = "Conexão com a Câmera do Celular"
            else:
                tipo = "Outro Dispositivo de Vídeo"
            print(f"  Índice [{cam}] -> {tipo}")
        print("="*40)
        
        while True:
            try:
                escolha = int(input(f"\nDigite o número do índice que deseja usar {cameras_encontradas}: "))
                if escolha in cameras_encontradas:
                    indice_escolhido = escolha
                    break
                else:
                    print(f"[AVISO] Índice {escolha} inválido. Escolha um dos ativos.")
            except ValueError:
                print("[AVISO] Por favor, digite apenas números.")
    else:
        indice_escolhido = cameras_encontradas[0]
        print(f"\n[INFO] Apenas uma câmera detectada. Usando o índice padrão: {indice_escolhido}")

    # Inicializa a câmera usando DirectShow (CAP_DSHOW) para pular o delay do MSMF
    print(f"\n[INFO] Inicializando a câmera {indice_escolhido} de forma rápida...")
    cap = cv2.VideoCapture(indice_escolhido, cv2.CAP_DSHOW)
    
    # Configurações de imagem otimizadas para evitar travamentos
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    tempo_presente = 0.0
    tempo_ausente = 0.0
    ultimo_tempo = time.time()

    y_real = []
    y_predito = []
    
    classe_real_atual = 1 

    ref_nariz_x, ref_nariz_y, ref_dist_ombros_olhos = None, None, None
    frames_calibracao = 0

    # VARIÁVEIS PARA O DELAY DE FILTRO TEMPORAL
    tempo_inicio_desalinhado = None  
    TEMPO_LIMITE_ALERTA = 3.0        

    print("\n" + "="*50)
    print(" SISTEMA DE MONITORAMENTO ERGONÔMICO (PUC-MG)")
    print("="*50)
    print("A IA DETECTA A SUA POSTURA AUTOMATICAMENTE!")
    print("\nCOMANDOS DE TECLADO (Para calibrar a Matriz de Confusão):")
    print(" Aperte [1] -> Definir Real como: POSTURA CORRETA")
    print(" Aperte [2] -> Definir Real como: POSTURA INCORRETA")
    print(" Aperte [0] -> Definir Real como: CADEIRA VAZIA / AUSENTE")
    print(" Aperte [q] -> SAIR e gerar a Matriz de Confusão do Professor")
    print("="*50)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        tempo_atual = time.time()
        dt = tempo_atual - ultimo_tempo
        ultimo_tempo = tempo_atual

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        pose_landmarker_result = landmarker.detect(mp_image)

        classe_predita = 0 
        cor_hud = (0, 255, 0) 
        texto_postura = "POSTURA: SAUDAVEL (OK)"

        if pose_landmarker_result.pose_landmarks and pose_landmarker_result.pose_landmarks[0][0].visibility > 0.70:
            landmarks = pose_landmarker_result.pose_landmarks[0]
            classe_predita = 1 
            tempo_presente += dt
            
            h, w, _ = frame.shape
            nariz_x, nariz_y = landmarks[0].x, landmarks[0].y
            centro_olhos_y = (landmarks[2].y + landmarks[5].y) / 2.0
            dist_ombros_olhos_atual = (landmarks[11].y + landmarks[12].y) / 2.0 - centro_olhos_y

            # Desenho do esqueleto inteligente comercial (Apenas Ombro a Ombro e Rosto)
            cv2.line(frame, (int(landmarks[11].x * w), int(landmarks[11].y * h)), (int(landmarks[12].x * w), int(landmarks[12].y * h)), (255, 255, 255), 2)
            cv2.circle(frame, (int(nariz_x * w), int(nariz_y * h)), 6, (0, 255, 0), -1)

            if frames_calibracao < 30:
                if ref_nariz_x is None:
                    ref_nariz_x, ref_nariz_y, ref_dist_ombros_olhos = nariz_x, nariz_y, dist_ombros_olhos_atual
                else:
                    ref_nariz_x = (ref_nariz_x * 0.9) + (nariz_x * 0.1)
                    ref_nariz_y = (ref_nariz_y * 0.9) + (nariz_y * 0.1)
                    ref_dist_ombros_olhos = (ref_dist_ombros_olhos * 0.9) + (dist_ombros_olhos_atual * 0.1)
                
                frames_calibracao += 1
                texto_postura = "CALIBRANDO SUA ANATOMIA..."
                cor_hud = (255, 255, 0)
            else:
                postura_fisicamente_errada = False
                motivo_erro = ""
                
                if dist_ombros_olhos_atual < (ref_dist_ombros_olhos * 0.82):
                    postura_fisicamente_errada = True
                    motivo_erro = "ALERTA: POSTURA CORCUNDA!"
                elif (nariz_y - ref_nariz_y) > 0.06:
                    postura_fisicamente_errada = True
                    motivo_erro = "ALERTA: TRONCO MUITO BAIXO!"
                elif abs(nariz_x - ref_nariz_x) > 0.07:
                    postura_fisicamente_errada = True
                    motivo_erro = "ALERTA: CORPO DESALINHADO LATERAL!"
                elif abs(landmarks[11].y - landmarks[12].y) > 0.04:
                    postura_fisicamente_errada = True
                    motivo_erro = "ALERTA: OMBROS INCLINADOS!"

                # LÓGICA DE FILTRO TEMPORAL (DELAY DE 5 SEGUNDOS)
                if postura_fisicamente_errada:
                    if tempo_inicio_desalinhado is None:
                        tempo_inicio_desalinhado = tempo_atual
                    
                    tempo_passado_errado = tempo_atual - tempo_inicio_desalinhado
                    
                    if tempo_passado_errado >= TEMPO_LIMITE_ALERTA:
                        classe_predita = 2
                        cor_hud = (0, 0, 255)
                        texto_postura = motivo_erro
                    else:
                        tempo_restante = int(TEMPO_LIMITE_ALERTA - tempo_passado_errado) + 1
                        texto_postura = f"POSTURA INSTAVEL... ({tempo_restante}s)"
                        cor_hud = (0, 165, 255) # Laranja para aviso
                else:
                    tempo_inicio_desalinhado = None
        else:
            tempo_ausente += dt
            texto_postura = "CADEIRA VAZIA"
            cor_hud = (255, 0, 0)
            tempo_inicio_desalinhado = None 

        # SÓ COLETA DADOS APÓS CALIBRAÇÃO ESTABILIZAR
        if frames_calibracao >= 30:
            y_real.append(classe_real_atual)
            y_predito.append(classe_predita)

        # Renderização do HUD na Tela
        cv2.rectangle(frame, (10, 10), (460, 150), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (460, 150), cor_hud, 2)
        
        status_txt = "STATUS: PRESENTE" if classe_predita > 0 else "STATUS: USUARIO AUSENTE"
        cv2.putText(frame, status_txt, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, texto_postura, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_hud, 2)
        
        cv2.putText(frame, f"Tempo focado: {int(tempo_presente)}s", (20, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(frame, f"Tempo longe do PC: {int(tempo_ausente)}s", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        status_real_str = ["Ausente (0)", "Correto (1)", "Incorreto (2)"][classe_real_atual]
        cv2.putText(frame, f"Validacao PUC (Gabarito Teclado): {status_real_str}", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)

        cv2.imshow('Monitoramento de Presenca e Ergonomia', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('1'):
            classe_real_atual = 1
            print("-> Gabarito alterado via teclado: POSTURA CORRETA")
        elif key == ord('2'):
            classe_real_atual = 2
            print("-> Gabarito alterado via teclado: POSTURA INCORRETA")
        elif key == ord('0'):
            classe_real_atual = 0
            print("-> Gabarito alterado via teclado: CADEIRA VAZIA")

    cap.release()
    cv2.destroyAllWindows()

# =====================================================================
# MATRIZ DE CONFUSÃO E RELATÓRIO ANALÍTICO
# =====================================================================
nomes_classes = ['Ausente', 'Presente (Ok)', 'Postura Inadequada']
print("\n" + "="*60)
print("             RELATÓRIO DE DESEMPENHO DA SESSÃO")
print("="*60)
print(f"Tempo Total Conectado: {int(tempo_presente)} segundos")
print(f"Tempo Total Longe do PC: {int(tempo_ausente)} segundos")
print("-"*60)

if len(y_real) > 0:
    print(classification_report(y_real, y_predito, labels=[0, 1, 2], target_names=nomes_classes, zero_division=0))

    cm = confusion_matrix(y_real, y_predito, labels=[0, 1, 2])
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=nomes_classes)
    disp.plot(cmap=plt.cm.Blues, values_format='d')

    plt.title('Matriz de Confusão por Teclado - PUC-MG')
    plt.xlabel('Predito pelo Sistema (IA)')
    plt.ylabel('Realidade (Gabarito Informado)')
    plt.savefig('matriz_tempo_real.png', bbox_inches='tight')
    
    # FORÇA A MATRIZ A PULAR NA TELA NA FRENTE DE TUDO
    try:
        fig = plt.gcf()
        fig.canvas.manager.window.attributes('-topmost', 1)
    except Exception:
        pass 
        
    print("\n[INFO] Exibindo a Matriz de Confusão... Feche a janela do gráfico para encerrar o programa.")
    plt.show()
else:
    print("[AVISO] O sistema foi fechado antes de coletar dados válidos pós-calibração.")