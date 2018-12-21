@ECHO OFF
set source_dir="../bingling_subtitle_tools"
set output_dir="../.build_and_dist/"
set icon_dir="../icon/bingling.ico"

@ECHO ON
nuitka %source_dir% --standalone --output-dir %output_dir% --show-progress --show-scons  --windows-icon=%icon_dir%
pause