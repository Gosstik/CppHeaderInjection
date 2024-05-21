#include <iostream>
#include <include/inner_dir/log2.hpp>

int inner_include() {
    std::cout << "start inner_include\n";
    log2();
    std::cout << "end inner_include\n";
    return 1;
}
