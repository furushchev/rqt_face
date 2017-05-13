#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuki Furuta <furushchev@jsk.imi.i.u-tokyo.ac.jp>

import math
from rqt_face.emotion import get_emotion
from python_qt_binding.QtGui import (QBrush, QColor, QPainter)
from python_qt_binding.QtCore import Qt

WHITE = QColor(255, 255, 255)
BLACK = QColor(  0,   0,   0)
LIGHTBLUE = QColor(0, 200, 200)
LIGHTRED = QColor(200, 100, 0)
NOBRUSH = Qt.NoBrush
NOPEN = Qt.NoPen


class Face(object):
    def __init__(self, width, height):
        self.color = (255, 200, 0)
        self.size = (width, height)
        self.look = (width / 2.0, height / 2.0)
        self.emotion = (0.0, 0.0, 0.0)

    @property
    def size(self):
        return (self.width, self.height)

    @size.setter
    def size(self, value):
        self.width, self.height = value

    @property
    def emotion(self):
        return self.p, self.a, self.d

    @emotion.setter
    def emotion(self, pad):
        self.p, self.a, self.d = pad
        self._emotion = get_emotion(*pad)

    @property
    def look(self):
        x = (self.look_x + 0.5) * self.width
        y = (self.look_y + 0.5) * self.height
        return x, y

    @look.setter
    def look(self, pt):
        self.look_x = 2.0 * pt[0] / self.width - 1.0
        self.look_y = 2.0 * pt[1] / self.height - 1.0

    @property
    def color(self):
        return self.face_color.red(), self.face_color.green(), self.face_color.blue()

    @color.setter
    def color(self, c):
        self.face_color = QColor(*c)

    def paint(self, ctx):
        assert isinstance(ctx, QPainter)

        base_eye_pos = (self.width / 4.0, self.height / 12.0)

        mx = (self.look_x + 1.0) / 2.0 * 7 - 1
        my = (self.look_y + 1.0) / 2.0 * 7 - 1

        fdx = (self.look_x + 1.0) / 2.0 * 6
        fdy = (self.look_y + 1.0) / 2.0 * 14 #  self.height / 10.0 - int((self.a + self.d) * self.height / 20.0)

        sx = 2
        sy = 2

        # face
        ctx.setBrush(self.face_color)
        ctx.setPen(NOPEN)
        ctx.drawEllipse(sx + 4, sy, self.width - 8, self.height)
        ctx.drawEllipse(sx + 4, sy, self.width - 8, int(self.height * 0.66))

        slex = fdx + sx + self.width / 2.0 - int(base_eye_pos[0] * 1.4)
        sley = fdy + sy + self.height / 3.0

        print "slex", slex, "sley", sley

        srex = fdx + sx + self.width / 2.0 + int(base_eye_pos[0] * 0.4)
        srey = fdy + sy + self.height / 3.0

        print "base_eye_pos", base_eye_pos

        eye_height     = int(base_eye_pos[1] * (1.0 + self._emotion[0]) + 2)
        eye_brow_space = int(base_eye_pos[1] * (1.0 + self._emotion[1] / 2.0) + 1)
        eye_brow_outer = int(-self._emotion[2] * base_eye_pos[1] / 2.0)
        eye_brow_inner = int(-self._emotion[3] * base_eye_pos[1] / 2.0)

        print "eye_height", eye_height
        print "eye", eye_brow_space, eye_brow_outer, eye_brow_inner

        # left eye
        ctx.setBrush(QBrush(WHITE))
        ctx.setPen(NOPEN)
        ctx.drawChord(slex, sley - eye_height / 2.0,
                      base_eye_pos[0], eye_height,
                      0, 360 * 16)

        ctx.setBrush(QBrush(LIGHTBLUE))
        ctx.setPen(NOPEN)
        ctx.drawChord(mx + slex + base_eye_pos[0] * 0.25, my + sley - base_eye_pos[0] / 4.0,
                      base_eye_pos[0] / 2.0, base_eye_pos[0] / 2.0,
                      0, 360 * 16)

        ctx.setBrush(QBrush(BLACK))
        ctx.setPen(NOPEN)
        ctx.drawChord(mx + slex + base_eye_pos[0] * 0.40, my + sley - base_eye_pos[0] / 10.0,
                      base_eye_pos[0] / 5.0, base_eye_pos[0] / 5.0,
                      0, 360 * 16)

        ctx.fillRect(slex, sley - eye_height / 2.0 - base_eye_pos[0] / 2.0,
                     base_eye_pos[0], base_eye_pos[0] / 2.0,
                     self.face_color)
        ctx.fillRect(slex, sley + eye_height / 2.0,
                     base_eye_pos[0], base_eye_pos[0] / 2.0,
                     self.face_color)

        # left eye brow
        ctx.setPen(BLACK)
        ctx.drawLine(slex, sley - eye_brow_space + eye_brow_outer,
                     slex + base_eye_pos[0], sley - eye_brow_space + eye_brow_inner)
        ctx.drawLine(slex, 1 + sley - eye_brow_space + eye_brow_outer,
                     slex + base_eye_pos[0], 1 + sley - eye_brow_space + eye_brow_inner)

        # right eye
        ctx.setBrush(QBrush(WHITE))
        ctx.setPen(NOPEN)
        ctx.drawChord(srex, srey - eye_height / 2.0,
                      base_eye_pos[0], eye_height,
                      0, 360 * 16)

        ctx.setBrush(QBrush(LIGHTBLUE))
        ctx.setPen(NOPEN)
        ctx.drawChord(mx + srex + base_eye_pos[0] * 0.25, my + srey - base_eye_pos[0] / 4.0,
                      base_eye_pos[0] / 2.0, base_eye_pos[0] / 2.0,
                      0, 360 * 16)

        ctx.setBrush(QBrush(BLACK))
        ctx.setPen(NOPEN)
        ctx.drawChord(mx + srex + base_eye_pos[0] * 0.40, my + srey - base_eye_pos[0] / 10.0,
                      base_eye_pos[0] / 5.0, base_eye_pos[0] / 5.0,
                      0, 360 * 16)

        ctx.fillRect(srex, srey - eye_height / 2.0 - base_eye_pos[0] / 2.0,
                     base_eye_pos[0], base_eye_pos[0] / 2.0,
                     self.face_color)
        ctx.fillRect(srex, srey + eye_height / 2.0,
                     base_eye_pos[0], base_eye_pos[0] / 2.0,
                     self.face_color)

        # right eye brow
        ctx.setPen(BLACK)
        ctx.drawLine(srex, srey - eye_brow_space + eye_brow_inner,
                     srex + base_eye_pos[0], srey - eye_brow_space + eye_brow_outer)
        ctx.drawLine(srex, 1 + srey - eye_brow_space + eye_brow_inner,
                     srex + base_eye_pos[0], 1 + srey - eye_brow_space + eye_brow_outer)

        # mouth
        base_mouth_pos = (self.width / 2.0, self.height / 6.0)
        smx = fdx + sx + self.width / 2.0
        smy = fdy + sy + 2.0 * self.height / 3.0
        mw = int(base_mouth_pos[0] * (self._emotion[4] + 4) / 6.0)
        mo = int(base_mouth_pos[1] * (self._emotion[5] + 1) / 3.0)
        mt = int(base_mouth_pos[1] * (self._emotion[6] + 0) / 2.0)
        tv = int(base_mouth_pos[1] * (self._emotion[7] - 1) / 3.0)

        print "m", mw, mo, mt, tv

        upper_lip = mt - mo
        lower_lip = mt + mo
        shift = -mt

        print "lip", upper_lip, lower_lip

        print mw, mo, mt, tv
        print upper_lip, lower_lip

        if upper_lip > 0:
            if lower_lip > 0:
                ctx.setBrush(QBrush(WHITE))
                ctx.setPen(NOPEN)
                ctx.drawChord(smx - mw / 2.0, shift + smy - lower_lip,
                              mw, lower_lip * 2.0,
                              -180 * 16, 180 * 16)
            else:
                ctx.setBrush(QBrush(self.face_color))
                ctx.setPen(NOPEN)
                ctx.drawChord(smx - mw / 2.0, shift + smy + lower_lip,
                              mw, -lower_lip * 2.0,
                              0, 180 * 16)
            ctx.setBrush(QBrush(self.face_color))
            ctx.setPen(NOPEN)
            ctx.drawChord(smx - mw / 2.0, shift + smy - upper_lip,
                          mw, upper_lip * 2.0,
                          -180 * 16, 180 * 16)
        else:
            ctx.setBrush(QBrush(WHITE))
            ctx.setPen(NOPEN)
            ctx.drawChord(smx - mw / 2.0, shift + smy + upper_lip,
                          mw, -upper_lip * 2.0,
                          0, 180 * 16)
            if lower_lip > 0:
                ctx.setBrush(QBrush(WHITE))
                ctx.setPen(NOPEN)
                ctx.drawChord(smx - mw / 2.0, shift + smy + lower_lip,
                              mw, lower_lip * 2,
                              -180*16, 180*16)
            else:
                ctx.setBrush(QBrush(self.face_color))
                ctx.setPen(NOPEN)
                ctx.drawChord(smx - mw / 2.0, shift + smy + lower_lip,
                              mw, -lower_lip * 2.0,
                              0, 180 * 16)

        ctx.fillRect(smx - mw / 2.0, smy + tv, mw, -tv * 2, self.face_color)

        return

        # teeth
        ctx.setPen(self.face_color)
        for i in range(6):
            ctx.drawLine(smx - base_mouth_pos[0] * (0.5 - i * 0.2), smy - math.fabs(mt) - mo,
                         smx - base_mouth_pos[0] * (0.5 - i * 0.2), smy + math.fabs(mt) + mo)
        ctx.drawLine(smx - base_mouth_pos[0] / 2.0, smy,
                     smx + base_mouth_pos[0] / 2.0, smy)

        # lips
        ctx.setBrush(NOBRUSH)
        ctx.setPen(LIGHTRED)
        if upper_lip > 0:
            ctx.drawArc(smx - mw / 2, shift + smy - upper_lip,
                        mw, upper_lip * 2,
                        -180 * 16, 180 * 16)
        else:
            ctx.drawArc(smx - mw / 2, shift + smy + upper_lip,
                        mw, -upper_lip * 2,
                        0, 180 * 16)
        if lower_lip > 0:
            ctx.drawArc(smx - mw / 2, shift + smy - upper_lip,
                        mw, lower_lip * 2,
                        -180 * 16, 180 * 16)
        else:
            ctx.drawArc(smx - mw / 2, shift + smy + lower_lip,
                        mw, -lower_lip * 2,
                        0, 180 * 16)


if __name__ == '__main__':
    pass
