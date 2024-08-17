#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <BOT_TOKEN>"
    exit 1
fi

echo "Running CalculationServer..."

cd ./Telegram/Calculation_Server/ || exit 1
rm -rf build # Remove the existing build directory
mkdir -p build
cd build || exit 1

if ! cmake .. || ! make -j$(nproc); then
    echo "Build failed. Exiting..."
    exit 1
fi

if [ ! -f "./CalculationServer" ]; then
    echo "CalculationServer executable not found! Exiting..."
    exit 1
fi

./CalculationServer &
server_pid=$!

echo "Running Telegram bot"
export BOT_TOKEN=$1

cd ../../ || exit 1
python3 bot.py

trap ctrl_c INT
function ctrl_c() {
    echo "Killing server work..."
    kill $server_pid
    rm -rf list_names.xlsx
}

wait $server_pid
