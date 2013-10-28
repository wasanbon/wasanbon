@if "%1" == "" goto list
@FOR /f "DELIMS=" %%A IN ('wasanbon-admin.py package directory %1') DO @SET TARGET_DIR=%%A
@cd %TARGET_DIR%
@goto end
:list
@wasanbon-admin.py package list
:end