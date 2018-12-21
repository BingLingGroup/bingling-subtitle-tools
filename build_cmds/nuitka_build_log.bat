@ECHO OFF
set nuitka_build_name="nuitka_build.bat"
set log_name="%date:~0,4%_%date:~5,2%_%date:~8,2%_%time:~0,2%_%time:~3,2%_%time:~6,2%_build.log"

@ECHO ON
call %nuitka_build_name% 1>%log_name% 2>&1 3>&1
pause>con
