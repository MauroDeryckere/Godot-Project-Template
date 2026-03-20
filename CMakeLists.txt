cmake_minimum_required(VERSION 3.20)
project(GodotCppTemplate)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(BUILD_TESTS OFF CACHE BOOL "Build unit tests")

add_subdirectory(third_party/godot-cpp)
add_subdirectory(cpp)

if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()