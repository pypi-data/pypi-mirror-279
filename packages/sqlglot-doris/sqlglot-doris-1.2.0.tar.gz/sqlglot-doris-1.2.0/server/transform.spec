#transfrom.spec

block_cipher = None

a = Analysis(['manage.py'],
             pathex=['/root/doris-sql-convertor/server'],
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
          name='doris-sql-convertor-1.0.2-bin-x86',
          debug=False,
          strip=False,
          upx=True,
          console=True)
