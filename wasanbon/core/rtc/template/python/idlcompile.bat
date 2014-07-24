@echo off
setlocal
for %%I in (python.exe) do if exist %%~$path:I set f=%%~$path:I
if exist %f% goto IDLCOMPILE
if not exist %f% goto ECHOERROR
endlocal


:IDLCOMPILE
  for %%A in (idl\*.idl) do %f:python.exe=%omniidl.exe -bpython -I"%RTM_ROOT%rtm/idl" -I"$HOMEPATH/rtm/idl" %%~fA 
  exit /b

:ECHOERROR
  echo "python.exe" can not be found.
  echo Please modify PATH environmental variable for python command.
  exit /b
