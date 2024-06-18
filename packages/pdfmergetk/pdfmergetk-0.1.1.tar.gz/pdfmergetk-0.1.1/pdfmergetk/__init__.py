# -*- coding: utf-8 -*-
"""
PDFMergeTK application.
"""

from pdfmergetk.gui import main

from pdfmergetk.gui import (
    ElementsTK,
    LanguagesClass,
    LoadImagePDFThread,
    MainGUI,
    UserListBox,
    DisplayCanvas,
    AvoidOpeningThemMultipleTimes,
    WarningOpenedApp
)

from pdfmergetk.styles import AppStyles
from pdfmergetk.langs import languagesDict
from pdfmergetk.reader import ReaderPDFImage
from pdfmergetk.models import PDFile
from pdfmergetk.dataclass import Data
from pdfmergetk.configmanager import ConfigManager

from pdfmergetk.installer import InstallerPDFMergeTK
