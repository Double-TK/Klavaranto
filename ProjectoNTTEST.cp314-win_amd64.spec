# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ProjectoNTTEST.cp314-win_amd64.pyd'],
    pathex=[],
    binaries=[],
    datas=[('idiomas.json', '.'), ('ProtestRiot-Regular.ttf', '.'), ('app_idioma_es.png', '.'), ('app_idioma_en.png', '.'), ('app_idioma_eo.png', '.'), ('ProjectoNTTEST.cp314-win_amd64.pyd', '.')],
    hiddenimports=[],
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
    name='ProjectoNTTEST.cp314-win_amd64',
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
