#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuki Furuta <furushchev@jsk.imi.i.u-tokyo.ac.jp>


from rqt_gui_py.plugin import Plugin
from rqt_face.face_widget import FaceWidget


class FacePlugin(Plugin):
    def __init__(self, ctx):
        super(FacePlugin, self).__init__(ctx)
        self.setObjectName("Face")
        self._widget = FaceWidget()
        ctx.add_widget(self._widget)

if __name__ == '__main__':
    pass
