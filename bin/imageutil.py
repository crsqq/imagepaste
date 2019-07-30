"""
for Linux use
pip install PyUserInput, pyscreenshot 
and install python-pyqt4 as backend of pyscreenshot
"""
import sys
import os
from PIL import Image
import pyscreenshot as ImageGrab
from pymouse import PyMouse
from pymouse import PyMouseEvent
import time

import subprocess

class event(PyMouseEvent):
	def __init__(self):
		super(event, self).__init__()
		self.clicks = []
		# FORMAT = '%(asctime)-15s ' + gethostname() + ' touchlogger %(levelname)s %(message)s'
		# logging.basicConfig(filename='/var/log/mouse.log', level=logging.DEBUG, format=FORMAT)

	def move(self, x, y):
		pass

	def click(self, x, y, button, press):
		if press:
			# print('{ "event": "click", "type": "press", "x": "' + str(x) + '", "y": "' + str(y) + '"}') 
			self.clicks.append((x, y))
		else:
			pass
			# print('{ "event": "click", "type": "release", "x": "' + str(x) + '", "y": "' + str(y) + '"}') 




def getSize(filename):
	with Image.open(filename) as im:
		# print("file: %s with size: %d %d" % (file1, im.width, im.height))
		return (im.width, im.height)



def call_cmd(cmd_args):
    p = subprocess.Popen(cmd_args, stdout=subprocess.PIPE)
    return p.stdout.read()


def getClipboardData():
    xclip_targets = call_cmd("xclip -selection clipboard -o -t TARGETS".split(" ")).decode().split("\n")

    ft = None
    if 'image/png' in xclip_targets:
        ft = 'png'
    elif 'image/jpeg' in xclip_targets:
        ft = 'jpeg'
    else:
        raise Exception('filetype not png or jpeg')

    get_image_args = ['xclip','-selection', 'clipboard', '-o', '-t', 'image/' + ft]
    im = call_cmd(get_image_args)
    return im, ft


def saveImagefile(filename):
	im,ft = getClipboardData()
	filename = "".join(filename.split(".")[:-1])
	if im:
		print("save")
		with open(filename + '.' + ft, 'wb') as f:
			f.write(im)
		#im.save(filename)
		return 0
	else:
		return 1

def saveImagefile2(filename, pt1, pt2):
	im = ImageGrab.grab(bbox=(pt1[0], pt1[1], pt2[0], pt2[1]))
	if im:
		print("grab %r %r %r" % (filename, pt1, pt2))
		# ret = im.show()
		# print("ret %r" % (ret))
		im.save(filename)
		return 0
	else:
		return 1

# print(__name__, sys.argv)
if __name__ == '__main__':
	if len(sys.argv) == 3:
		# python imageutil.py size filename
		# print("begin %r" % sys.stdin.encoding)
		if sys.argv[1] == 'size':
			print("%d,%d" % getSize(sys.argv[2]))
		elif sys.argv[1] == 'save':
			print(saveImagefile(sys.argv[2]))
		elif sys.argv[1] == 'grab':
			# print("grab123 %s" % os.environ.get('DISPLAY', ':0'))
			e = event()
			e.capture = False
			e.daemon = True
			e.start()

			while(True):
				time.sleep(1)
				if len(e.clicks) == 2:
					saveImagefile2(sys.argv[2], e.clicks[0], e.clicks[1])
					break;

		# print("end")
