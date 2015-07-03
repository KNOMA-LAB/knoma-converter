from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=[], excludes=[])

import sys

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('papaya-converter.py', base=base)
]

setup(name='knoma-converter',
      version='1.0',
      description='knoma imagemagick frontend',
      options=dict(build_exe=buildOptions),
      executables=executables)
