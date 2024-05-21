#include <include/inner_dir/log1.hpp> // specific comment 1
// Some comment
//#include <include/inner_dir/log1.hpp> // specific comment 1
// Other comment
  #include <include/include.hpp> // space before include
        #include <iostream>     // spaces and tabs before include

#include <include/inner_dir/include.hpp>    // one more comment

int func() {
    int a = 42;
    log1();
    return a;
}

#include <include/other_dir_include.hpp> // other_dir
// #include<include/does/not/exist.hpp>

int main() {
    int cur = other_dir_include();
    cur += outer_include_2();
    cur += outer_include_1();
    cur += inner_include();
    std::cout << func() << '\n';
    std::cout << "cur = " << cur << '\n';
}
