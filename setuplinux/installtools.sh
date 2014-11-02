#!/bin/bash
#install Linux basic tools
apt-get install konsole
apt-get install g++
apt-get install dos2unix

#install input method
apt-get install ibus ibus-clutter ibus-gtk ibus-gtk3 ibus-qt4

#install scrapy
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 627220E7
echo 'deb http://archive.scrapy.org/ubuntu scrapy main' | tee /etc/apt/sources.list.d/scrapy.list
apt-get update && apt-get install scrapy-0.24

#set up git
apt-get install git
git config --global core.editor vi

#install python library
apt-get install python-pyodbc
