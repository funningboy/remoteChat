

#import gevent
#from zmq import green as zmq
#import numpy as np
#import cv2
#import json
#
#
#class Server(object):
#    """ Server as publisher """
#
#    def __init__(self, context):
#        self._context = context
#        self._socket = self._context.socket(zmq.PUSH)
#        self._img = []
#
#    def setup_ip(self, addr='inproc://polltest1'):
#        """ setup ip """
#        self._socket.connect(addr)
#
#    def receive_imgs(self, wait=0.5):
#
#    def broadcast_imgs(self, wait=0.5):
#
#    def send_imgs
