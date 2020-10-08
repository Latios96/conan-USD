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

conan remote add my_bintray https://api.bintray.com/conan/latios96/my_conan
conan remote list

if [[ "$(uname -s)" != 'Darwin' ]]; then
  sudo apt-get update -qq

  # Install X11 dev libraries
  sudo apt-get install libxrandr-dev
  sudo apt-get install libxcursor-dev
  sudo apt-get install libxinerama-dev
  sudo apt-get install libxi-dev

  # install glut and xxf86vm (for GL libs)
  sudo apt-get install freeglut3
  sudo apt-get install freeglut3-dev
  sudo apt-get install libxxf86vm1
  sudo apt-get install libxxf86vm-dev


  ###############################################################################
  # Upgrade to get a version of Mesa that supports OGL 4
  sudo add-apt-repository ppa:ubuntu-x-swat/updates -y
  sudo apt-get update -qq
  sudo apt-get dist-upgrade
fi

