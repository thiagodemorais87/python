import random

def jogo_adivinhacao():
    numero_secreto = random.randint(1, 100)
    tentativas = 10
    print("Bem-vindo ao jogo de Adivinhação!")
    print("Tente adivinhar o número entre 1 e 100.")

    for tentativa in range(1, tentativas + 1):
        palpite = int(input(f"Tentativa {tentativa}: "))
        
        if palpite < numero_secreto:
            print("Tente um número maior!")
        elif palpite > numero_secreto:
            print("Tente um número menor!")
        else:
            print(f"Parabéns! Você acertou o número {numero_secreto} em {tentativa} tentativas.")
            break
    else:
        print(f"Você perdeu! O número era {numero_secreto}.")

jogo_adivinhacao()