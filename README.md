[ ![Download](https://api.bintray.com/packages/latios96/my_conan/USD:latios96/images/download.svg?version=20.08:channel) ](https://bintray.com/latios96/my_conan/USD:latios96/20.08:channel/link)

[![Build status](https://ci.appveyor.com/api/projects/status/7412cbxwjx8nnlid?svg=true)](https://ci.appveyor.com/project/Latios96/conan-usd)
[![Build Status](https://travis-ci.com/Latios96/conan-USD.svg?branch=main)](https://travis-ci.com/Latios96/conan-USD)


# Conan recipe for USD

[USD](https://github.com/PixarAnimationStudios/USD) is a scene description for interchange between graphics applications.. 

The and prebuild binaries can be found on [Bintray](https://bintray.com/beta/#/latios96/my_conan/USD:latios96?tab=overview).

## How to use
You need to add my Bintray repo to conan:
```shell
conan remote add my_bintray https://api.bintray.com/conan/latios96/my_conan
```
Now you can install the package:
```shell
conan install USD/20.08@latios96/stable