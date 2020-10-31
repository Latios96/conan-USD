#define NOMINMAX
#include <pxr/usd/usd/stage.h>
#include <iostream>
int main() {
    pxr::UsdStage::CreateInMemory();
    std::cout << "works" << std::endl;
}
