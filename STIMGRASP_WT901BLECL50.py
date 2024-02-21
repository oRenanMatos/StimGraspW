import serial
import time
import numpy as np
import WT901BLECL50 as IMU
import WT901BLECL50Config as IMUConfig
import threading

stimgrasp_port = "/dev/ttyUSB1"
stimgrasp_baudrate = 9600

port = "/dev/ttyUSB0"
baudrate = 115200

ser = serial.Serial(port,baudrate, timeout=1)

ser1 = serial.Serial(stimgrasp_port,stimgrasp_baudrate, timeout = 1)

# Variaveis globais 
current_CH0 = 25.0 #corrente do canal 1 em (mA)
frequency = 20	   #frequencia do sinal em (Hz)
pulse_width = 200  #largura de pulso do sinal (us)	

setStimGrasp = False
updateStimGrasp = False
updateSetStimGrasp  = False
startStimGrasp = False
stopStimGrasp = False
shutdownStimGrasp = False


def thread_WT901BLECL50():
	while True:
		if(ser.in_waiting >=2):
			start_bytes = ser.read(2)
			if(start_bytes == b'\x55\x61' or start_bytes == b'\x55\x71'):
				dataHex = start_bytes + ser.read(18)
				MotionData= IMU.getMotionData(dataHex, currTime)
				print("{:.3f} sec| acc_x {:.3f} m/s^2 acc_y {:.3f} m/s^2 acc_z {:.3f} m/s^2 ".format(MotionData[0], MotionData[1], MotionData[2], MotionData[3]))

