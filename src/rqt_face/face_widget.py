#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuki Furuta <furushchev@jsk.imi.i.u-tokyo.ac.jp>

import math
import rospy
from rqt_face.face import Face
from python_qt_binding import QtGui
from python_qt_binding.QtGui import QWidget, QPainter
from std_msgs.msg import ColorRGBA
from rqt_face.msg import Emotion, Gaze


class FaceWidget(QWidget):
    def __init__(self):
        super(FaceWidget, self).__init__()
        self.face = Face(self.width(), self.height(), False)
        self.face.emotion = (0, 0, 0)
        self.face.look = (self.width() / 2.0, self.height() / 2.0)
        self.setMouseTracking(True)

        self.sub_emotion = rospy.Subscriber("face/emotion", Emotion, self.emotionCallback)
        self.sub_gaze = rospy.Subscriber("face/gaze", Gaze, self.gazeCallback)
        self.sub_color = rospy.Subscriber("face/color", ColorRGBA, self.colorCallback)

    def pad_from_screen_point(self, x, y):
        threshold = 0.55
        gain = 1.1

        w, h = self.width(), self.height()

        p =   (x - w / 2.0) / (w + 1.0) * 2.0 * gain
        d = - (y - h / 2.0) / (h + 1.0) * 2.0 * gain

        if abs(p) > threshold or abs(d) > threshold:
            if p == 0.0:
                if d > 0:
                    x1, y1, x2, y2 = 0, threshold, 0, 1
                else:
                    x1, y1, x2, y2 = 0, -threshold, 0, -1
            else:
                rc = d / p
                if p >= d:
                    if -p >= d:
                        y1, y2 = -threshold, -1
                        x1, x2 = y1 / rc, y2 / rc
                    else:
                        x1, x2 = threshold, 1
                        y1, y2 = x1 * rc, x2 * rc
                else:
                    if -p >= d:
                        x1, x2 = -threshold, -1
                        y1, y2 = x1 * rc, x2 * rc
                    else:
                        y1, y2 = threshold, 1
                        x1, x2 = y1 / rc, y2 / rc
            d1 = math.sqrt((x1-x2) ** 2 + (y1-y2) ** 2)
            a0 = math.sqrt((x1- p) ** 2 + (y1- d) ** 2)
            a = 2 * a0 / d1 - 1
        else:
            a = -1

        p = min(1, max(-1, p))
        a = min(1, max(-1, a))
        d = min(1, max(-1, d))

        return p, a, d

    ###### ROS Handlers
    def emotionCallback(self, msg):
        self.face.emotion = (msg.P, msg.A, msg.D)
        self.update()

    def gazeCallback(self, msg):
        x = (msg.x + 1.0) * self.width() / 2.0
        y = (msg.y + 1.0) * self.height() / 2.0
        self.face.look = (x, y)
        self.update()

    def colorCallback(self, msg):
        self.face.color = (int(v*255.0) for v in [msg.r, msg.g, msg.b])
        self.update()

    ###### EVent Handlers
    def paintEvent(self, event, ctx=None):
        if ctx is None:
            ctx = QPainter(self)
        self.face.paint(ctx)
        ctx.end()

    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        pad = self.pad_from_screen_point(x, y)
        self.face.emotion = pad
        self.face.look = (x, y)
        self.update()

    def resizeEvent(self, event):
        self.face.size = (event.size().width(), event.size().height())
        self.update()

    def closeEvent(self, event):
        rospy.logwarn("close event")
        self.sub_emotion.unregister()
        self.sub_gaze.unregister()
        self.sub_color.unregister()
        super(FaceWidget, self).closeEvent(event)

if __name__ == '__main__':
    pass
