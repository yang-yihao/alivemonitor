#!/bin/sh

if [ -d "build" ]; then
    rm -rf build/*
fi

mkdir -p build/alivemonitor/logs

cp -R app build/alivemonitor
cp __init__.py build/alivemonitor
cp main.py build/alivemonitor
cp -R bin build/alivemonitor

cd build
zip -r alivemonitor alivemonitor

rm -rf alivemonitor

if [ "$1" == "upload" -a "$2" == "vastcm.com" ]; then
    echo uploading to vastcm.com
    scp alivemonitor.zip root@vastcm.com:/usr/local
fi
