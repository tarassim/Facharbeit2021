#
# Facharbeit2021Starter sorgt dafür, dass man die Anlage nach einem Absturz wieder startenb kann
# v3.2
#
# Python (nicht Python3!!!)
#

import discord			# Importiert Discord Libary
import asyncio			# Für Asyncrone methoden
import subprocess		# Für Shell befehle
import time			# Für Verzögerungen

token = "TOKEN" # Der Bot Token

def getPassword():
	pswd = open("passwd.txt" , "r")
	passwrd = pswd.readline().strip()
	pswd.close()
	return passwrd

def kill():
	k = subprocess.Popen("pgrep vlc", stdout=subprocess.PIPE, shell=True)
	output, err = k.communicate()
	try:
		rip = subprocess.Popen("kill -9" + str(int(output)), stdout=subprocess.PIPE, shell=True)
		rip.wait()
	except ValueError:
		pass
	k2 = subprocess.Popen("pgrep python3", stdout=subprocess.PIPE, shell=True)
	output, err = k2.communicate()
	processes = str(output).strip()
	processes = processes.replace("b","")
	processes = processes.replace("'","")
	processes = processes.split("\\n")
	for x in processes:
		rip2 = subprocess.Popen("kill -9 " + x, stdout=subprocess.PIPE, shell=True)
		rip2.wait()

async def cleanChannel(pCount, pChannel):
	async for message in pChannel.history(limit=pCount):
		if (message.id != 899046028085428224 and message.id != 898391768888909824):		# Die Nachrichten mit den entsprechenden IDs  sind Erklärungen
			await message.delete()


class MyBot(discord.Client):
	async def on_ready(self):
		print ("waiting for /startSystem")
	async def on_message(self, message):
		if (message.content == "/restart "+getPassword()):
			await message.channel.send("restarting...")
			await cleanChannel(2, message.channel)
			kill()
			start = subprocess.Popen("python3 WatchCat.py", stdout=subprocess.PIPE, shell=True)
			time.sleep(1)
		elif (message.content == "/startSystem "+getPassword()):
			await message.channel.send("starting...")
			await cleanChannel(2, message.channel)
			kill()
			start = subprocess.Popen("python3 WatchCat.py", stdout=subprocess.PIPE, shell=True)
			time.sleep(1)
		elif(message.content.startswith("/startSystem")):
			await message.channel.send("Use /start PASSWORT to start the System")
			await cleanChannel(2, message.channel)



if __name__ == '__main__':
	client = MyBot()
	client.run(token)
