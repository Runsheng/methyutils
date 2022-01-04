#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/4/2022 3:13 PM
# @Author  : Runsheng     
# @File    : utils.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/8 16:58
# @Author  : Runsheng
# @File    : utils.py

import subprocess
import sys
import signal
import os
import fnmatch
import multiprocessing
import unittest
import gzip

from Bio import SeqIO

#### logger init
import logger
LOGGER=logger.get_logger()
####


def myexe(cmd, timeout=0):
    """
    a simple wrap of the shell
    mainly used to run the bwa mem mapping and samtool orders
    """
    def setupAlarm():
        signal.signal(signal.SIGALRM, alarmHandler)
        signal.alarm(timeout)

    def alarmHandler(signum, frame):
        sys.exit(1)

    LOGGER.info("running %s" % cmd)
    proc=subprocess.Popen(cmd, shell=True, preexec_fn=setupAlarm,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd=os.getcwd())
    out, err=proc.communicate()
    LOGGER.info(( err, "Run finished with return code:", proc.returncode))
    return out