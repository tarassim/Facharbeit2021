Einrichten der Facharbeit2021

Im discord Developer Portal 3 Bots erstellen und diese einem Server hinzufügen.
Auf dem Server verschiedene Textchannel erstellen und die ID's später in den Quellcode einfügen,
ebenso die Tokens

Linux Betriebssystem benötigt:
	optional:
	1. Virtual Machine Herunterladen
		Installiere Virtual Box von:
		https://www.virtualbox.org
	2. Ubuntu Server oder Desktop Herunterladen
		https://ubuntu.com/download/
	3. Ubuntu zu VirtualBox hinzufügen und einrichten

Installieren der Packete:
	sudo apt-get update && sudo apt-get upgrade
	sudo apt-get install python3
	sudo apt install python-is-python3
	sudo apt install pip
	sudo pip install discord
	sudo apt install ffmpeg
	sudo apt install vlc

	git clone  tarassim/Facharbeit2021.git
	cd Facharbeit2021
	
	Installieren von Yolo nach:
	https://robocademy.com/2020/05/01/a-gentle-introduction-to-yolo-v4-for-object-detection-in-ubuntu-20-04/
	(Achtung in Makefile mus OpenCV = 0 stehen und die einstellungen entsprechen CPU oder GPU build)
	(Achtung: Haben Sie Yolo v4 weigths runtergeladen? (https://drive.google.com/u/0/uc?export=download&confirm=ZrNT&id=11m9OszXC2kO33sDl8a0gtrNIlZs40D3z))
	
	cp -r cfg ..
	cp -r data ..
	cd .. (in den Facharbeitsordnet zurückkehren)
	
	mkdir detections
	
	mit "nano DATEINAME" die 3 Programme (Logger.py, WatchCat.py, Starten.py) bearbeiten (Token und Channel ID's)

	in Facharbeit2021CaptureAndScan unter def Alarm, def pauseAlarm, def reArmAlarm, einstellen was passieren soll wenn der Alarm ausgelöst wir
	
	sicherstellen, dass wenn der Alarm über ssh(ausgelöst war der rechner zuvor einmalig mit dem zu ereichendem Rechner verbunden war)
	
	und finally: python Starten.py und im Discord /startSystem Baum1234

	mit /help herhalten sie eine übersicht aller Befehle
