@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion
title Claude Desktop 복구 도구

echo.
echo ============================================
echo   Claude Desktop 복구 도구 (Windows)
echo ============================================
echo.
echo  설정 파일(claude_desktop_config.json)은 백업 후 그대로 둡니다.
echo  캐시만 지우므로 커넥터 설정은 사라지지 않습니다.
echo.
pause

set "CLAUDE_DATA=%APPDATA%\Claude"
set "CLAUDE_APP=%LOCALAPPDATA%\AnthropicClaude"

echo.
echo [1/4] 살아있는 Claude 프로세스를 모두 종료합니다...
taskkill /F /IM claude.exe /T >nul 2>&1
taskkill /F /IM Claude.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo       완료.

echo.
echo [2/4] 설정 파일을 백업합니다...
if exist "%CLAUDE_DATA%\claude_desktop_config.json" (
    copy /Y "%CLAUDE_DATA%\claude_desktop_config.json" "%CLAUDE_DATA%\claude_desktop_config.json.bak" >nul
    echo       백업: %CLAUDE_DATA%\claude_desktop_config.json.bak
) else (
    echo       설정 파일이 없습니다. 건너뜁니다.
)

echo.
echo [3/4] 캐시를 삭제합니다...
if not exist "%CLAUDE_DATA%" (
    echo       [경고] %CLAUDE_DATA% 폴더가 없습니다.
    echo       Claude Desktop이 설치되지 않았거나 경로가 다릅니다.
    goto :launch
)
for %%D in ("Cache" "Code Cache" "GPUCache" "DawnCache" "DawnGraphiteCache" "DawnWebGPUCache" "Service Worker" "blob_storage") do (
    if exist "%CLAUDE_DATA%\%%~D" (
        rmdir /S /Q "%CLAUDE_DATA%\%%~D" >nul 2>&1
        echo       삭제: %%~D
    )
)
if exist "%CLAUDE_DATA%\Local Storage\leveldb\LOCK" del /F /Q "%CLAUDE_DATA%\Local Storage\leveldb\LOCK" >nul 2>&1
echo       완료.

:launch
echo.
echo [4/4] Claude Desktop을 다시 실행합니다...
set "EXE="
if exist "%CLAUDE_APP%\claude.exe" set "EXE=%CLAUDE_APP%\claude.exe"
if not defined EXE (
    for /f "delims=" %%F in ('dir /b /o-n "%CLAUDE_APP%\app-*" 2^>nul') do (
        if not defined EXE if exist "%CLAUDE_APP%\%%F\claude.exe" set "EXE=%CLAUDE_APP%\%%F\claude.exe"
    )
)

set "LNK=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Claude.lnk"

if defined EXE (
    start "" "!EXE!"
    echo       실행: !EXE!
) else if exist "%LNK%" (
    start "" "%LNK%"
    echo       시작 메뉴 바로가기로 실행했습니다.
) else (
    echo       [주의] claude.exe를 찾지 못했습니다. 직접 실행해 주세요.
)

echo.
echo ============================================
echo  창이 정상적으로 떴으면 여기서 끝입니다.
echo.
echo  아직도 안 열리거나 흰 화면이면 [1] 을 누르세요.
echo  (그래픽 가속을 끄고 실행 - 흰 화면의 가장 흔한 원인)
echo  그냥 종료하려면 [Enter].
echo ============================================
set "CHOICE="
set /p CHOICE=선택:

if "%CHOICE%"=="1" (
    echo.
    echo 그래픽 가속을 끄고 다시 실행합니다...
    taskkill /F /IM claude.exe /T >nul 2>&1
    timeout /t 2 /nobreak >nul
    if defined EXE (
        start "" "!EXE!" --disable-gpu --disable-software-rasterizer
        echo 실행했습니다. 이걸로 열리면 그래픽 드라이버 문제입니다.
        echo 그래픽 드라이버를 최신으로 업데이트하세요.
    ) else (
        echo claude.exe 경로를 찾지 못해 실행할 수 없습니다.
    )
    echo.
    pause
)

endlocal
