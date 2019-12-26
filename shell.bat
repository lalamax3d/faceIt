@Echo off
echo Enabling Computer Vision Environment for FACE_IT
SET FILEPATH=%~dp0
cmd /k "%userprofile%\.venv\cv\Scripts\activate & cd /d %FILEPATH%"