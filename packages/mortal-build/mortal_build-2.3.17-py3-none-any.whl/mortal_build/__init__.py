# cython: language_level=3
# #!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/16 17:08
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
import os.path

from .build_main import MortalBuildMain


class MortalBuild(MortalBuildMain):
    def build_config(self):
        return self._build_config()

    def build_ext_wheel_pypi(self, config):
        self._build_ext_wheel_pypi(config)

    def build_ext_wheel(self, config):
        wheel_path = self._build_ext_wheel(config)
        return wheel_path

    def build_wheel(self, config):
        self._build_wheel(config)
