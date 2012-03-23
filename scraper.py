import pandora
import getpass
import urllib2
import os
import time
import eyeD3
import sys
import random

def maxWidth(string, width):
  if len(string) <= width:
    return string
  else:
    return string[:width-3] + '...'

def scrape():
  pandora_connection = pandora.make_pandora()

  # email = raw_input("Email Address: ")
  email = 'zabu.other@gmail.com'

  loggedin = False
  while not loggedin:
    password = getpass.getpass("Password: ")
    print "Logging in..."
    try:
      pandora_connection.connect(email, password)
      loggedin = True
      print "Login Successful"
    except:
      print "Login failed"

  print "Requesting stations..."
  pandora_connection.get_stations()
  stations = pandora_connection.stations
  print "Stations recieved."
  print "Select a station"
  for i in range(len(stations)):
    print '\t[%2d] %s' % (i, stations[i].name)

  selection = int(raw_input("Enter selection: "))

  selected_station = stations[selection]

  print selected_station.name, "selected"

  song_count = 0
  for i in range(50):
    try:
      songs = selected_station.get_playlist()
    except pandora.PandoraError:
      print "Playlist request failed!"
      time.sleep(10)
      continue

    for song in songs:
      song_count += 1
      print u"[{:3d}]: {:>30} by {:<30}".format(song_count, 
                                                maxWidth(song.title, 30), 
                                                maxWidth(song.artist, 30))
      filename = os.getenv("HOME") + "/Music/"
      filename +=  song.artist.replace('/', '\\')
      try:
        os.mkdir(filename)
      except OSError:
        pass
      filename += '/' + song.album.replace('/', '\\')
      try:
        os.mkdir(filename)
      except OSError:
        pass
      filename += '/' + song.title.replace('/', '\\') + '.mp3'
      pandora_file = urllib2.urlopen(song.audioUrl)
      local_file = open(filename, 'w')
      local_file.write(pandora_file.read())
      local_file.close()
      pandora_file.close()

      t = eyeD3.Tag()
      t.link(filename)
      # audioFile = eyeD3.Mp3AudioFile(filename)
      # waitTime = audioFile.getPlayTime() / 2
      t.header.setVersion(eyeD3.ID3_V2_4)
      t.setArtist(song.artist)
      t.setAlbum(song.album)
      t.setTitle(song.title)
      tmp_file = open('/tmp/img.jpg', 'w')
      try:
        remote_image = urllib2.urlopen(song.artRadio)
        tmp_file.write(remote_image.read())
        remote_image.close()
        tmp_file.close()
        t.addImage(eyeD3.ImageFrame.FRONT_COVER, '/tmp/img.jpg')
      except:
        tmp_file.close()
        print "Unable to download album art"
      t.update()
      seconds = random.randint(60, 120)
      sys.stdout.write("Waiting for %d seconds" % seconds)
      sys.stdout.flush()
      waitTime = seconds
      while waitTime > 0:
        time.sleep(1)
        waitTime -= 1
        sys.stdout.write('.')
        sys.stdout.flush()
      print

