cmake_minimum_required(VERSION 3.10)
project(test_package CXX)

find_package(libframeutil REQUIRED)

add_executable(test_package test_package.cpp)
target_include_directories(test_package PRIVATE ${libframeutil_INCLUDE_DIRS})