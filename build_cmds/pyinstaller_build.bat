@echo off
set dist_dir="..\.build_and_dist\pyinstaller.build"

@echo on
pyinstaller pyinstaller_build.spec --clean --distpath %dist_dir% --workpath %dist_dir%
call cmd