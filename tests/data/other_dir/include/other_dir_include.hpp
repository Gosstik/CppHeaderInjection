#include <include/inner_dir/include.hpp>
#include <iostream>

int other_dir_include() {
    std::cout << "begin other_dir_include\n";
    inner_include();
    std::cout << "end other_dir_include\n";
    return 1000;
}
