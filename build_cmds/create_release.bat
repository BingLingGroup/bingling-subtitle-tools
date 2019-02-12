set "release_name=bingling-subtitle-tools"
set "package_name=bingling_subtitle_tools"

mkdir "..\.release\%package_name%"
cp "release_files\run.bat" "..\.release\%package_name%"
cp "release_files\help.bat" "..\.release\%package_name%"
cp "release_files\config.py" "..\.release\%package_name%"
cp "..\.build_and_dist\%package_name%.dist\%release_name%.exe" "..\.release\%package_name%"
cp -r "..\docs\notice" "..\.release\%package_name%"
7z a "..\.release\%release_name%-win.7z" "..\.release\%package_name%"
call cmd