mkdir ..\.release\bingling_subtitle_tools
cp release_files\run.bat ..\.release\bingling_subtitle_tools
cp release_files\config.py ..\.release\bingling_subtitle_tools
cp ..\.build_and_dist\bingling_subtitle_tools.dist\bingling_subtitle_tools.exe ..\.release\bingling_subtitle_tools
cp -r ..\docs\notice ..\.release\bingling_subtitle_tools
7z a ..\.release\bingling_subtitle_tools_win.7z ..\.release\bingling_subtitle_tools
pause