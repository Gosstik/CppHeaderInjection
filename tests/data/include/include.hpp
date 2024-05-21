#include <include/inner_dir/log1.hpp> // specific comment 2
// #include<include/does/not/exist.hpp>


int outer_include_1() {
    std::cout << "begin outer_include_1\n";
    log1();
    std::cout << "end outer_include_1\n";
    return 10;
}

#include <include/inner_dir/log2.hpp>

int outer_include_2() {
    std::cout << "begin outer_include_1\n";
    log2();
    std::cout << "end outer_include_1\n";
    return 100;
}
