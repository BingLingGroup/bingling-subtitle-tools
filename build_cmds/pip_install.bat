@echo off
set setup_dir="..\"
@echo on
cd %~dp0
cd %setup_dir%
pip install .
call cmd