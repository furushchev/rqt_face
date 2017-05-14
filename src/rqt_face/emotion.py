#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuki Furuta <furushchev@jsk.imi.i.u-tokyo.ac.jp>

from collections import namedtuple
import math
import numpy as np

class EmotionGenerator(object):
    def __init__(self):
        self.emotions = np.array([
            [-1.0, -0.3,  1.0,  0.5, -1.0, -0.5,  0.3,  0.5,  0.0],  # eyes height
            [-1.0,  0.0,  1.0,  0.0, -1.0,  0.0,  1.0,  0.5,  0.0],  # space between eyes and brows
            [-1.0,  0.0, -0.8,  0.8,  0.0,  0.0,  0.0,  0.0,  0.0],  # eye brow outer height
            [ 1.0, -1.0,  0.8, -0.8,  0.0,  0.0,  0.0,  0.0,  0.0],  # eye brow inner height
            [-1.0, -1.0,  0.0,  1.0,  0.0,  0.0, -1.5,  1.0,  0.0],  # mouth width
            [-1.0, -0.5,  0.0,  1.0, -1.0, -0.5,  0.5,  0.5, -0.5],  # mouth openness
            [-1.0, -0.5, -0.3, -1.0,  0.7,  1.0,  0.5,  1.0,  0.0],  # mouth twist
            [ 1.0,  1.0,  0.5,  1.0,  1.0,  1.0, -0.5,  0.5,  1.0],  # teeth visible
            [-1.0, -1.0, -1.0, -1.0,  1.0,  1.0,  1.0,  1.0,  0.0],  # p value of emotions
            [-1.0, -1.0,  1.0,  1.0, -1.0, -1.0,  1.0,  1.0,  0.0],  # a value of emotions
            [-1.0,  1.0, -1.0,  1.0, -1.0,  1.0, -1.0,  1.0,  0.0],  # d value of emotions
        ]).T.tolist()
        # print self.emotions
        self.face_mixture_distances = [1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.7]

    def get(self, p, a, d):
        # interpolate emotion
        emotions = []
        for j in range(8):
            emotion = 0.0
            weight = 0.0
            for i in range(9):
                dist = self.face_mixture_distances[i]
                w = dist - min(dist, self.distance(p, a, d, self.emotions[i]))
                weight += w
                emotion += w * self.emotions[i][j]
            emotion /= weight if weight != 0.0 else 1.0
            emotions.append(emotion)
        return emotions

    def distance(self, p, a, d, emotion):
        return math.sqrt((p - emotion[8])  ** 2 +
                         (a - emotion[9])  ** 2 +
                         (d - emotion[10]) ** 2)

_GEN = EmotionGenerator()
def get_emotion(p, a, d):
    return _GEN.get(p, a, d)

if __name__ == '__main__':
    print get_emotion(-1.0, 1.0, -1.0)  # sad