def thread_STIMGRASP():
	while True:
		# Utilizando a palavra-chave global para acessar a variável global dentro da função
		global frequency
		global pulse_width
		global current_CH0
		global setStimGrasp
		global updateStimGrasp
		global updateSetStimGrasp
		global startStimGrasp
		global stopStimGrasp
		global shutdownStimGrasp
		
		if setStimGrasp:
				
			pulse_width_ = pulse_width
			frequency_ = frequency
			current_CH0_ = current_CH0
			
			if(pulse_width_ >= 200 and frequency_ < 111 and frequency_ >= 10 and current_CH0_ >= 5 and current_CH0_ < 26):
			
				#Ajusta os valores para serem enviados para o Stimgrasp de uma forma que ele entenda
				pulse_width_ = round((pulse_width_/100) - 2)
				frequency_ = round((1/frequency_)*10000)
				current_CH0_ = round(current_CH0_ * 42.41)
			
				# Formatar as variáveis conforme necessário
				formatted_pulse_width = f"{pulse_width_:04d}"  # "0002"
				formatted_frequency = f"{frequency_:04d}"      # "0500"
				formatted_current_CH0 = f"{current_CH0_:04d}"      # "0500""
			
				#Configura o tempo de subida para 3 segundos para todos os canais
				dataToSend = "<STIMV0010001000100010001000100010001000>\n"
				ser1.write(dataToSend.encode())
				time.sleep(0.5)
		
				#Configura o tempo de descida para 1 segundo para todos os canais
				dataToSend = "<STIMV0120001000100010001000100010001000>\n"
				ser1.write(dataToSend.encode())
				time.sleep(0.5)
		
				#Configura a amplitude para os canais nesse caso esta sendo configuro apenas os quatro primeiros
				dataToSend = f"<STIMV02{formatted_current_CH0}{formatted_current_CH0}{formatted_current_CH0}{formatted_current_CH0}1000100010001000>\n"
				ser1.write(dataToSend.encode())
				time.sleep(0.5)
		
				#Configura a largura de pulso e frequencia do sinal
				dataToSend = f"<STIMC33{formatted_pulse_width}{formatted_frequency}CCCCDDDDEEEEFFFFGGGGHHHH>\n"
				ser1.write(dataToSend.encode())
				time.sleep(0.5)

				print(f"\n\n\n\n\n Stimgrasp Configurado com sucesso!!! \n pulse_width: {pulse_width_}  frequency: {frequency_} current_CH0 {current_CH0_}\n\n\n\n")
				
				setStimGrasp = False
			else:
				print("\n\nAlgum parametro esta fora dos limites permitidos checar os valores de largura de pulso, frequencia e corrente dos canais.\n\n")
				
		elif updateStimGrasp:
			current_CH0_ = current_CH0
			if(current_CH0_ >= 5 and current_CH0_ < 26):
				#Ajusta os valores para serem enviados para o Stimgrasp de uma forma que ele entenda
				current_CH0_ = round(current_CH0_ * 42.41)
			
				# Formatar as variáveis conforme necessário	
				formatted_current_CH0 = f"{current_CH0_:04d}"      # "0500""
				#Atualiza o valor da amplitude para os canais nesse caso esta sendo atualizado apenas os quatro primeiros
				dataToSend = f"<STIMC03{formatted_current_CH0}{formatted_current_CH0}{formatted_current_CH0}{formatted_current_CH0}1000100010001000>\n"
				ser1.write(dataToSend.encode())
				time.sleep(1)
				print(" Status: Amplitude atualizada com sucesso!")
			else:
				print("\n\nAlgum parametro esta fora dos limites permitidos checar os valores de corrente dos canais.\n\n")
			
			updateStimGrasp = False 
		
		elif updateSetStimGrasp:
			pulse_width_ = pulse_width
			frequency_ = frequency
			
			if(pulse_width_ >= 200 and frequency_ < 111 and frequency_ >= 10):
				#Ajusta os valores para serem enviados para o Stimgrasp de uma forma que ele entenda
				pulse_width_ = round((pulse_width_/100) - 2)
				frequency_ = round((1/frequency_)*10000)

			
				# Formatar as variáveis conforme necessário
				formatted_pulse_width = f"{pulse_width_:04d}"  # "0002"
				formatted_frequency = f"{frequency_:04d}"      # "0500"
				
				#Atualiza a largura de pulso e frequencia do sinal
				dataToSend = f"<STIMC33{formatted_pulse_width}{formatted_frequency}CCCCDDDDEEEEFFFFGGGGHHHH>\n"
				ser1.write(dataToSend.encode())
				time.sleep(0.5)
				print(" Status: Largura de pulso e frequencia atualizada com sucesso!")
			else:
				print("\n\nAlgum parametro esta fora dos limites permitidos checar os valores de corrente dos canais.\n\n")
			
			updateSetStimGrasp = False 
								
		elif startStimGrasp:
			pulse_width_ = pulse_width
			frequency_ = frequency
			current_CH0_ = current_CH0
						
			if(pulse_width_ >= 200 and frequency_ < 111 and frequency_ >= 10 and current_CH0_ >= 5 and current_CH0_ < 26):
				#Ativa o Stimgrasp para realizar o estimulo
				dataToSend = "<STIMC04AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH>\n"
				ser1.write(dataToSend.encode())
				time.sleep(1)
				print(" Status: Iniciando o estimulo com sucesso!")
			else:
				print("\n\nAlgum parametro esta fora dos limites permitidos checar os valores de largura de pulso, frequencia e corrente dos canais.\n\n")
			startStimGrasp = False
			
		elif stopStimGrasp:
			pulse_width_ = pulse_width
			frequency_ = frequency
			current_CH0_ = current_CH0
						
			if(pulse_width_ >= 200 and frequency_ < 111 and frequency_ >= 10 and current_CH0_ >= 5 and current_CH0_ < 26):
				#Desativa esimulo do Stimgrasp
				dataToSend = "<STIMC02AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH>\n"
				ser1.write(dataToSend.encode())
				time.sleep(1)
				print(" Status: Estimulo Interrompido com sucesso!")
			else:
				print("\n\nAlgum parametro esta fora dos limites permitidos checar os valores de largura de pulso, frequencia e corrente dos canais.\n\n")
			
			stopStimGrasp = False
			
		elif shutdownStimGrasp:
			#Desativa esimulo do Stimgrasp
			dataToSend = "<STIMC00AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH>\n"
			ser1.write(dataToSend.encode())
			time.sleep(1)
			print(" Status: Stimgrasp Desligado com sucesso!")

			shutdownStimGrasp = False
			
			time.sleep(1)
		else:
			pass

print("STIMGRASP e WT901BLECL50\n")


currTime=time.time()
thread_WT901BLECL50 = threading.Thread(target=thread_WT901BLECL50)
#thread_WT901BLECL50.start()

thread_STIMGRASP = threading.Thread(target=thread_STIMGRASP)
thread_STIMGRASP.start()

#Exemplo
#Inicializando Stimgrasp
#Frequencia de 15 Hz
#Largura de Pulso 300 us
#Corrente de estimulo 20 mA

#Configura os parametros
current_CH0 = 10
frequency = 20
pulse_width = 200

#Manda as configuracoes para o Stimgrasp
setStimGrasp = True

#Inicia o estimulo
startStimGrasp = True

time.sleep(10)

#Atualiza o valor de corrente para 10 mA
current_CH0 = 20
#Manda atualizar o valor de corrente no Stimgrasp
updateStimGrasp = True

time.sleep(10)

#Atualiza o valor de largura de pulso para 200us e frequencia para 30 HZ
pulse_width = 400
#frequency = 30
#Manda atualizar o valor de largura de pulso e frequencia
updateSetStimGrasp = True

time.sleep(20)

#Manda parar a estimulacao
stopStimGrasp = True

time.sleep(10)

#Manda desligar o Stimgrasp
shutdownStimGrasp = True

while True:
	input()
	ser.close()
	thread_WT901BLECL50.stop()
	time.sleep(1)
	

