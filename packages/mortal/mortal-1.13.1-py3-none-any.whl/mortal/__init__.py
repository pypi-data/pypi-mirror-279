#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/16 17:08
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .build import MortalBuild
from .crypt import MortalCrypt
from .curl import MortalCurl
from .database import MortalExecute
from .database import MortalSQL
from .func import MortalFunc
from .ini import MortalIni
from .log import MortalLog
from .minio import MortalMinio
from .redis import MortalRedis
from .sftp import MortalSFTP
try:
    from .sqlparse import MortalParse
except(ImportError,):
    import os
    import re
    import ply
    old = "/" if os.name == 'nt' else "\\"
    new = "\\" if os.name == 'nt' else "/"
    old_path = r"\ply\__init__.py".replace(old, new)
    new_path = r"\mo_parsing\infix.py".replace(old, new)
    path = ply.__file__.replace(old_path, new_path)
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    with open(path, "w", encoding="utf-8") as f:
        old = "from collections import Iterable"
        new = "from collections.abc import Iterable"
        f.write(re.sub(old, new, data))
    from .sqlparse import MortalParse
from .ssh import MortalSSH
from .shell import MortalShell
from .threads import MortalThreads
from .timer import MortalTimer
from .var import MortalVar

MortalFunc()
