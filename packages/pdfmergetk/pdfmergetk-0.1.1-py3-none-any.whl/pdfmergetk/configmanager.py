# -*- coding: utf-8 -*-
"""
ConfigManager : in charge to manages configuration of app.
"""

import os
import sys
import subprocess

import json

from typing import Union


class ConfigManager:
    """
    In charge to load, save configuration of app.
    """
    app = 'pdfmergetk'
    file = 'appconfig.json'
    runfile = 'run.py'

    def __init__(self) -> None:
        """
        Constructor
        """
        self.path_config = None
        self.path_config_file = None
        self.current_platform = None
        self.start()

    def start(self) -> None:
        """
        Main method in charge of obtaining platform, sets directory path and
        app configuration file.
        """
        self.current_platform = sys.platform.lower()

        if self.current_platform == 'darwin':
            path_config = os.path.join(
                            os.path.expanduser('~'),
                            "Library",
                            "Application Support",
                            ConfigManager.app
                        )

            # self.set_config_path(config=path_config)
            # creates shortcut to run app gui using a command
            # `mergepdf` or run script python.

        elif self.current_platform == 'linux':
            path_config = os.path.join(
                            os.path.expanduser('~'),
                            ".config",
                            ConfigManager.app
                        )

            # self.set_config_path(config=path_config)

            # result = LinuxEnvironment.check_system_daemon()
            # if result:
            #     LinuxEnvironment.create_desktop_file()

        elif self.current_platform == 'win32':
            path_config = os.path.join(
                            os.getenv('LOCALAPPDATA'),
                            ConfigManager.app
                        )

            # self.set_config_path(config=path_config)

            # run_path = os.path.join(path_config, ConfigManager.runfile)
            #
            # WindowsEnvironment.make_file_run(
            #         name_app=ConfigManager.app,
            #         file_runnable_path=run_path
            #     )
            #
            # WindowsEnvironment.make_shortcut(
            #         script_path=run_path
            #     )

        else:
            # Platform Error.
            path_config = None

        self.set_config_path(config=path_config)

    def set_config_path(
        self,
        config: str
    ) -> None:
        """
        """
        if config is not None:
            self.path_config = config
            self.path_config_file = os.path.join(
                                        self.path_config,
                                        ConfigManager.file
                                    )

            if not os.path.exists(self.path_config):
                os.makedirs(self.path_config)

    def save_config(
        self,
        config: dict
    ) -> None:
        """
        Saves configuration of app.
        """
        with open(self.path_config_file, 'w') as file:
            file.write(json.dumps(config))

    def load_config(self) -> Union[dict, None]:
        """
        Loads configuration of app.
        """
        try:
            with open(self.path_config_file, 'r') as file:
                return json.loads(file.readline())
        except FileNotFoundError:
            return None

    def __str__(self) -> str:
        """
        Returns a representation of instance.
        """
        return '<[ Config: %s, Plat: %s ]>' % (
                            self.path_config_file,
                            self.current_platform
                        )


class WindowsEnvironment:
    """
    """
    pythonw_base_dir = os.path.dirname(sys.executable)
    pythonw_path_exec = os.path.join(
                            pythonw_base_dir,
                            'pythonw.exe'
                        )

    def make_file_run(
        name_app: str,
        file_runnable_path: str
    ) -> None:
        """
        """
        string = """
import %s
if __name__ == '__main__':\n
    %s.gui.main()
        """ % (name_app, name_app)
        if not os.path.exists(file_runnable_path):
            with open(file_runnable_path, 'w') as fl:
                fl.writelines(string)

    def make_shortcut(
        script_path: str
    ) -> None:
        """
        """
        from win32com.client import Dispatch

        link_path = os.path.join(
                            WindowsEnvironment.get_desktop_path(),
                            'PDFMergeTK.lnk'
                        )

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(link_path)
        shortcut.TargetPath = WindowsEnvironment.pythonw_path_exec
        shortcut.Arguments = script_path
        shortcut.WorkingDirectory = WindowsEnvironment.pythonw_base_dir
        # shortcut.IconLocation = r"C:\path\to\your\icon.ico"  # Optional: specify an icon
        shortcut.save()

    def get_desktop_path() -> str:
        """
        """
        import winshell
        return winshell.desktop()


class LinuxEnvironment:
    """
    """
    command = 'ps -p 1 -o comm='
    path_desktop_file = os.path.join(
                            os.path.expanduser('~'),
                            ".local/share/applications/"
                        )

    def check_system_daemon() -> bool:
        """
        """
        result = subprocess.check_output(
                        args=LinuxEnvironment.command.split(" "),
                        text=True
                    )
        return result.strip().lower() in ['init', 'sysvinit', 'systemd']

    def create_desktop_file() -> None:
        """
        """
        file_desktop = """\
[Desktop Entry]
Name=PDFMergeTK
Comment=Merge PDFs
Exec=mergepdf
Terminal=false
StartupNotify=true
Type=Application
Categories=Utility;
        """
        name_file = 'PDFMergeTK.desktop'
        path_ = os.path.join(LinuxEnvironment.path_desktop_file, name_file)
        if not os.path.exists(path_):
            with open(path_, 'w') as file:
                file.writelines(file_desktop)
        LinuxEnvironment.update_desktop_file()

    def get_desktop_path() -> str:
        """
        """
        result = subprocess.check_output(['xdg-user-dir', 'DESKTOP'])
        return result.strip()

    def update_desktop_file() -> None:
        """
        """
        process = subprocess.run(args=[
                                    'update-desktop-database',
                                    LinuxEnvironment.path_desktop_file
                                ],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT
                            )
        process.returncode


class MacEnvironment:
    """
    I don't have a mac and I don't know how to do something similar to Linux or
    Windows.
    """
    pass
