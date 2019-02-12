@echo off
set output_dir="../.build_and_dist/"
set icon_dir="../docs/icon/bingling.ico"
set output_name="bingling-subtitle-tools"
set package_name="bingling_subtitle_tools"

@echo on
call nuitka "../%package_name:~1,-1%" --standalone --output-dir %output_dir% --show-progress --show-scons  --windows-icon=%icon_dir%
cd "%output_dir:~1,-1%%package_name:~1,-1%.dist/"
ren "%package_name:~1,-1%.exe" "%output_name:~1,-1%.exe"