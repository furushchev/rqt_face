#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuki Furuta <furushchev@jsk.imi.i.u-tokyo.ac.jp>

import math
from rqt_face.face import Face
from python_qt_binding import QtGui
from python_qt_binding.QtGui import (QWidget, QPainter)


class FaceWidget(QWidget):
    def __init__(self):
        super(FaceWidget, self).__init__()
        self.face = Face(150, 150)
        self.face.emotion = (-1, 1, -1)
        self.face.look = (0, 150)
        self.setMouseTracking(True)

    def paintEvent(self, event, ctx=None):
        if ctx is None:
            ctx = QPainter(self)
        self.face.paint(ctx)
        ctx.end()

    def pad_from_screen_point(self, x, y):
        threshold = 0.55
        gain = 1.1

        w, h = self.width(), self.height()
        w, h = 150, 150  # FIXME

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

    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        pad = self.pad_from_screen_point(x, y)
        self.face.emotion = pad
        self.face.look = (x, y)
        self.update()

if __name__ == '__main__':
    pass
