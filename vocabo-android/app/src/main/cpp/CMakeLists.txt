cmake_minimum_required(VERSION 3.22.1)

project("vocabo")

add_library(
        llama-lib
        SHARED
        llama_interface.cpp)

target_link_libraries(
        llama-lib
        android
        log)
