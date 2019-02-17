set "release_name=bingling-subtitle-tools"
set "package_name=bingling_subtitle_tools"

cd %~dp0
mkdir "..\.release\%release_name%-port"
cp "release_files\run.bat" "..\.release\%release_name%-port"
cp "release_files\help.bat" "..\.release\%release_name%-port"
cp "release_files\config.py" "..\.release\%release_name%-port"
cp "..\LICENSE" "..\.release\%release_name%-port"
cp "..\README.md" "..\.release\%release_name%-port"
cp "..\docs\README_ZH.md" "..\.release\%release_name%-port"
cp -r "..\docs\notice" "..\.release\%release_name%-port"
call update_requirements.bat
cp "..\requirements.txt" "..\.release\%release_name%-port"
cp -r "..\.release\%release_name%-port" "..\.release\%release_name%-port-pyinstaller"
cp -r "..\.build_and_dist\%package_name%.dist" "..\.release\%release_name%-port\%release_name%"
mkdir "..\.release\%release_name%-port-pyinstaller\%release_name%"
cp "..\.build_and_dist\pyinstaller.build\%release_name%.exe" "..\.release\%release_name%-port-pyinstaller\%release_name%"
7z a "..\.release\%release_name%-win.7z" "..\.release\%release_name%-port"
7z a "..\.release\%release_name%-win-pyinstaller.7z" "..\.release\%release_name%-port-pyinstaller"
call cmd