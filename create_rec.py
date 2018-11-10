#!/usr/local/bin/python
import os
import sys, getopt
from gluoncv import utils
import subprocess

def main(argv):
   try:
      opts, args = getopt.getopt(argv,"hp:r:",["prefix=","root="])
   except getopt.GetoptError:
      print 'create_rec.py -p <prefix> -r <root>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'create_rec.py -p <prefix> -r <root>'
         sys.exit()
      elif opt in ("-p", "--prefix"):
         prefix = arg
      elif opt in ("-r", "--root"):
         root = arg

   if os.path.isfile('im2rec.py'):
      print 'Using local im2rec.py'
   else:
      print 'Downloading im2rec.py'
      #im2rec = utils.download('https://raw.githubusercontent.com/apache/incubator-mxnet/' +
      #                  '6843914f642c8343aaa9a09db803b6af6f5d94a2/tools/im2rec.py', 'im2rec.py_orig')
      im2rec = utils.download('https://raw.githubusercontent.com/apache/incubator-mxnet/master/tools/im2rec.py', 'im2rec.py_new')
   subprocess.check_output([sys.executable, 'im2rec.py', prefix+'_train', root, '--pass-through', '--pack-label'])
   subprocess.check_output([sys.executable, 'im2rec.py', prefix+'_val', root, '--no-shuffle', '--pass-through', '--pack-label'])

if __name__ == "__main__":
   main(sys.argv[1:])

