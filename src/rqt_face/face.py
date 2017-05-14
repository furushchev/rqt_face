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
    def __init__(self, width, height, draw_contour=True):
        self.draw_contour = draw_contour
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

        mx_factor = self.width / 150.0 * 7
        my_factor = self.height / 150.0 * 7
        mx = (self.look_x + 1.0) / 2.0 * mx_factor - 1
        my = (self.look_y + 1.0) / 2.0 * my_factor - 1

        fdx = (self.look_x + 1.0) / 2.0 * 6
        fdy = (self.look_y + 1.0) / 2.0 * 14

        sx = 2
        sy = 2

        # face
        if self.draw_contour:
            ctx.setBrush(self.face_color)
            ctx.setPen(NOPEN)
            ctx.drawEllipse(sx + 4, sy, self.width - 8, self.height)
            ctx.drawEllipse(sx + 4, sy, self.width - 8, int(self.height * 0.66))
        else:
            ctx.fillRect(0, 0, self.width, self.height, self.face_color)

        left_eye_center = fdx + sx + self.width / 2.0, fdy + sy + self.height / 3.0
        right_eye_center = fdx + sx + self.width / 2.0, fdy + sy + self.height / 3.0
        eye_height     = int(base_eye_pos[1] * (1.0 + self._emotion[0]) + 2)
        pupil_radius   = int(base_eye_pos[0] / 4.0)
        eye_brow_space = int(base_eye_pos[1] * (1.0 + self._emotion[1] / 2.0) + 1)
        eye_brow_outer = int(-self._emotion[2] * base_eye_pos[1] / 2.0)
        eye_brow_inner = int(-self._emotion[3] * base_eye_pos[1] / 2.0)
        eye_brow_boldness = 2

        # left eye
        left_eye_offset_x = -int(base_eye_pos[0] * 1.4)
        ctx.setBrush(QBrush(WHITE))
        ctx.setPen(NOPEN)
        ctx.drawChord(left_eye_center[0] + left_eye_offset_x, left_eye_center[1] - eye_height / 2.0,
                      base_eye_pos[0], eye_height,
                      0, 360 * 16)

        ctx.setBrush(QBrush(LIGHTBLUE))
        ctx.setPen(NOPEN)
        ctx.drawChord(left_eye_center[0] + left_eye_offset_x + mx + base_eye_pos[0] * 0.5 - pupil_radius / 2.0,
                      left_eye_center[1] + my - pupil_radius / 2.0,
                      pupil_radius, pupil_radius,
                      0, 360 * 16)

        ctx.setBrush(QBrush(BLACK))
        ctx.setPen(NOPEN)
        ctx.drawChord(left_eye_center[0] + left_eye_offset_x + mx + base_eye_pos[0] * 0.5 - pupil_radius / 5.0,
                      left_eye_center[1] + my - pupil_radius / 5.0,
                      pupil_radius / 2.5, pupil_radius / 2.5,
                      0, 360 * 16)

        ctx.fillRect(left_eye_center[0] + left_eye_offset_x,
                     left_eye_center[1] - eye_height / 2.0 - base_eye_pos[0] / 2.0,
                     base_eye_pos[0], base_eye_pos[0] / 2.0,
                     self.face_color)
        ctx.fillRect(left_eye_center[0] + left_eye_offset_x,
                     left_eye_center[1] + eye_height / 2.0,
                     base_eye_pos[0], base_eye_pos[0] / 2.0,
                     self.face_color)

        # left eye brow
        ctx.setPen(BLACK)
        for b in range(eye_brow_boldness):
            ctx.drawLine(left_eye_center[0] + left_eye_offset_x,
                         left_eye_center[1] - eye_brow_space + eye_brow_outer + b,
                         left_eye_center[0] + left_eye_offset_x + base_eye_pos[0],
                         left_eye_center[1] - eye_brow_space + eye_brow_inner + b)

        # right eye
        right_eye_offset_x = int(base_eye_pos[0] * 0.4)
        ctx.setBrush(QBrush(WHITE))
        ctx.setPen(NOPEN)
        ctx.drawChord(right_eye_center[0] + right_eye_offset_x,
                      right_eye_center[1] - eye_height / 2.0,
                      base_eye_pos[0], eye_height,
                      0, 360 * 16)

        ctx.setBrush(QBrush(LIGHTBLUE))
        ctx.setPen(NOPEN)
        ctx.drawChord(right_eye_center[0] + right_eye_offset_x + mx + base_eye_pos[0] * 0.5 - pupil_radius / 2.0,
                      right_eye_center[1] + my - pupil_radius / 2.0,
                      pupil_radius, pupil_radius,
                      0, 360 * 16)

        ctx.setBrush(QBrush(BLACK))
        ctx.setPen(NOPEN)
        ctx.drawChord(mx + right_eye_center[0] + right_eye_offset_x + base_eye_pos[0] * 0.5 - pupil_radius / 5.0,
                      my + right_eye_center[1] - pupil_radius / 5.0,
                      pupil_radius / 2.5, pupil_radius / 2.5,
                      0, 360 * 16)

        ctx.fillRect(right_eye_center[0] + right_eye_offset_x,
                     right_eye_center[1] - eye_height / 2.0 - base_eye_pos[0] / 2.0,
                     base_eye_pos[0], base_eye_pos[0] / 2.0,
                     self.face_color)
        ctx.fillRect(right_eye_center[0] + right_eye_offset_x,
                     right_eye_center[1] + eye_height / 2.0,
                     base_eye_pos[0], base_eye_pos[0] / 2.0,
                     self.face_color)

        # right eye brow
        ctx.setPen(BLACK)
        for b in range(eye_brow_boldness):
            ctx.drawLine(right_eye_center[0] + right_eye_offset_x,
                         right_eye_center[1] - eye_brow_space + eye_brow_inner + b,
                         right_eye_center[0] + right_eye_offset_x + base_eye_pos[0],
                         right_eye_center[1] - eye_brow_space + eye_brow_outer + b)

        # mouth
        base_mouth_pos = (self.width / 2.0, self.height / 6.0)
        smx = fdx + sx + self.width / 2.0
        smy = fdy + sy + 2.0 * self.height / 3.0
        mw = int(base_mouth_pos[0] * (self._emotion[4] + 4) / 6.0)
        mo = int(base_mouth_pos[1] * (self._emotion[5] + 1) / 3.0)
        mt = int(base_mouth_pos[1] * (self._emotion[6] + 0) / 2.0)
        tv = int(base_mouth_pos[1] * (self._emotion[7] - 1) / 3.0)

        upper_lip = mt - mo
        lower_lip = mt + mo
        shift = -mt

        if upper_lip > 0:
            if lower_lip > 0:
                ctx.setBrush(QBrush(WHITE))
                ctx.setPen(NOPEN)
                ctx.drawChord(smx - mw / 2, shift + smy - lower_lip,
                              mw, lower_lip * 2,
                              -180 * 16, 180 * 16)
            else:
                ctx.setBrush(QBrush(self.face_color))
                ctx.setPen(NOPEN)
                ctx.drawChord(smx - mw / 2, shift + smy + lower_lip,
                              mw, -lower_lip * 2,
                              0, 180 * 16)
            ctx.setBrush(QBrush(self.face_color))
            ctx.setPen(NOPEN)
            ctx.drawChord(smx - mw / 2, shift + smy - upper_lip,
                          mw, upper_lip * 2,
                          -180 * 16, 180 * 16)
        else:
            ctx.setBrush(QBrush(WHITE))
            ctx.setPen(NOPEN)
            ctx.drawChord(smx - mw / 2, shift + smy + upper_lip,
                          mw, -upper_lip * 2,
                          0, 180 * 16)
            if lower_lip > 0:
                ctx.setBrush(QBrush(WHITE))
                ctx.setPen(NOPEN)
                ctx.drawChord(smx - mw / 2, shift + smy - lower_lip,
                              mw, lower_lip * 2,
                              -180 * 16, 180 * 16)
            else:
                ctx.setBrush(QBrush(self.face_color))
                ctx.setPen(NOPEN)
                ctx.drawChord(smx - mw / 2, shift + smy + lower_lip,
                              mw, -lower_lip * 2,
                              0, 180 * 16)

        ctx.fillRect(smx - mw / 2.0, smy + tv, mw, -tv * 2, self.face_color)

        # teeth
        ctx.setPen(self.face_color)
        for i in range(6):
            ctx.drawLine(smx - base_mouth_pos[0] * (0.5 - i * 0.2), smy - abs(mt) - mo,
                         smx - base_mouth_pos[0] * (0.5 - i * 0.2), smy + abs(mt) + mo)
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
            ctx.drawArc(smx - mw / 2, shift + smy - lower_lip,
                        mw, lower_lip * 2,
                        -180 * 16, 180 * 16)
        else:
            ctx.drawArc(smx - mw / 2, shift + smy + lower_lip,
                        mw, -lower_lip * 2,
                        0, 180 * 16)


if __name__ == '__main__':
    pass
