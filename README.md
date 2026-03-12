# nginx-windows-arm

Unofficial ARM builds of NGINX for Windows.

This project provides a build script that cross-compiles **NGINX for Windows ARM64 (aarch64)** from Linux using the **MinGW LLVM toolchain**.  
The script downloads all required dependencies, builds NGINX with them, and packages the final Windows ARM executable into a distributable ZIP archive.

> ⚠️ These builds are **unofficial** and are **not provided or supported by the official NGINX project**.

---

## Features

- Cross-compile **NGINX for Windows ARM64**
- Automatic dependency setup
- Downloads and builds required libraries:
  - PCRE
  - LibreSSL
  - Zlib
- Uses **llvm-mingw** toolchain
- Generates a ready-to-use **Windows ZIP package**
- Automatically strips the binary to reduce size
- Repackages the official NGINX Windows distribution with the ARM64 executable

---

## Build Environment

The script is designed to run on **Ubuntu / Debian Linux**.

Requirements:

- Python 3
- curl
- unzip
- zip
- build-essential

These dependencies are automatically installed by the script.

---

## Toolchain

The build uses:

- **llvm-mingw**
- target: `aarch64-w64-mingw32`
- Windows ARM64 executable output

If the cross compiler is not installed, the script automatically downloads it from:

https://github.com/mstorsjo/llvm-mingw

---

## Libraries Built From Source

The following libraries are downloaded and compiled during the build:

| Library | Version |
|--------|--------|
| PCRE | 8.45 |
| LibreSSL | 3.8.4 |
| Zlib | 1.3.2 |
