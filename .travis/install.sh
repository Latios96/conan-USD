#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then

fi

pip install conan --upgrade
pip install conan_package_tools

conan user
conan profile new default --detect
conan profile update settings.compiler.libcxx=libstdc++11 default
