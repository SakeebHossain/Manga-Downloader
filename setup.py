from cx_Freeze import setup, Executable

options = {
    'build_exe': {
        'includes': ['MangaDownloaderClient', 'requests'],
    }
}

setup(name = "MangaDownloader" ,
      version = "0.1" ,
      description = "" ,
      executables = [Executable("MangaDownloader.py")])