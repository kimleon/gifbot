"""
Consumes the Giphy API -- https://github.com/Giphy/GiphyAPI
i.e. 'http://api.giphy.com/v1/gifs/search?q=superman&api_key=dc6zaTOxFJmzC'
"""

# Import some necessary libraries.
from IPython import embed
import urllib.parse
import socket, ssl
import random
import urllib
import urllib.request
import json
import unicodedata as uni

GIPHY_API = 'http://api.giphy.com/v1/gifs'
GIPHY_KEY = 'dc6zaTOxFJmzC'

# Some basic variables used to configure the bot
server = "irc.your.server.com" # Server
port = 0000 # Port
channel = "#channel" # Channel
botnick = "gifbot" # Your bots nick
current_channel = channel #either channel or None depending on incoming message

def ping(): # This is our first function! It will respond to server Pings.
  ircsock.send(bytes("PONG :pingis\n", 'UTF-8'))

def sendmsg(chan , msg): # This is the send message function, it simply sends messages to the channel.
  if chan is not None:
    ircsock.send(bytes("PRIVMSG "+ chan +" :"+ msg +"\n", 'UTF-8'))

def joinchan(chan): # This function is used to join channels.
  ircsock.send(bytes("JOIN "+ chan +"\n", 'UTF-8'))

def hello(): # This function responds to a user that inputs "Hello Mybot"
  sendmsg(current_channel, "Hello!")

def giphy_me():
  terms = ircmsg.partition('giphy me ')[2]
  # translate from emoji to actual words
  if (terms.encode('utf-8')[:1]==b'\xf0'):
    terms = uni.name(terms.encode('utf-8')[:4].decode('utf-8'))
  if (terms.encode('utf-8')[:1]==b'\xe2'):
    terms = uni.name(terms.encode('utf-8')[:3].decode('utf-8'))
  if (terms == "blerg" or terms == "blergh"):
    terms = "30rock"
  terms = terms.lower()
  print("searching giphy for "+terms)
  sendmsg(current_channel, search_gifs(terms))

def shakecam():
  sendmsg(current_channel,"https://www.shakeshack.com/camera.jpg")

def love():
  sendmsg(current_channel, "http://media0.giphy.com/media/A3SXPrh6OrOc8/giphy.gif")

def idk():
  sendmsg(current_channel, "i don't know")

def hah_no():
  sendmsg(current_channel, "http://media0.giphy.com/media/rsBVkMZABjup2/giphy.gif")

def lmao():
  sendmsg(current_channel, (u'\U0001F47D').encode('utf-8').decode("utf-8")+ "lmao")

def giphy_api_url(endpoint, **kwargs):
  kwargs['api_key'] = GIPHY_KEY
  return "%s%s?%s" % (GIPHY_API, endpoint, urllib.parse.urlencode(kwargs))

def search_api_request(query):
  req = urllib.request.Request(giphy_api_url('/search', q=query))
  with urllib.request.urlopen(req) as response:
   the_page = response.read().decode("utf-8")
  return json.loads(the_page)

def search_gifs(query):
  json = search_api_request(query)
  data = json['data']
  num_choices = len(data)
  # gif_url = "http://i0.kym-cdn.com/photos/images/newsfeed/000/240/081/21f.gif"
  gif_url = (u'\U0001F610').encode('utf-8').decode("utf-8")
  if (num_choices != 0):
    choice = random.randint(0, num_choices-1)
    uni = data[choice]['images']['original']['url']
    gif_url = str(uni)
  return gif_url

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port)) # Here we connect to the server using the port 6667
ircsock = ssl.wrap_socket(s)
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" :This bot is a result of a tutoral covered on http://shellium.org/wiki.\n", 'UTF-8')) # user authentication
ircsock.send(bytes("NICK "+ botnick +"\n", 'UTF-8')) # here we actually assign the nick to the bot

joinchan(channel) # Join the channel using the functions we previously defined

while 1: # Be careful with these! it might send you to an infinite loop
  ircmsg = ircsock.recv(2048).decode("utf-8") # receive data from the server
  ircmsg = ircmsg.rstrip('\r\n') # removing any unnecessary linebreaks.
  print(ircmsg) # Here we print what's coming from the server

  if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
    ping()

  if ircmsg.find(channel+ " :") != -1:
    current_channel = channel
  else:
    their_nick = ircmsg.partition('!~')[0][1:]
    current_channel = their_nick

  if (ircmsg.lower().find(":hello "+ botnick) != -1 or ircmsg.lower().find(":hi "+ botnick) != -1 or ircmsg.lower().find(":hey "+ botnick) != -1):
    hello()

  if ircmsg.lower().find(":"+ botnick+ " why") != -1:
    idk()

  if ircmsg.find(":"+ botnick+ " giphy me ") != -1:
    giphy_me()

  if ircmsg.find(":"+ botnick+ " are you my friend?") != -1:
    hah_no()

  if ircmsg.find(":"+ botnick+ " shakecam") != -1:
    shakecam()
  
  if ircmsg.find(":"+ botnick+ " ayy") != -1:
    lmao()

  if ircmsg.lower().find(":i love you "+ botnick) != -1:
    love()
        
