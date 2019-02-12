# -*- mode: python -*-

block_cipher = None


a = Analysis([r"..\bingling_subtitle_tools\__main__.py",
             r"..\bingling_subtitle_tools\ass_v4p_prcs.py",
             r"..\bingling_subtitle_tools\__init__.py",
             r"..\bingling_subtitle_tools\file_io.py",
             r"..\bingling_subtitle_tools\version.py"],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          icon=r"..\docs\icon\bingling.ico",
          name="bingling-subtitle-tools-pyinstaller",
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
