# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('ProjectoNTTEST.cp314-win_amd64.pyd', '.')],
    datas=[('idiomas.json', '.'), ('ProtestRiot-Regular.ttf', '.'), ('app_idioma_es.png', '.'), ('app_idioma_en.png', '.'), ('app_idioma_eo.png', '.')],
    hiddenimports=['pynput', 'pynput.keyboard', 'pynput.keyboard._win32', 'pystray', 'pystray._win32', 'PIL', 'PIL.Image', 'PIL.ImageDraw', 'PIL.ImageTk', 'psutil', 'tkinter', 'tkinter.ttk', 'tkinter.font', 'configparser', 'json', 'threading', 'ctypes'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icono.ico'],
)
