@echo off
set nuitka_build_bat_name="nuitka_build.bat"
set log_name="%date:~0,4%_%date:~5,2%_%date:~8,2%_%time:~0,2%_%time:~3,2%_%time:~6,2%_build.log"

@echo on
cd %~dp0
call %nuitka_build_name% 1>%log_name% 2>&1 3>&1
pause>nul