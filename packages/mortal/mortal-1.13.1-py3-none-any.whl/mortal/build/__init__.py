#!/usr/bin/env python
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
    def build(
            self, path, name, desc, version, author, long_desc, long_desc_type,
            requires, skip_dir: list = None, resume=False, replace=False
    ):
        self._build_ext(path, skip_dir, resume)
        wheel_path = os.path.join(self._be_tgt_path, os.path.basename(path))
        self._build_wheel(
            wheel_path, name, desc, version, author, long_desc, long_desc_type, requires, skip_dir, replace
        )
        return self._copy_wheel_dist()

    def build_ext(self, path, skip_dir: list = None, resume=False):
        self._build_ext(path, skip_dir, resume)

    def build_wheel(
            self, path, name, desc, version, author, long_desc, long_desc_type,
            requires, skip_dir: list = None, replace=False
    ):
        self._build_wheel(path, name, desc, version, author, long_desc, long_desc_type, requires, skip_dir, replace)
