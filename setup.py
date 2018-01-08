from cx_Freeze import setup, Executable

build_exe_options = {
        'packages': ['MangaDownloaderClient', 'requests', 'os','bs4', "idna.idnadata", "multiprocessing"]
    }

setup(name = "MangaDownloader" ,
      version = "0.1" ,
      description = "" ,
      options = {"build_exe": build_exe_options},
      executables = [Executable("MangaDownloader.py")])