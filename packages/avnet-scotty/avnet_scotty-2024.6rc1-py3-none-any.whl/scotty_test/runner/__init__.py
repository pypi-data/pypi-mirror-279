# SPDX-FileCopyrightText: (C) 2023 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only

"""Test runnner for scotty-test."""

import json
import logging
import os
import re
import time
import zipfile
from typing import Dict, List, Tuple

from scotty_test.menu import show_editor, show_menu
from scotty_test.storage import StorageClient
from scotty_test.utils import Utils


class SDCardHandler():
    """Abstract handler for SDCards."""

    def is_already_flashed(self, image: str) -> bool:
        """Return if the image is already flashed to SD."""
        return False

    def get_menu_options(self) -> List[Tuple[str, str]]:
        """Return the potentialy SD devices."""
        raise NotImplementedError()

    def run(self, device: str, file: str) -> bool:
        """Run the flashing procedure."""
        raise NotImplementedError()


class SDCardManualHandler(SDCardHandler):
    """Handle manual SDCard flashing."""

    def get_menu_options(self) -> List[Tuple[str, str]]:
        """Return the potentialy SD devices."""
        res = set()
        for f in os.listdir('/dev'):
            # match /dev/mmc[0-9] /dev/mmcblk[0-9] and /dev/sd[a-z]
            if re.match(r'^(mmc[0-9]|mmcblk[0-9]|sd[a-z])$', f):
                path = os.path.join('/dev', f)
                res.add((path, path))
        return list(res)

    def run(self, device: str, file: str) -> bool:
        """Run the flashing procedure wih dd."""
        return Utils.run_interactive(
            [f'sudo dd if={file} of={device} bs=64M']) is not None

    def is_already_flashed(self, image: str) -> bool:
        """Return if the image is already flashed to SD."""
        return show_menu(f'Is {image} already flashed to the SDCard?', entries=[('Yes', True), ('No', False)])


class SDCardSDWireHandler(SDCardHandler):
    """Handle SDCard flashing with SDWire."""


