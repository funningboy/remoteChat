
import numpy as np
import cv2
import StringIO
from PIL import Image
import gevent
from jobs import *

class ImageBaseHandler(object):
    """ image base handler """

    debug = False

    def __init__(self, cfg):
        """ init """
        self._cfg = {
                'show_in_opt'   : False,
                'show_out_opt'  : False,
                'receive_opt'   : False,
                'send_opt'      : False,
                'work_opt'      : False,
                'ws'            : None, #websocket
                }
        self._channel = {
                'in'    : [],
                'out'   : [],
                }
        self._cfg.update(cfg)

    def update(self, cfg):
        """ update """
        self._cfg.update(cfg)

    def show_channel_in(self, wait=0.5):
        """ show channel in status """
        while True:
            if self._cfg['show_in_opt']:
                if len(self._channel['in']) > 0:
                    img = self._channel['in'][-1]
                    cv2.imshow('in', img)
                    cv2.waitKey(1)
            gevent.sleep(wait)

    def show_channel_out(self, wait=0.5):
        """ show channel out status """
        while True:
            if self._cfg['show_out_opt']:
                if len(self._channel['out']) > 0:
                    img = self._channel['out'][-1]
                    cv2.imshow('out', img)
                    cv2.waitKey(1)
            gevent.sleep(wait)

    def destory(self):
        """ destory """
        if self._cfg['receive_opt'] == True:
            self._cfg['receive_opt'] = Fasle
            self._channel['in'] = []

        if self._cfg['send_opt'] == True:
            self._cfg['send_opt'] = Fasle
            self._channel['out'] = []

        if self._cfg['show_in_opt'] == True or self._cfg['show_out_opt'] == True:
            self._cfg['show_in_opt'] = False
            self._cfg['show_out_opt'] = False
            cv2.destroyAllWindows('test')

    def receive(self, wait=0.5):
        """ receive video stream from websocket """
        while True:
            if self._cfg['receive_opt']:
                msg = self._cfg['ws'].receive()
                img = Image.open(StringIO.StringIO(msg))
                arr = np.array(img, dtype=np.uint8)
                self._channel['in'].append(arr)
            gevent.sleep(wait)

    def send(self, wait=0.5):
        """ send img to server """
        while True:
            if self._cfg['send_opt']:
                if len(self._channel['out']) > 0:
                    fp = StringIO.StringIO()
                    arr = self._channel['out'].pop()
                    img = Image.fromarray(arr)
                    img.save(fp, 'jpeg')
                    self._cfg['ws'].send(fp.getvalue().encode('base64'))
            gevent.sleep(wait)

    def work(self, wait=0.5):
        """ base work """
        while True:
            if self._cfg['work_opt']:
                if len(self._channel['in']):
                    img = self._channel['in'].pop()
                    self._channel['out'].append(img)
            gevent.sleep(wait)

    def warning(self, wait=0.5, max_in=1000, max_out=1000):
        while True:
            self._cfg['receive_opt'] = False if len(self._channel['in']) >= max_in else True
            self._cfg['send_opt'] = False if len(self._channel['out']) >= max_out else True
            gevent.sleep(wait)


class ImageJobHandler(ImageBaseHandler):
    """ image Job handler """

    def __init__(self, cfg={}):
        """ init """
        super(ImageJobHandler, self).__init__(cfg)
        self._cfg.update({
            'job' : 'DetectEdge',
            })

        self._jobs = {
                'DetectCircle' : DetectCircle,
                'DetectEdge'   : DetectEdge,
                'DetectFace'   : DetectFace,
                }

    def work(self, wait=0.5):
        """ base work """
        while True:
            if self._cfg['work_opt']:
                if len(self._channel['in']):
                    img = self._channel['in'].pop()
                    if self._cfg['job'] in self._jobs:
                        img = self._jobs[self._cfg['job']]().run(img)
                    self._channel['out'].append(img)
            gevent.sleep(wait)

    def update(self, cfg):
        """ update """
        self._cfg.update(cfg)

