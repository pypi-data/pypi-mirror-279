# PDFMergeTK

GUI application that allows you to merge PDF files quickly, easily, intuitively and with respect for privacy.

---

[![Build Executables](https://github.com/kurotom/PDFMergeTK/actions/workflows/build.yml/badge.svg)](https://github.com/kurotom/PDFMergeTK/actions/workflows/build.yml)

---

> [!IMPORTANT]
> * **Windows** : The executable EXE is generated using [`pyinstaller`](https://pyinstaller.org/en/stable/), it is possible that when downloading and/or running this executable, the antivirus you are using detects it as a virus, but it is because it is a **false positive**, [review `pyinstaller` developer notes](https://github.com/pyinstaller/pyinstaller/blob/develop/.github/ISSUE_TEMPLATE/antivirus.md). If you have any problems running this program, it should be added to the <u>*antivirus exception list*</u> and it would be helpful to this project if you **report it as false positive** to the antivirus company you use.
> * **Linux** : did not file any reports on virustotal.com.
> * If you have any problems create an issue in the [`Github Issue` section of the project](https://github.com/kurotom/PDFMergeTK/issues)
>

> [!NOTE]
> As a *sign of transparency*, you can review the code, view the analysis results at *virustotal.com* and compare the SHA256 hash of the generated executable, available in the download section.
>


# Install

You can install this project in several ways.


## From Pypi, install package

```bash
$ pip install pdfmergetk
```

Upon completion of the installation, the following commands will be available:

| Command | Description |
|-|-|
| `mergepdf` | start the program. |
| `mergepdfreset` | in case of an error when trying to open the program, restarts the program's multiple run mechanism (opening the program more than once). |
| `pdfmergetklinks` | creates shortcuts for the program, on desktop on Windows and in `~/.local/share/applications/` on Linux. With the name `PDFMergeTK`.|


## From Github, clone project

```bash
$ git clone https://github.com/kurotom/PDFMergeTK.git

$ cd PDFMergeTK

$ poetry shell

$ poetry install

$ python src
```

# Download executable for Linux or Windows

* [Download latest PDFMergeTK - Linux](https://github.com/kurotom/PDFMergeTK/releases/download/v0.1.0-linux/PDFMergeTK)

  SHA256: 5316655626c9c9c3ce873e0b63fe2729d456881d948955f635f54209f8ed1eef

  [Virustotal.com scan latest version](https://www.virustotal.com/gui/file/5316655626c9c9c3ce873e0b63fe2729d456881d948955f635f54209f8ed1eef/detection)


* [Download latest PDFMergeTK - Windows](https://github.com/kurotom/PDFMergeTK/releases/download/v0.1.0-windows/PDFMergeTK.exe)

  SHA256: fdcf5504057b8f6b79b13dbdd705d6285b8b89e72bfdef6d71bbf97746fdf9b4

  [Virustotal.com scan latest version](https://www.virustotal.com/gui/file/fdcf5504057b8f6b79b13dbdd705d6285b8b89e72bfdef6d71bbf97746fdf9b4/detection)


