#
# Facharbeit2021WatchCat dies ist der Bot welcher die Alarmanlage Steuert und auch über Logger richten kann.
# Also quasi DER rosa Elephant unter den Rosa Elephanten
#
# v3.0
#

import discord		# Wie immer die Discord Lib
import asyncio		# Für asyncrone Methoden
import time		# Für die Zeit
import subprocess	# Für Shell befehle
import threading	# Für parraleles ablaufen von Methoden
import Facharbeit2021CaptureAndScan as coreprog # Der Core der Alarmanlage
from multiprocessing import Process, Queue # Ähnlich threading wird ausschließlich bei record benutzt, da threading in der kombination nicht funktioniert

core = coreprog.core()

praefix = "/"
cmdGetImg ="ffmpeg -loglevel fatal -rtsp_transport tcp -i \"rtsp://GpSJkxsh:A8CH8Q5ubY8S6FT3@192.168.178.111:554/live/ch1\" -r 1 -vframes 1 stream.png -y"
streamChID = 898391213554663556
statusChID = 898994828271042631
runstream = False
detec = 898190093804781589              # Channel ID
everyoneID=898189948803481660           # ID der Rolle everyone
pathToPrediction = "predictions.jpg"

def getPassword():
	pswd = open("passwd.txt" , "r")
	passwrd = pswd.readline()
	pswd.close()
	return passwrd

def setPassword(pPasswd):
	pswd = open("passwd.txt", "w")
	pswd.write(pPasswd)
	pswd.close()
	return

async def cleanChannel(pCount, pChannel):
	async for message in pChannel.history(limit=pCount):
		if (message.id != 899046028085428224 and message.id != 898391768888909824):
			await message.delete()



def handleRecord(pTime):	# Das sind nicht die Jed-i ähhh die Methode die Sie suchen
	print ("Hä")			# Nein wirklich die Lösung ist einfach beschissen aber die beste die ich finden konnte
	p1 = Process(target=core.record)
	p1.start()
	print("zwichen")
	p2 = Process(target=timeToRecord, args=(pTime,))
	p2.start()
	print ("weiter")
	return

def timeToRecord(pTime):
	time.sleep(pTime)
	core.stopRecord()

def kill():
	k = subprocess.Popen("pgrep vlc", stdout=subprocess.PIPE, shell=True)
	output, err = k.communicate()
	try:
		rip = subprocess.Popen("kill -9 " + str(int(output)), stdout=subprocess.PIPE, shell=True)
		rip.wait()
	except ValueError:
		pass
	k2 = subprocess.Popen("pgrep python3", stdout=subprocess.PIPE, shell=True)
	output, err = k2.communicate()
	processes = str(output).strip()
	processes = processes.replace("b","")
	processes = processes.replace("'","")
	processes = processes.split("\\n")
	i = len(processes)-1
	print (processes)
	while i >=0:
		try:
			rip2 = subprocess.Popen("kill -9 " + str(int(processes[i-1])), stdout=subprocess.PIPE, shell=True)
			rip2.wait()
		except ValueError:
			pass
		i=i-1
	exit()

	#_____________________$$______#
	#__$s_______s$__________$$____#
	#_$$$_$$$_$$$$__________$$____#
	#_$$$O$$$$O$$$___________$$___#
	#_$$$$$=Y=$$$$___________$$___#
	#__$$$$$$$$$$____________$$___#
	#_____$$$$___$$$$$$$$$__$$____#
	#______$$$$$$$$$$$$$$$$$$_____#
	#____$$$$$$$$$$$$$$$$$$$______#
	#____$$_$$_$$$$$$_$$_$$_______#
	#__$$__$$_________$$__$$______#
	#(($$ ((($$$$___((($$$$_$$$$__#

