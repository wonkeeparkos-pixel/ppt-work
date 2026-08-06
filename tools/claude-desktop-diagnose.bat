@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion
title Claude Desktop 진단

set "REPORT=%USERPROFILE%\Desktop\claude-진단결과.txt"
if not exist "%USERPROFILE%\Desktop" set "REPORT=%USERPROFILE%\claude-진단결과.txt"
break>"%REPORT%"

call :both ""
call :both "==================================================="
call :both "  Claude Desktop 진단 결과"
call :both "==================================================="
call :both ""

call :both "[계정/경로]"
call :both "  USERPROFILE = %USERPROFILE%"
call :both "  APPDATA     = %APPDATA%"
call :both "  LOCALAPPDATA= %LOCALAPPDATA%"
call :both ""

call :both "[1] 프로그램 설치 폴더 (%%LOCALAPPDATA%%\AnthropicClaude)"
if exist "%LOCALAPPDATA%\AnthropicClaude" (
    call :both "  -> 있음. 내용:"
    for /f "delims=" %%F in ('dir /b "%LOCALAPPDATA%\AnthropicClaude" 2^>nul') do call :both "     %%F"
    if exist "%LOCALAPPDATA%\AnthropicClaude\claude.exe" (
        call :both "  -> claude.exe 실행파일 확인됨"
    ) else (
        call :both "  -> [문제] 루트에 claude.exe 없음"
    )
) else (
    call :both "  -> [없음] 프로그램이 설치되어 있지 않거나 삭제되었습니다."
)
call :both ""

call :both "[2] 사용자 데이터 폴더 (%%APPDATA%%\Claude)"
if exist "%APPDATA%\Claude" (
    call :both "  -> 있음. 내용:"
    for /f "delims=" %%F in ('dir /b "%APPDATA%\Claude" 2^>nul') do call :both "     %%F"
) else (
    call :both "  -> [없음] 데이터 폴더가 통째로 사라졌습니다."
)
call :both ""

call :both "[3] 커넥터 설정 파일 흔적"
set "FOUND=0"
for %%P in (
    "%APPDATA%\Claude\claude_desktop_config.json"
    "%APPDATA%\Claude\claude_desktop_config.json.bak"
    "%USERPROFILE%\claude_desktop_config.json"
) do (
    if exist %%P ( call :both "  -> 발견: %%~P" & set "FOUND=1" )
)
if "!FOUND!"=="0" call :both "  -> 설정 파일을 찾지 못했습니다. (커넥터 재설정 필요)"
call :both ""

call :both "[4] 실행 중인 프로세스"
tasklist /FI "IMAGENAME eq claude.exe" 2>nul | find /I "claude.exe" >nul
if errorlevel 1 ( call :both "  -> 실행 중 아님" ) else ( call :both "  -> claude.exe 가 살아있습니다 (좀비 프로세스 가능성)" )
call :both ""

call :both "[5] 시작 메뉴 바로가기"
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Claude.lnk" (
    call :both "  -> 있음"
) else (
    call :both "  -> 없음"
)
call :both ""

call :both "[6] 제어판 등록 정보"
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall" /s /f "Claude" 2>nul | find /I "DisplayName" >nul
if errorlevel 1 ( call :both "  -> 설치 목록에 없음" ) else ( call :both "  -> 설치 목록에 등록되어 있음" )
call :both ""

call :both "[7] C: 드라이브 여유 공간"
set "FREE="
for /f "delims=" %%S in ('powershell -NoProfile -Command "[math]::Round((Get-PSDrive C).Free/1GB,1)" 2^>nul') do set "FREE=%%S"
if defined FREE ( call :both "  -> !FREE! GB 남음" ) else ( call :both "  -> 확인 실패" )
call :both ""

call :both "==================================================="
call :both " 이 결과를 그대로 복사해서 알려주세요."
call :both " 파일로도 저장했습니다: %REPORT%"
call :both "==================================================="

echo.
start "" notepad "%REPORT%"
pause
endlocal
exit /b

:both
rem  !LINE! 은 파싱이 끝난 뒤 치환되므로 값 안의 > < & | 가 연산자로 오인되지 않는다.
rem  %~1 을 그대로 echo 하면 "-> 있음" 의 > 가 리다이렉트로 해석되어 줄이 통째로 사라진다.
set "LINE=%~1"
if not defined LINE (
    echo.
    >>"%REPORT%" echo.
) else (
    echo(!LINE!
    >>"%REPORT%" echo(!LINE!
)
set "LINE="
exit /b
