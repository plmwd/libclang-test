cmake_minimum_required(VERSION 3.20)

project(libclang-test)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include_directories(include)
add_executable(test src/test.cpp)
