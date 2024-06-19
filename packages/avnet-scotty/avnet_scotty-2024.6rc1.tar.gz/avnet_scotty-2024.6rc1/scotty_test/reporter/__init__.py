# SPDX-FileCopyrightText: (C) 2023 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only
"""Reporter for scotty-test."""

import json
import logging
import os
import shutil
import subprocess
import tempfile
import time
from typing import Dict

from scotty_test.storage import StorageClient
from scotty_test.utils import Utils


class Reporter():
    """Create a test report."""

    def __init__(self, storage: StorageClient, version: str, results: Dict) -> None:
        """Construct a Reporter instance."""
        self.__storage = storage
        self.__version = version
        self.__results = results
        self.__branch_name = ''

        self.__scotty_path = os.path.join(
            self.__storage.local_storage(), '.scotty')

    def run(self) -> bool:
        """Entry point for Reporter class."""
        self.__setup_scotty()
        self.__create_branch()
        self.__convert_results()
        return self.__git_commit_and_publish()

    def __setup_scotty(self):
        if os.path.exists(self.__scotty_path):
            shutil.rmtree(self.__scotty_path, ignore_errors=True)
        os.makedirs(self.__scotty_path)

        logging.getLogger('scotty-test').info('Setup scotty... please wait')
        Utils.run(['scotty', 'update', '-b', 'kirkstone'],
                  cwd=self.__scotty_path)

    def __convert_results(self):
        for item in self.__results:
            result, testdata = item
            with tempfile.TemporaryDirectory() as t:
                with open(os.path.join(t, 'testresults.json'), 'w') as o:
                    json.dump(result, o)
                with open(os.path.join(t, 'testdata.json'), 'w') as o:
                    json.dump(testdata, o)
                Utils.run(['build/tools/scotty/validation/oeqa-report-enhancer',
                           self.__version,
                           t, 'build/tools/report'],
                          cwd=self.__scotty_path)

    def __create_branch(self):
        self.__branch_name = f'report/{self.__version}-{int(time.time())}'
        Utils.run(['git', 'checkout', '-b', self.__branch_name, 'avnet/kirkstone'],
                  cwd=os.path.join(self.__scotty_path, 'build', 'tools'),
                  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def __git_commit_and_publish(self) -> bool:
        res = Utils.run(['git', 'add', '*'],
                        cwd=os.path.join(self.__scotty_path, 'build', 'tools'),
                        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        res &= Utils.run(['git', 'commit', '-m', 'report: add test results'],
                         cwd=os.path.join(self.__scotty_path,
                                          'build', 'tools'),
                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        res &= Utils.run(['git', 'push', '-u', 'avnet', self.__branch_name],
                         cwd=os.path.join(self.__scotty_path,
                                          'build', 'tools'),
                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return res
