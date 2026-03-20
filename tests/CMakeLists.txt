include(FetchContent)

FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG v3.8.0
    GIT_SHALLOW TRUE
)
FetchContent_MakeAvailable(Catch2)

file(GLOB_RECURSE TEST_SRC CONFIGURE_DEPENDS src/*.cpp)

# Pure C++ sources that can be tested without Godot
set(ENGINE_SRC
    ${CMAKE_SOURCE_DIR}/cpp/src/engine/Time.cpp
)

add_executable(tests ${TEST_SRC} ${ENGINE_SRC})

target_compile_features(tests PRIVATE cxx_std_20)
set_target_properties(tests PROPERTIES CXX_EXTENSIONS OFF)

target_include_directories(tests PRIVATE
    ${CMAKE_SOURCE_DIR}/cpp/include
)

target_link_libraries(tests PRIVATE
    Catch2::Catch2WithMain
)

include(Catch)
catch_discover_tests(tests)
