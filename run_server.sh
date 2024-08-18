#!/bin/bash

echo "Running CalculationServer..."

cd ./Telegram/Calculation_Server/ || exit 1
rm -rf build
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