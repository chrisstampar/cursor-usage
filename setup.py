from setuptools import setup

APP = ['src/app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'assets/icon.icns',
    'plist': {
        'LSUIElement': True,
        'CFBundleName': 'CursorUsage',
        'CFBundleDisplayName': 'CursorUsage',
        'CFBundleGetInfoString': 'Cursor Usage Menu Bar App',
        'CFBundleIdentifier': 'com.cursorusage.menubar',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
    },
    'packages': ['rumps']
}

setup(
    app=APP,
    name='CursorUsage',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)