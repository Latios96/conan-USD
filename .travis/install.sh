#!/bin/bash

set -e
set -x


pip3 install conan --upgrade
pip3 install conan_package_tools

conan user
conanDefaultProfile=~/.conan/profiles/default
if [ -f "$conanDefaultProfile" ]; then
  echo "Conan default profile already exists!"
else
  echo "Conan default profile not exists, creating.."
  conan profile new default --detect
fi

if [[ "$(uname -s)" != 'Darwin' ]]; then
  conan profile update settings.compiler.libcxx=libstdc++11 default
fi

