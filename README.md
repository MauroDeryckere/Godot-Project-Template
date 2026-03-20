# Godot C++ Project Template

A ready-to-use template for Godot 4.6 projects with C++ GDExtension support. Includes CMake build system, cross-platform presets, unit testing, and CI workflows.

## Prerequisites

- [Godot 4.6+](https://godotengine.org/download)
- [CMake 3.20+](https://cmake.org/download/)
- [Ninja](https://ninja-build.org/) (or another CMake-supported generator)
- A C++20 compiler (MSVC, GCC, Clang)

For mobile builds:
- **Android**: [Android NDK](https://developer.android.com/ndk) with `ANDROID_NDK_ROOT` environment variable set
- **iOS**: Xcode with iOS SDK

## Getting Started

```bash
git clone --recursive https://github.com/MauroDeryckere/Godot-Project-Template.git
cd Godot-Project-Template
```

Rename the extension to match your project:
```bash
python tools/rename_extension.py myextension your_extension_name
```

## Building

### Desktop

```bash
cmake --preset debug
cmake --build --preset debug
```

Available presets: `debug`, `release`, `dist` (RelWithDebInfo)

### Android

```bash
cmake --preset android-arm64
cmake --build --preset android-arm64
```

Available presets: `android-arm64`, `android-arm32`, `android-x86_64`

### iOS

```bash
cmake --preset ios
cmake --build --preset ios
```

Built binaries are automatically copied to `godot/bin/`.

## Running

Open `godot/project/project.godot` in the Godot editor.

## Testing

```bash
cmake --preset debug -DBUILD_TESTS=ON
cmake --build --preset debug
ctest --test-dir build/debug --output-on-failure
```

Tests use [Catch2](https://github.com/catchorg/Catch2) and cover pure C++ code (non-Godot classes). Add test files to `tests/src/`.

## Project Structure

```
├── cpp/                    C++ extension source code
│   ├── include/            Headers
│   └── src/                Implementation + register_types.cpp
├── godot/
│   ├── bin/                Compiled extension binaries
│   └── project/            Godot project files
├── tests/                  Unit tests (Catch2)
├── third_party/godot-cpp/  Godot C++ bindings (submodule)
├── tools/                  Utility scripts
├── CMakeLists.txt          Top-level CMake configuration
└── CMakePresets.json       Build presets (desktop + mobile)
```

## Adding a New Class

1. Create your header in `cpp/include/` and source in `cpp/src/`
2. If it's a Godot class, register it in `cpp/src/register_types.cpp`:
   ```cpp
   ClassDB::register_class<YourClass>();
   ```
3. Rebuild — the extension is automatically copied to the Godot project

## CI Workflows

- **ci.yml** — Builds and tests on all platforms (manual trigger)
- **build.yml** — Builds release binaries for all platforms and collects them as a downloadable artifact (manual trigger)

## License

[MIT](LICENSE)
