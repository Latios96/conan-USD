#!/bin/bash

set -e
set -x


pip3 install conan --upgrade
pip3 install conan_package_tools

conan user
conan profile new default --detect

if [[ "$(uname -s)" != 'Darwin' ]]; then
  conan profile update settings.compiler.libcxx=libstdc++11 default
fi

