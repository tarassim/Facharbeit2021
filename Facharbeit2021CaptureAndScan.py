#
# Facharbeit2021 Autor:Christoph Mörs Version: 3.0
#
#############################################################################################################################
#
# Das Programm greift aus dem Stream der IP-Kamera, durch ffmpeg, ein Bild ab und untersucht es unter der Verwendung von YOLO
# siehe:
# YOLO: https://pjreddie.com/darknet/yolo/
# ffmpeg: https://ffmpeg.org/ffmpeg.html
#
#############################################################################################################################
#
# Python3
#

import subprocess	# Im späteren Verlauf wird subprocess verwendet um Befehle in der Shell auszuführen
import time 		# Zeitmodul für Logs etz.
import paramiko 	# Ein ssh Modul, über das Modul wird ein befehl gesendet, welcher dazu führt das ein Licht blinkt
import os		# Wird von paramiko gebraucht
from multiprocessing import Process	# Für parraleles ablaufen von Methoden

class core():

	# Gibt die Wahrscheinlichkeit an mit der eine Person erkennt werden muss bevor der Alarm ausgelöst wird
	minValueAlarm = 40

	# Der Pfad zum darknet Ordner
	pfad = "darknet"

	# Pfad zum Bild mit den Ergebnisen
	pathToPrediction = "predictions.jpg"

	# Der Befehl womit ich ein Bild aus dem Stream erhalte
	cmdGetImg ="ffmpeg -loglevel fatal -rtsp_transport tcp -i \"rtsp://GpSJkxsh:A8CH8Q5ubY8S6FT3@192.168.178.111:554/live/ch0\" -r 1 -vframes 1 Camera.png -y"

	# Der Befehl der den Scan auslöst (WICHTIG!!! Der Ordnet data und cfg aus darknet muss sich im gleichen Verzeichniss befinden wie dieses Programm am besten befindet sich der ordner sowohl in /darknet als auch in ./
	cmdScan = "./darknet/darknet detector test darknet/cfg/coco.data darknet/cfg/yolov4.cfg darknet/yolov4.weights Camera.png -i o -thresh0.25"

	#Alarmanlage ist aktiv
	active = True

	#gibt an ob der Alarm läuft
	alreadyrunning = False

	def __init___():				#Konstruktor
		pass


	def lookup(self):
		pass
	def main(self, queue):					# Der Alarm, wenn er denn ausgelöst wird läuft parralel zum Rest, queue wird zum Austausch mit dem Prozess verwendet
		while True:
			self.getImg()
			if self.enemyDetected() == True:
				self.log("\n" + "Person detected at: " + time.ctime()+ "\n")
				self.safePic()
				if(self.alreadyrunning == False):
					self.alreadyrunning = True
					print ("start rec")
					rec = Process(target=self.record)                                 #Startet Aufnahme aber nur wenn der Alarm noch nicht lief
					rec.start()
					print ("nach rec")
					self.log("\n" + "Alarm activated at: " + time.ctime()+ "\n")
						                 # Verbindungsdaten (natürlich verändert)
					while (self.active):						# Erst wenn disarm() ausgeführt wurde bricht die Schleife ab
						#alarma = Process(target=self.alarm)			# Die Methode Alarm wird nun Parralel ausgeführt, dies führt dazu, dass die Anlage weiter nach Personen sucht und diese Aufniimmt
						#alarma.start()							# Sorgt dafür, dass der Mother Prozess kann beendet werden auch wen alarm() noch läuft
						self.alarm()
						time.sleep(4)
						self.active = self.readQueue(queue, True)
					print ("bin raus")
					self.pauseAlarm(queue)


	def log(self, tolog):
		templog = open("templog.txt", "a")			# templog ist zum austausch zwichen diesem Programm und Logger.py
		permlog = open("permlog.txt", "a")			# permlog ist ein Log der vor Ort verbleibt (auf dem Pc)
		templog.write(tolog)
		permlog.write(tolog)
		templog.close()
		permlog.close()
	#	log = subprocess.Popen("python3 Logger.py", stdout=subprocess.PIPE, shell=True)	# Logger schickt das Log zu discord in den "log" channel
	#	log.wait()

	def getImg(self):							# Greift ein Bild aus dem Kamera Stream ab
		log = self.log

		p = subprocess.Popen(self.cmdGetImg, stdout=subprocess.PIPE, shell=True)

		p.wait()

		log("\n" +"Img_loaded at: " + time.ctime() + "\n")


	def scan(self): 						# Scant das Bild was getImg() geliefert hat und gibt den output zurück
		log = self.log
		cmdScan = self.cmdScan

		log("\n" + "Start Scan at: " + time.ctime() + "\n")

		p = subprocess.Popen(cmdScan, stdout=subprocess.PIPE, shell=True)

		output, err = p.communicate()

		p.wait()


		log("\n" + "Finished Scan at: " + time.ctime() + "\n")

		strOut = str(output)					# Von Bytes in String umwandeln
		out = strOut.split("\\n")				# Teilt den Langen String bei \n auf
		return out						# Ausgabe ist dann eine Liste

	def enemyDetected(self): 						# Schaut ob scan() Personen gefunden hat
		minValueAlarm = self.minValueAlarm			# Da der wert nicht verändert wird, reicht einmaliges Auslesen
		objects = self.scan()					# Erhält die Ausgabe des Scans
		for x in objects:					# Geht jede stelle der Liste durch
			if "person:" in x:				# Wenn ein String "person:" enthält, wird die Wahrscheinlichkeit überprüft
				size = len(x)
				rawPercent2 = x[size-4:]		# Die letzten 4 Stellen sind entweder "xxx%" oder " xx%" durch das "[size-4]" wir der string verkleinert es verbleibt jetzt entweder "xxx%" oder " xx%"
				rawPercent = rawPercent2[:3]		# Nun werden nur noch die ersten 3 Stellen genommen, "xxx" oder " xx"
				percent = int(rawPercent.lstrip())	# Entfernen des Leerzeichen und umwandeln in int
				if percent > minValueAlarm:
					return True
					print ("True")


	def safePic(self):
		pathToPrediction = self.pathToPrediction
		print ("1")
		new = "predictions"+ str(time.ctime()).replace(" ", "")+".jpg"			# Zeitstempel hinzufügen
		print ("2")
		c = subprocess.Popen("cp -p "+ pathToPrediction + " " + "./detections/" + new, stdout=subprocess.PIPE, shell=True)	# Speichert eine Kopie der prediction mit Zeit, sodass diese zu einem späteren Zeitpunkt einsehbar ist. Jedes mal wenn eine Person erkannt wurde
		print ("3")
		output, err = c.communicate()
		print ("4")

	def alarm(self):
				ssh = paramiko.SSHClient()                                                              # Aufbauen der Verbindung
				ssh.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
				ssh.connect("192.168.178.62", username="pi", password="Pi2021")
				stdin1, stdout1, stderr1 = ssh.exec_command('sudo 433Utils/RPi_utils/steuerung 1')	# Licht anschalten
				stdin1.close()
				time.sleep(2)
				stdin0, stdout0, stderr0 = ssh.exec_command('sudo 433Utils/RPi_utils/steuerung 0')	# Licht ausschalten
				stdin0.close()
				ssh.close()
				print ("closed")										# Verbindung trennen

	def readQueue(self, queue, excepted):
		print ("a")
		if(queue.empty()== False):
			first = queue.get_nowait()
			while (queue.empty()==False):
				puffer = queue.get_nowait					# sorgt dafür das die queue immer leer ist
			print ("queue : " + str(first))
			if (str(first) == "True"):
				print ("return: True")
				return True
			elif(str(first) == "False"):
				print("return: False")
				return False
		print ("alternativ")
		return excepted


	def disarmAlarm(self, queue): 								# Dies deaktiviert den Alarm und die Alarmanlage nimmt ihren Betrieb wieder auf
		queue.put(False)

	def armAlarm(self, queue):
		queue.put(True)
		print ("putput")

	def pauseAlarm(self, queue):
		print ("Wir gehen Rein")
		self.active = False
		print ("a")
		ssh = paramiko.SSHClient()                                                              # Aufbauen der Verbindung
		print ("b")
		ssh.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
		print ("c")
		ssh.connect("192.168.178.62", username="pi", password="Pi2021")
		print ("d")
		time.sleep(1)
		stdin1, stdout1, stderr1 = ssh.exec_command('sudo 433Utils/RPi_utils/steuerung 1')		# Licht anschalten
		print ("e")
		stdin1.close()
		print ("f")
		self.log("\n" + "Alarm Stoped at: " + time.ctime()+ "\n")
		print ("g")
		while True:
			print ("wir bleiben drin")
			self.active = self.readQueue(queue, False)
			if(self.active):
				print("und aus")
				stdin0, stdout0, stderr0 = ssh.exec_command('sudo 433Utils/RPi_utils/steuerung 0')      # Licht anschalten
				stdin0.close
				ssh.close()
				self.stopRecord()
				time.sleep(4)
				self.log("The System is Active: " + time.ctime())
				self.alreadyrunning = False
				break
		return

	def record(self):
		k = subprocess.Popen("pgrep vlc", stdout=subprocess.PIPE, shell=True)
		output, err = k.communicate()
		name= "record" + str(time.ctime()).replace(" ", "") + ".mpg"
		if(str(output) == "b\'\'"):								# Der Prozess wird noch nicht ausgeführt, dann führe ihn aus
			r = subprocess.Popen("cvlc rtsp://GpSJkxsh:A8CH8Q5ubY8S6FT3@192.168.178.111:554/live/ch0 --sout=file/ts:" + name, shell=True)
			r.wait()
			mv = subprocess.Popen("mv "+ name + " " + "./detections/"+name, stdout=subprocess.PIPE, shell=True)
			mv.wait()
		return

	def stopRecord(self):
		k = subprocess.Popen("pgrep vlc", stdout=subprocess.PIPE, shell=True)
		output, err = k.communicate()
		try:
			rip = subprocess.Popen("kill " + str(int(output)), stdout=subprocess.PIPE, shell=True)
			rip.wait()
		except ValueError:
			pass
		finally:
			return
	load=True										# Lädt alle Methoden der Klasse
	print("geladen")

#if __name__ == "__main__":
#	print ("ja")
#	anlage = core()
#	anlage.main(anlage)
#	print("hä")
