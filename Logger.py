#
#
# Facharbeit2021Logger das ist der Bot der für das loggen und reporten zuständig ist
# V3.0
#
#

import discord # Importiert Discord Libary
import asyncio # Für Asyncrone methoden
import time
import subprocess
logid = 898303191731544074		# Channel ID
detec = 898190093804781589              # Channel ID
everyoneID=898189948803481660           # ID der Rolle everyone
pathToPrediction = "predictions.jpg"
token = "ODk4MzAzNDI3NTAxNzYwNTcy.YWiQQg.lunTyf1cVfpQO-QmnOO1WWet9uQ" # Der Bot Token

async def report():
	print	("report")
	global pathToPrediction
	log = open("templog.txt", "r")									# Öffnet templog.txt
	for x in log:											# Geht Zeile für Zeile durch und sucht nach "Alarm activated:"
		if(x.lstrip().startswith("Alarm activated at:")):					# Wurde in der Zwichenzeit ein Alarm ausgelöst, sendet er ein Bild vom Täter in den "detections" Channel und Meldet das Ereigniss
			print (True)
			everyone = discord.utils.get(client.get_channel(detec).guild.roles, id=everyoneID)
			dchannel=client.get_channel(detec)                                      	# Bild holen und senden
			await dchannel.send(f'Achtung {everyone}, eine Person wurde erkannt!!!')
			await dchannel.send(file=discord.File(pathToPrediction))
			atime = str(time.ctime())
			new = "predictions"+atime.replace(" ", "")+".jpg"
			r = subprocess.Popen("cp -p "+ pathToPrediction + " " + "./detections/" + new, stdout=subprocess.PIPE, shell=True)
			r.wait()
			log.close()
			print ("done")
			return True									# Alarm wurde gemeldet und weiteres Absuchen wird unterbrochen um Zeit zu sparen, sollte der Alarm in der Zeit mehrmals aktiviert wurden sein (Logger war über lange Zeit deaktiviert) wird nur das letzte Bild Ausgegeben
	log.close()
	return False											# Es wurde kein Alarm ausgelöst

class MyBot(discord.Client):

	async def on_ready(self):
		await self.LogAndReport()	# Der Bot ist Hochgefahren

	async def LogAndReport(self):                       #übernimmt die aufgabe welche Logger zuvor erfüllte, also den log sowie von report, welches in def report() umgesetzt ist
		logchannel=client.get_channel(logid)									# Channel herausfinden
		await logchannel.send("Logger online! Its " + time.ctime() + " right now")
		doItonce = await report()									# Melde, das der Logger an ist
		while True:											# überprüft ob ein Alarm ausgelöst wurde
			log = open("templog.txt", "r")									# öffnet die Datei, speichert den ganzen Log als cnt (content) ab.
			cnt = log.read()
			log.close()
			async for message in client.get_channel(logid).history(limit=1):				# Schaut ob ein deaktivierungsbefehl vom User gesendet wurde (bezogen auf den Logger NICHT auf die Anlage!!!)
				if cnt == " " or cnt == "":							# der Logger wartet immer darauf das im Log etwas steht nur dann wird er aktiv
					pass									# Wenn nichts neues im Log steht passiert nichts
				else:
					log  = open("templog.txt", "w")						# Log wird zurückgesetzt
					log.write(" ")
					log.close()
					try:
						await logchannel.send(cnt)					# Der zuvor zwichengespeicherte Log wird gepostet
					except Exception as e:
						try:								# Der Log ist zu Lang oder ein anderer Fehler trat auf, meldung erstatten
							await logchannel.send("Its not possible to repost the missed log please look it up on the Head-Pc \nThe Error orcourded was " + str(e))	
						except Exception as e:						# Meldung konnte nicht erstattet werden: Ignorieren
							pass
					for i in range(1, 61):							# Eine Minute nach dem Senden warten um Spam zu verhindern. Ob ein Alarm vorliegt wird allerdings sekündlich geprüft (i in range(1, 61)entspricht in Java i=1; 1<61; i+=1)
						if (await report()):						# Sollte ein Alarm gefunden werden aktualisiere den Log sofort
							break
						time.sleep(1)


client = MyBot()
client.run(token)
