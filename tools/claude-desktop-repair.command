#!/bin/bash
# Claude Desktop 복구 도구 (macOS)
# Finder에서 더블클릭하면 실행됩니다.

set -u

DATA_DIR="$HOME/Library/Application Support/Claude"
LOG_DIR="$HOME/Library/Logs/Claude"
CONFIG="$DATA_DIR/claude_desktop_config.json"

echo
echo "============================================"
echo "  Claude Desktop 복구 도구 (macOS)"
echo "============================================"
echo
echo " 설정 파일(claude_desktop_config.json)은 백업 후 그대로 둡니다."
echo " 캐시만 지우므로 커넥터 설정은 사라지지 않습니다."
echo
read -r -p "계속하려면 Enter를 누르세요..."

echo
echo "[1/4] 살아있는 Claude 프로세스를 모두 종료합니다..."
osascript -e 'quit app "Claude"' >/dev/null 2>&1
sleep 2
pkill -f "Claude.app/Contents/MacOS/Claude" >/dev/null 2>&1
sleep 1
echo "      완료."

echo
echo "[2/4] 설정 파일을 백업합니다..."
if [ -f "$CONFIG" ]; then
    cp -f "$CONFIG" "$CONFIG.bak"
    echo "      백업: $CONFIG.bak"
else
    echo "      설정 파일이 없습니다. 건너뜁니다."
fi

echo
echo "[3/4] 캐시를 삭제합니다..."
if [ ! -d "$DATA_DIR" ]; then
    echo "      [경고] $DATA_DIR 폴더가 없습니다."
    echo "      Claude Desktop이 설치되지 않았을 수 있습니다."
else
    for d in "Cache" "Code Cache" "GPUCache" "DawnCache" "DawnGraphiteCache" \
             "DawnWebGPUCache" "Service Worker" "blob_storage"; do
        if [ -d "$DATA_DIR/$d" ]; then
            rm -rf "$DATA_DIR/$d"
            echo "      삭제: $d"
        fi
    done
    rm -f "$DATA_DIR/Local Storage/leveldb/LOCK" 2>/dev/null
    echo "      완료."
fi

echo
echo "[4/4] Claude Desktop을 다시 실행합니다..."
if [ -d "/Applications/Claude.app" ]; then
    open -a "Claude"
    echo "      실행했습니다."
else
    echo "      [주의] /Applications/Claude.app 을 찾지 못했습니다."
    echo "      https://claude.ai/download 에서 재설치하세요."
fi

echo
echo "============================================"
echo " 창이 정상적으로 떴으면 여기서 끝입니다."
echo
echo " 아직도 안 열리거나 흰 화면이면 [1] 을 누르세요."
echo " (그래픽 가속을 끄고 실행 - 흰 화면의 가장 흔한 원인)"
echo " 그냥 종료하려면 Enter."
echo "============================================"
read -r -p "선택: " CHOICE

if [ "${CHOICE:-}" = "1" ]; then
    echo
    echo "그래픽 가속을 끄고 다시 실행합니다..."
    osascript -e 'quit app "Claude"' >/dev/null 2>&1
    sleep 2
    pkill -f "Claude.app/Contents/MacOS/Claude" >/dev/null 2>&1
    sleep 1
    if [ -x "/Applications/Claude.app/Contents/MacOS/Claude" ]; then
        "/Applications/Claude.app/Contents/MacOS/Claude" --disable-gpu \
            --disable-software-rasterizer >/dev/null 2>&1 &
        echo "실행했습니다. 이걸로 열리면 그래픽 관련 문제입니다."
    else
        echo "Claude 실행 파일을 찾지 못했습니다."
    fi
    echo
    read -r -p "Enter를 누르면 종료합니다..."
fi

echo
echo "로그가 필요하면 아래 폴더를 열어 최근 파일을 확인하세요:"
echo "  $LOG_DIR"
