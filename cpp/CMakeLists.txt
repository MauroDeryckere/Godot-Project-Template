file(GLOB_RECURSE SRC CONFIGURE_DEPENDS src/*.cpp)

add_library(myextension SHARED ${SRC})

target_include_directories(myextension PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)


target_link_libraries(myextension
    godot-cpp
)

# Output directly to Godot project
add_custom_command(TARGET myextension POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
    $<TARGET_FILE:myextension>
    ${CMAKE_SOURCE_DIR}/godot/bin/
)

    