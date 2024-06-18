# -*- coding: utf-8 -*-
"""
"""

import os

from pdfmergetk.configmanager import (
    ConfigManager,
    WindowsEnvironment,
    LinuxEnvironment,
    MacEnvironment
)


class InstallerPDFMergeTK:
    """
    """

    def install() -> None:
        """
        """
        config = ConfigManager()
        config.current_platform

        if config.current_platform == 'darwin':
            pass

        elif config.current_platform == 'linux':
            result = LinuxEnvironment.check_system_daemon()
            if result:
                LinuxEnvironment.create_desktop_file()

        elif config.current_platform == 'win32':
            run_path = os.path.join(config.path_config, ConfigManager.runfile)
            WindowsEnvironment.make_file_run(
                        name_app=ConfigManager.app,
                        file_runnable_path=run_path
                    )

            WindowsEnvironment.make_shortcut(
                        script_path=run_path
                    )

def main():
    InstallerPDFMergeTK.install()


if __name__ == '__main__':
    main()