class Runner():
    """Test runner implementation."""

    def __init__(self, storage: StorageClient, version: str, machine: str, image_dict: dict, sdhandler: str, sdk: str) -> None:
        """Construct the runner."""
        self.__storage = storage
        self.__machine = machine
        self.__version = version
        self.__sdk_path = sdk
        self.__overlays = set()
        self.__image_name = list(image_dict.keys())[0]
        self.__image_dict = image_dict[self.__image_name]
        self.__sdhandler = SDCardSDWireHandler(
        ) if sdhandler == 'sdwire' else SDCardManualHandler()
        self.__results = {}
        self.__testdata = {}

    def run(self) -> Dict:
        """Entry point for the Runner implementation."""
        Utils.do_in_tempdir(self._prepare_sd)
        Utils.do_in_tempdir(self._do_testrun)
        with open(f'{self.__machine}-{self.__image_name}-{time.time_ns()}-testresults.json', 'w') as o:
            json.dump(self.__results, o)
        return (self.__results, self.__testdata)

    def _unpack_zip(self, path: str):
        file = self.__storage.download(self.__version + path)
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
        return os.getcwd()

    def _find_testexport_dir(self, basedir: str, needle: str) -> str:
        for root, dirs, _ in os.walk(basedir):
            for d in dirs:
                if d == needle:
                    return os.path.join(root, d)
        return '/does/not/exist'

    def _find_wic_file(self, basedir: str, needle: str) -> str:
        for root, _, files in os.walk(basedir):
            for f in files:
                if f == needle:
                    return os.path.join(root, f)
        return '/does/not/exist'

    def _find_sdk_installer(self, basedir: str) -> str:
        for root, _, files in os.walk(basedir):
            for f in files:
                if f.endswith('.sh'):
                    return os.path.join(root, f)
        return '/does/not/exist'

    def _find_overlays(self, basedir: str) -> List[str]:
        res = set()
        for _, _, files in os.walk(basedir):
            for f in files:
                if f.endswith('.dtb'):
                    if not f.startswith('overlay-'):
                        continue
                    if f'-{self.__machine}' in f:
                        continue
                    res.add(f)
        return res

    def _configure_overlays(self, selected_overlays: List[str], ip: str, folder: str) -> bool:
        overlay_str = "fdt_overlay=" + " ".join(selected_overlays)

        # patch testdata.json
        with open(os.path.join(folder, 'data', 'testdata.json'), 'r') as f:
            cnt = json.load(f)

        cnt['UBOOT_ENV_VARS'] = overlay_str

        with open(os.path.join(folder, 'data', 'testdata.json'), 'w') as f:
            json.dump(cnt, f, sort_keys=True, indent=2)

        self.__testdata = cnt

        ssh_cmd = ['ssh', '-l', 'root', '-o', 'StrictHostKeyChecking=no',
                   '-o', 'UserKnownHostsFile=/dev/null', ip,
                   f'[ -e /boot/uEnv.txt ] && echo "{overlay_str}" >> /boot/uEnv.txt && /sbin/reboot']
        return Utils.run(ssh_cmd)

    def _prepare_sdk(self) -> Dict:
        def get_sdk_environ(path):
            logging.getLogger(
                'scotty-test').info('Sourcing SDK, please wait...')
            res = {}
            out = Utils.run_output(
                [f'. {path}/environment-setup* > /dev/null && printenv'], shell=True)
            for line in out[1].split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    res[key] = value
            return res

        if not self.__sdk_path:
            _sdk = self.__image_dict.get('sdk')
            if _sdk:
                _sdk_version = self.__storage.blob_hash(self.__version + _sdk)
                _sdk_local_path = os.path.join(
                    self.__storage.local_storage(), '.sdk', f'{self.__machine}-{_sdk_version}')
                if not os.path.exists(_sdk_local_path):
                    _dir = self._unpack_zip(_sdk)
                    _file = self._find_sdk_installer(_dir)
                    if not os.access(_file, os.X_OK):
                        os.chmod(_file, 0o755)
                    logging.getLogger(
                        'scotty-test').info('Installing SDK, please wait...')
                    Utils.run(f'{_file} -y -d {_sdk_local_path}', shell=True)
                return get_sdk_environ(_sdk_local_path)
        else:
            return get_sdk_environ(self.__sdk_path)
        return {}

    def _handle_hw_map(self, testexport_dir: str) -> None:
        # patch testdata.json
        with open(os.path.join(testexport_dir, 'data', 'testdata.json'), 'r') as f:
            cnt = json.load(f)

        # always patch TOPDIR
        cnt['TOPDIR'] = testexport_dir

        # set interactive
        cnt['INTERACTIVE_TEST'] = '1'

        # find HW_TESTING_MAP
        hw_map = json.loads(cnt.get('HW_TESTING_MAP_ORIG', '{}'))
        hw_map = {k: v for k, v in hw_map.items()}
        if any(k for k, v in hw_map.items() if v != -1):
            hw_map_selection = show_menu("Please choose the features your base board offers", [
                                         (k, k) for k, v in hw_map.items() if v != -1], True)
        for item in hw_map_selection:
            hw_map[item] = 1

        cnt['HW_TESTING_MAP'] = json.dumps(hw_map, sort_keys=True)

        with open(os.path.join(testexport_dir, 'data', 'testdata.json'), 'w') as f:
            json.dump(cnt, f, sort_keys=True, indent=2)

        self.__testdata = cnt

    def _do_testrun(self) -> Dict:
        _cur_environ = os.environ.copy()
        logging.getLogger('scotty-test').info('Preparing the SDK...')
        os.environ.update(self._prepare_sdk())
        _dir = self._unpack_zip(self.__image_dict.get('testexport'))
        _folder = self._find_testexport_dir(_dir, self.__image_name)
        self._handle_hw_map(_folder)
        ip = show_editor('Power up the board and tell us the IP')
        if self.__overlays:
            _selected_overlays = show_menu(
                "Please select the matching overlays", [(x, x) for x in self.__overlays], True)
        elif self.__machine in ['sm2s-intel-all']:
            _selected_overlays = [show_menu(
                "What base board are you using?", [
                    ('EP5-001', 'overlay-baseboard-ep5-gpioexpander.dtb'),
                    ('EP5-002', 'overlay-baseboard-ep5.dtb'),
                    ('EP1', 'overlay-baseboard-ep1.dtb'),
                ])]
        else:
            _selected_overlays = [show_editor("Enter the to be used overlays")]
        self._configure_overlays(_selected_overlays, ip, _folder)

        logging.getLogger('scotty-test').info('Waiting for reboot...')
        time.sleep(15.0)

        os.chmod(os.path.join(_folder, 'oe-test'), 0o755)
        os.chdir(_folder)
        logging.getLogger('scotty-test').info('Starting tests...')
        Utils.run_interactive(f'./oe-test runtime --target-ip={ip}')
        with open(os.path.join(_folder, 'runtime-results/testresults.json')) as i:
            self.__results = json.load(i)
        os.environ = _cur_environ

    def _prepare_sd(self):
        if not self.__sdhandler.is_already_flashed(self.__image_name):
            _selected_device = None
            while not _selected_device:
                _selected_device = show_menu(
                    'Please select the SDCard device', entries=self.__sdhandler.get_menu_options() + [('Rescan', None)])
            _dir = self._unpack_zip(self.__image_dict.get('image'))
            _file = self._find_wic_file(
                _dir, f'{self.__image_name}-{self.__machine}.wic')
            logging.getLogger('scotty-test').info('Flashing SDCard...')
            while not self.__sdhandler.run(_selected_device, _file):
                pass
            self.__overlays = self._find_overlays(_dir)
