#/usr/bin/env python

import urllib
import sys
import os

class AppURLopener(urllib.FancyURLopener):
  version = "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101230 Mandriva Linux/1.9.2.13-0.2mdv2010.2 (2010.2) Firefox/3.6.13"

def main():
  if len(sys.argv) < 2:
    print 'Usage: {prog} URL'.format(prog = sys.argv[0])
    sys.exit(1)

  video_id = sys.argv[1]

  opener = AppURLopener()
  fp = opener.open('http://www.youtube.com/get_video_info?video_id={vid}'.format(vid = video_id))
  data = urllib.unquote(urllib.unquote(fp.read()))
  fp.close()

  if data.startswith('status=fail'):
    print 'Error: Video not found!'
    sys.exit(2)

  link = data[data.find('url=http://')+4:]
  link = link[:link.find('"')]

  fp = opener.open(link)
  data = fp.read(1024)
  while data:
    sys.stdout.write(data)
    data = fp.read(1024)
  fp.close()

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass