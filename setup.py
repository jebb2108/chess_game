from setuptools import setup

APP_NAME = 'Chess Game'
APP = ['main.py']
DATA_FILES = [
    ('db', ['db/users.db']),
    ('images', ['images/*.png']),
    ('sounds', ['sounds/*.mp3']),
]
OPTIONS = {
    'packages': ['pygame', 'pygwidgets', 'pyghelpers', 'pillow',],
    'iconfile': 'icon.icns',
    'argv_emulation': True,
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': 'Chess Game by Gabriel Bouchard',
        'CFBundleVersion': '1.5 stable',
        'CFBundleShortVersionString': '1.5',
        'NSHumanReadableCopyright': 'Copyright (c) 2023, Gabriel Bouchard, All rights reserved.',
    },
}

setup(
    app=APP,
    name=APP_NAME,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
