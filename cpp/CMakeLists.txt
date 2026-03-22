file(GLOB_RECURSE SRC CONFIGURE_DEPENDS src/*.cpp)

add_library(myextension SHARED ${SRC})

target_compile_features(myextension PRIVATE cxx_std_20)

target_compile_options(myextension PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -Wpedantic>
)

target_include_directories(myextension PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(myextension PRIVATE
    godot-cpp
)

# Suppress warnings from godot-cpp headers
get_target_property(GODOT_CPP_INCLUDE_DIRS godot-cpp INTERFACE_INCLUDE_DIRECTORIES)
target_include_directories(myextension SYSTEM PRIVATE ${GODOT_CPP_INCLUDE_DIRS})

# Compile class documentation into the extension (shows in Godot's built-in help)
file(GLOB_RECURSE DOC_XML CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/doc_classes/*.xml)
if(DOC_XML)
    target_doc_sources(myextension "${DOC_XML}")
endif()

# Use godot-cpp suffix for output naming (e.g. myextension.linux.template_debug.x86_64.so)
get_target_property(GODOTCPP_SUFFIX godot-cpp GODOTCPP_SUFFIX)

# Determine output directory based on platform
if(ANDROID)
    set(BIN_OUTPUT_DIR ${PROJECT_SOURCE_DIR}/godot/bin/android/${ANDROID_ABI})
elseif(CMAKE_SYSTEM_NAME STREQUAL "iOS")
    set(BIN_OUTPUT_DIR ${PROJECT_SOURCE_DIR}/godot/bin/ios)
else()
    set(BIN_OUTPUT_DIR ${PROJECT_SOURCE_DIR}/godot/bin)
endif()

set_target_properties(myextension PROPERTIES
    CXX_EXTENSIONS OFF
    POSITION_INDEPENDENT_CODE ON
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN ON

    PREFIX "lib"
    OUTPUT_NAME "myextension${GODOTCPP_SUFFIX}"

    LIBRARY_OUTPUT_DIRECTORY "$<1:${BIN_OUTPUT_DIR}>"
    RUNTIME_OUTPUT_DIRECTORY "$<1:${BIN_OUTPUT_DIR}>"
    PDB_OUTPUT_DIRECTORY "$<1:${BIN_OUTPUT_DIR}>"
)

if(CMAKE_SYSTEM_NAME STREQUAL "iOS")
    set_target_properties(myextension PROPERTIES
        XCODE_ATTRIBUTE_CODE_SIGNING_ALLOWED "NO"
    )
endif()
