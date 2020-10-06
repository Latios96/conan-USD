#!/bin/bash

set -e
set -x


pip install conan --upgrade
pip install conan_package_tools

conan user
conan profile new default --detect
conan profile update settings.compiler.libcxx=libstdc++11 default
