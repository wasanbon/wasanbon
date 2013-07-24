FOR /f "DELIMS=" %%A IN ('wasanbon-admin.py project directory %%1') DO SET TARGET_DIR=%%A
cd %%TARGET_DIR