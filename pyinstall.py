import PyInstaller.__main__

PyInstaller.__main__.run([
    'gui.py',
    '--onefile',
    '--noconsole',
    '--icon=YoutubeDownloader.icns',  # Utilise ton icône PNG
    '--add-data', 'download.py:.',    # Inclut download.py dans le même répertoire
])
