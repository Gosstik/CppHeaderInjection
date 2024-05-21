  #include <iostream>
#include <include/inner_dir/log1.hpp>// don't forget about comments

void log2() {
    std::cout << "begin log2\n";
    log1();
    std::cout << "end log2\n";
}