class MyBot(discord.Client):

	runstream == False
	queue = Queue()
	main = Process(target=core.main, args=[queue])



	async def stream(self):
		print("stream Test")
		while runstream == True:
			p = subprocess.Popen(cmdGetImg, stdout=subprocess.PIPE, shell=True)
			p.wait()
			streamCh = client.get_channel(streamChID)
			await streamCh.send(file=discord.File("stream.png"))
			async for oldmsg in streamCh.history(limit=3):
				if (oldmsg.id != 898391768888909824 and oldmsg != oldmsg.channel.last_message):
					await oldmsg.delete()
		return
	#TODO: möglichkeit für parraleles zu finden
	async def on_ready(self):
		print("Ich habe mich eingelogt. Beep bop bup.")
		statusCh = client.get_channel(statusChID)
		await cleanChannel(1, statusCh)
		await statusCh.send("```diff\nThe System is: \n+ active\n```")
		self.main.start()								#startet das Core Programm

	async def on_message(self, message):
		global runstream
		global statusChID
		global everyoneID
		if (message.content.startswith(praefix+"help")):
			help1 = f"\
This is a list of all commands:\n\
+ {praefix}help => Zeigt diese Hilfe Seite\n\
+ {praefix}changePassword PASSWORD NEW_PASSWORD => Ändern des Passworts\n\
+ {praefix}clean ANZAHL => Löcht die letzten ANZAHL Nachrichten in dem Channel der Nachricht\n\
+ {praefix}startSystem stream => Streamt live Bilder in den \#stream Channel\n\
+ {praefix}stop stream => Stoppt den Livestream\n\
+ {praefix}record TIME => Nimmt für TIME Minute ein Video auf und Speichert es auf dem Analyse-Pc\n\
+ {praefix}disarm PASSWORD => Entschärft die Alarmanlage/stellt den Alarm aus\n\
+ {praefix}arm PASSWORD => Schaltet die Alarmanlage scharf\n"

			
			await message.channel.send("```diff\n" + help1 + "```")
			help2 = f"\
```fix\n\
O {praefix}restart PASSWORD => Startet die Anlage neu HANDLE_WITH_CARE\n\
```"
			await message.channel.send(help2)
			help3 =f"\
- {praefix}start PASSWORD => Startet die Anlage ADMIN_USAGE_ONLY\n\
- {praefix}kill PASSWORD => Deaktiviert die Anlage kommplett ADMIN_USAGE_ONLY\n"

			await message.channel.send("```diff\n"+help3+"```")			
							
		if (message.content.startswith(praefix+"changePassword "+getPassword())):
			input = message.content
			splitinput = input.split(" ")
			if (splitinput[1]==getPassword()):
				setPassword(splitinput[2])
				await message.channel.send("New password is:" + getPassword() + "\nThis Chat will be deleted in 3 seconds")
				time.sleep(3)
				await cleanChannel(2, message.channel)
		elif (message.content == praefix+"changePassword".rstrip()):
			await message.channel.send("Please enter: old_password new_password\nTry again in 5 seconds")
			time.sleep(5)
			await cleanChannel(2, message.channel)
		elif(message.content.startswith(praefix+"changePassword ")):
			await message.channel.send("Something went wrong please try again\nThis Chat will be deleted in 3 seconds")
			time.sleep(3)
			await cleanChannel(2, message.channel)
		if(message.content.startswith(praefix+"clean ")):
			input = message.content
			splitinput = input.split(" ")
			await cleanChannel(int(splitinput[1].rstrip()), message.channel)
		if(message.content.startswith(praefix+"start ")):
			input = message.content
			splitinput = input.split(" ")
			if (splitinput[1]=="stream"):
				runstream= True
				print (self)
				print (message.channel)
				s = threading.Thread(target=await self.stream())		# Führt die Methode stream() parrallel zum Rest aus
				s.deamon = True
				print ("nope")				# Führt die Methode stream() parrallel zum Rest aus
			elif (splitinput[1]=="audio"):
				pass # TODO: audio konversation einfügen !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		if(message.content.startswith(praefix+"stop ")):
			input = message.content
			splitinput = input.split(" ")
			if (splitinput[1]=="stream"):
				runstream = False
			elif (splitinput[1]=="audio"):
				pass # TODO: audio konversation einfügen !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		if(message.content.startswith(praefix+"record ")):
			input = message.content
			splitinput = input.split(" ")
			#r = subprocess.Popen("cvlc rtsp://GpSJkxsh:A8CH8Q5ubY8S6FT3@192.168.178.111:554/live/ch0 --sout=file/ts:record.mpg", stdout=subprocess.PIPE, shell=True)
			print ("before")
			handleRecord(int(splitinput[1])*60)
			print("parralel")
		if(message.content.startswith(praefix+"disarm " + getPassword())):
			await cleanChannel(1, message.channel)
			await message.channel.send("accepted!")
			time.sleep(1)
			await cleanChannel(1, message.channel)
			print ("Trying...")
			core.disarmAlarm(self.queue)		#Teil disarm die Instanz mit in der der core Prozess läuft und die queue zur kommunikation
			print ("Done")
			statusCh = client.get_channel(statusChID)
			everyone = discord.utils.get(client.get_channel(detec).guild.roles, id=everyoneID)
			await cleanChannel(1, statusCh)
			await statusCh.send("```diff\nThe System is: \n- inactive\n```")
		if(message.content.startswith(praefix+"arm " + getPassword())):
			await cleanChannel(1, message.channel)
			await message.channel.send("accepted!")
			await message.channel.send("The System will be active again in 5 seconds")
			time.sleep(3)
			await cleanChannel(2, message.channel)
			core.armAlarm(self.queue)            #Teil arm die Instanz mit in der der core Prozess läuft und die queue zur Kommunikation
			statusCh = client.get_channel(statusChID)
			await cleanChannel(1, statusCh)
			await statusCh.send("```diff\nThe System is: \n+ active\n```")
		if(message.content.startswith(praefix+"kill " + getPassword())):
			statusCh = client.get_channel(statusChID)
			everyone = discord.utils.get(client.get_channel(detec).guild.roles, id=everyoneID)
			await cleanChannel(1, statusCh)
			await cleanChannel(1, message.channel)
			await statusCh.send("```diff\nThe System is: \n- inactive\n```")
			kill()

	#dchannel=client.get_channel(detec)
        #global yep
        #global pathToPrediction
        #if yep:
        #    await dchannel.send(file=discord.File(pathToPrediction))
        #    yep = False
        #exit()
if __name__ == '__main__':
	logger = subprocess.Popen("python3 Logger.py", stdout=subprocess.PIPE, shell=True)
	#logger.wait()
	client = MyBot()
	client.run("ODk4MTgwODU3MDQxMzk5ODE4.YWgeGw.DhipqSJ8tDV0Ug6IdAM7yaUqGrg")
