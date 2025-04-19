cmake_minimum_required(VERSION 3.10)
project(test_package)

find_package(libzedmd REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE libzedmd::libzedmd)