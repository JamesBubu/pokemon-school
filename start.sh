#!/bin/bash
# 啟動寶可夢學習大冒險
cd "$(dirname "$0")"

# 若 8080 已被佔用則先關掉
lsof -ti tcp:8080 | xargs kill -9 2>/dev/null

echo "啟動伺服器中... http://localhost:8080"
python3 -m http.server 8080 &
SERVER_PID=$!
sleep 0.5
open http://localhost:8080
echo "按 Ctrl+C 關閉伺服器"
wait $SERVER_PID
