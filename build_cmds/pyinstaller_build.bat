@ECHO OFF
set dist_dir="..\.build_and_dist\pyinstaller.build"

@ECHO ON
pyinstaller pyinstaller_build.spec --clean --distpath %dist_dir% --workpath %dist_dir%
pause