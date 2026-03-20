file(GLOB_RECURSE SRC CONFIGURE_DEPENDS src/*.cpp)

add_library(myextension SHARED ${SRC})

target_compile_features(myextension PRIVATE cxx_std_20)
set_target_properties(myextension PROPERTIES CXX_EXTENSIONS OFF)

target_include_directories(myextension PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)


target_link_libraries(myextension PRIVATE
    godot-cpp
)

# Output directly to Godot project
add_custom_command(TARGET myextension POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    $<TARGET_FILE:myextension>
    ${PROJECT_SOURCE_DIR}/godot/bin/
)

if(WIN32)
    add_custom_command(TARGET myextension POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        $<TARGET_PDB_FILE:myextension>
        ${PROJECT_SOURCE_DIR}/godot/bin/
    )
endif()
