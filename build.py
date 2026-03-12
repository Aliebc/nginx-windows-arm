#!/usr/bin/env python3
import os
import subprocess
import tempfile
import shutil

os.makedirs('/nginx-build', exist_ok=True)
os.chdir('/nginx-build')

TARGET_HOST = 'aarch64-w64-mingw32'
NGINX_VERSION = '1.29.3'
PCRE_VERSION = '8.45'
LIBRESSL_VERSION = '3.8.4'
LIBZ_VERSION = '1.3.2'

HOST_ARCH = os.uname().machine
if HOST_ARCH == 'arm64':
    HOST_ARCH = 'aarch64'

if HOST_ARCH == 'amd64':
    HOST_ARCH = 'x86_64'

os.environ['HOST'] = TARGET_HOST
os.environ['CC'] = f'{TARGET_HOST}-gcc'

REQUIRMENTS = ['build-essential', 'unzip', 'zip']
for req in REQUIRMENTS:
    os.system(f"sudo apt-get install -y {req}")

### Check curl
try:
    subprocess.run(['curl', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except Exception:
    print(f'[NGINX Builder] Error: curl is not installed. Please install curl and try again.')
    exit(1)

######## Check build-essential
try:
    subprocess.run([f'{TARGET_HOST}-gcc', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except Exception:
    print(f"'{TARGET_HOST}-gcc' is not installed. Installing.")

    DOWNLOAD_URL = f'https://github.com/mstorsjo/llvm-mingw/releases/download/20260311/llvm-mingw-20260311-ucrt-ubuntu-22.04-{HOST_ARCH}.tar.xz'
    INSTALL_DIR = '/usr/local/llvm-mingw'

    with tempfile.TemporaryDirectory() as tmpdir:
        archive_path = os.path.join(tmpdir, 'llvm-mingw.tar.xz')

        subprocess.run(['curl', '-L', '-o', archive_path, DOWNLOAD_URL], check=True)
        subprocess.run(['tar', '-xf', archive_path, '-C', tmpdir], check=True)

        # Find extracted directory
        extracted_dir = None
        for name in os.listdir(tmpdir):
            path = os.path.join(tmpdir, name)
            if os.path.isdir(path) and name.startswith("llvm-mingw"):
                extracted_dir = path
                break

        if extracted_dir is None:
            raise RuntimeError("Failed to locate extracted llvm-mingw directory")

        os.makedirs(INSTALL_DIR, exist_ok=True)

        for item in os.listdir(extracted_dir):
            src = os.path.join(extracted_dir, item)
            dst = os.path.join(INSTALL_DIR, item)

            if os.path.exists(dst):
                continue

            subprocess.run(['sudo', 'mv', src, dst], check=True)

        os.environ['PATH'] = f"{INSTALL_DIR}/bin:" + os.environ['PATH']
        
try:
    subprocess.run([f'{TARGET_HOST}-gcc', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f'[NGINX Builder] {TARGET_HOST}-gcc is installed.')
except Exception:
    print(f'[NGINX Builder] Error: Failed to install {TARGET_HOST}-gcc. Please check the installation and try again.')
    exit(1)

print('[NGINX Builder] All dependencies are installed.')

######## Download and build Nginx
NGINX_URL = f'http://nginx.org/download/nginx-{NGINX_VERSION}.tar.gz'
NGINX_ARCHIVE = f'nginx-{NGINX_VERSION}.tar.gz'
NGINX_DIR = f'nginx-{NGINX_VERSION}'

if not os.path.exists(NGINX_ARCHIVE):
    print(f'[NGINX Builder] Downloading Nginx {NGINX_VERSION}...')
    subprocess.run(['curl', '-L', '-o', NGINX_ARCHIVE, NGINX_URL], check=True)
else:
    print(f'[NGINX Builder] Nginx archive already exists. Skipping download.')

if not os.path.exists(NGINX_DIR):
    print(f'[NGINX Builder] Extracting Nginx...')
    subprocess.run(['tar', '-xf', NGINX_ARCHIVE], check=True)
else:
    print(f'[NGINX Builder] Nginx directory already exists. Skipping extraction.')
    
##### Download Modules
os.chdir(NGINX_DIR)
print(f'[NGINX Builder] Configuring Nginx for {TARGET_HOST}...')
os.makedirs('modules', exist_ok=True)
os.chdir('modules')
## PCRE
PCRE_LINK = "http://ftp.cs.stanford.edu/pub/exim/pcre/pcre-8.45.tar.gz"
PCRE_ARCHIVE = 'pcre-8.45.tar.gz'
PCRE_DIR = 'pcre-8.45'
if not os.path.exists(PCRE_ARCHIVE):
    print(f'[NGINX Builder] Downloading PCRE {PCRE_VERSION}...')
    subprocess.run(['curl', '-L', '-o', PCRE_ARCHIVE, PCRE_LINK], check=True)
else:
    print(f'[NGINX Builder] PCRE archive already exists. Skipping download.')
if not os.path.exists(PCRE_DIR):
    print(f'[NGINX Builder] Extracting PCRE...')
    subprocess.run(['tar', '-xf', PCRE_ARCHIVE], check=True)
else:
    print(f'[NGINX Builder] PCRE directory already exists. Skipping extraction.')
    
## OpenSSL(LibreSSL)
LIBRE_SSL_LINK = f'https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-{LIBRESSL_VERSION}.tar.gz'
LIBRE_SSL_ARCHIVE = f'libressl-{LIBRESSL_VERSION}.tar.gz'
LIBRE_SSL_DIR = f'libressl-{LIBRESSL_VERSION}'

if not os.path.exists(LIBRE_SSL_ARCHIVE):
    print(f'[NGINX Builder] Downloading LibreSSL {LIBRESSL_VERSION}...')
    subprocess.run(['curl', '-L', '-o', LIBRE_SSL_ARCHIVE, LIBRE_SSL_LINK], check=True)
else:
    print(f'[NGINX Builder] LibreSSL archive already exists. Skipping download.')

if not os.path.exists(LIBRE_SSL_DIR):
    print(f'[NGINX Builder] Extracting LibreSSL...')
    subprocess.run(['tar', '-xf', LIBRE_SSL_ARCHIVE], check=True)
else:
    print(f'[NGINX Builder] LibreSSL directory already exists. Skipping extraction.')

## Libz
LIBZ_LINK = f'https://github.com/madler/zlib/releases/download/v{LIBZ_VERSION}/zlib-{LIBZ_VERSION}.tar.gz'
LIBZ_ARCHIVE = f'zlib-{LIBZ_VERSION}.tar.gz'
LIBZ_DIR = f'zlib-{LIBZ_VERSION}'

if not os.path.exists(LIBZ_ARCHIVE):
    print(f'[NGINX Builder] Downloading Libz {LIBZ_VERSION}...')
    subprocess.run(['curl', '-L', '-o', LIBZ_ARCHIVE, LIBZ_LINK], check=True)
else:
    print(f'[NGINX Builder] Libz archive already exists. Skipping download.')

if not os.path.exists(LIBZ_DIR):
    print(f'[NGINX Builder] Extracting Libz...')
    subprocess.run(['tar', '-xf', LIBZ_ARCHIVE], check=True)
else:
    print(f'[NGINX Builder] Libz directory already exists. Skipping extraction.')
    
os.chdir('..')

# Build Resource
# aarch64-w64-mingw32-windres src/os/win32/nginx.rc -o objs/nginx-rc.o
try:
    subprocess.run(['aarch64-w64-mingw32-windres', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open('src/os/win32/nginx.rc', 'r') as f:
        content = f.read()
        content = content.replace('\\\\', '/')
        os.makedirs('objs', exist_ok=True)
    with open('src/os/win32/nginx.rc', 'w') as f:
        f.write(content)
    subprocess.run([
        'aarch64-w64-mingw32-windres', 'src/os/win32/nginx.rc', '-o', 'objs/nginx-rc.o'
    ])
    print(f'[NGINX Builder] Resource file built successfully.')
except Exception:
    print(f'[NGINX Builder] Error: aarch64-w64-mingw32-windres is not installed. Please install it and try again.')
    exit(1)

if not os.path.exists('objs/nginx-rc.o'):
    print(f'[NGINX Builder] Error: Failed to build resource file. Please check the build output for details.')
    exit(1)
    
# Configure Nginx
with open(os.path.join(os.path.dirname(__file__), 'configure_args.txt'), 'r') as f:
    configure_args = f.read().splitlines()
    for i, line in enumerate(configure_args):
        configure_args[i] = line.replace('__OPENSSL_DIR__', f'modules/{LIBRE_SSL_DIR}')
        configure_args[i] = configure_args[i].replace('__PCRE_DIR__', f'modules/{PCRE_DIR}')
        configure_args[i] = configure_args[i].replace('__ZLIB_DIR__', f'modules/{LIBZ_DIR}')
    
## REPLACE auto conf (PCRE)
try:
    pcre_conf_path = os.path.join('auto', 'lib', 'pcre', 'make')
    with open(pcre_conf_path, 'r') as f:
        content = f.read()
    content = content.replace('./configure', './configure --host=aarch64-w64-mingw32')
    with open(pcre_conf_path, 'w') as f:
        f.write(content)
    print(f'[NGINX Builder] Updated PCRE configuration for cross-compilation.')
except Exception as e:
    print(f'[NGINX Builder] Warning: Failed to update PCRE configuration. Cross-compilation may fail. Please check the file {pcre_conf_path} and update it manually if necessary.')
    print(e)

## REPLACE auto conf (OpenSSL)
try:
    openssl_conf_path = os.path.join('auto', 'lib', 'openssl', 'make')
    with open(openssl_conf_path, 'r') as f:
        content = f.read()
    if 'configure' not in content:
        content = content.replace('./config', f'./configure --host=aarch64-w64-mingw32 --build={HOST_ARCH}-linux-gnu ')
    with open(openssl_conf_path, 'w') as f:
        f.write(content)
    print(f'[NGINX Builder] Updated OpenSSL configuration for cross-compilation.')
except Exception as e:
    print(f'[NGINX Builder] Warning: Failed to update OpenSSL configuration. Cross-compilation may fail. Please check the file {openssl_conf_path} and update it manually if necessary.')
    print(e)
    
## REPLACE auto conf (ZLib)
try:
    zlib_conf_path = os.path.join('auto', 'lib', 'zlib', 'make')
    with open(zlib_conf_path, 'r') as f:
        content = f.read()
    content = content.replace('./configure', f'CHOST=aarch64-w64-mingw32 ./configure')
    with open(zlib_conf_path, 'w') as f:
        f.write(content)
    print(f'[NGINX Builder] Updated ZLib configuration for cross-compilation.')
except Exception as e:
    print(f'[NGINX Builder] Warning: Failed to update ZLib configuration. Cross-compilation may fail. Please check the file {zlib_conf_path} and update it manually if necessary.')
    print(e)
    
configure_command = configure_args
print(f'[NGINX Builder] Configuring Nginx with command: {" ".join(configure_command)}')
try:
    subprocess.run(configure_command, check=True)
    print(f'[NGINX Builder] Nginx configured successfully.')
except subprocess.CalledProcessError as e:
    print(f'[NGINX Builder] Error: Failed to configure Nginx. Please check the output for details.')
    print(e)
    
# Add bcrypt in objs/Makefile
try:
    makefile_path = os.path.join('objs', 'Makefile')
    with open(makefile_path, 'r') as f:
        content = f.read()
    if '-lbcrypt' not in content:
        content = content.replace('-lcrypt32', '-lcrypt32 -lbcrypt')
        with open(makefile_path, 'w') as f:
            f.write(content)
        print(f'[NGINX Builder] Updated Makefile to include bcrypt library.')
    else:
        print(f'[NGINX Builder] Makefile already includes bcrypt library. Skipping update.')
except Exception as e:
    print(f'[NGINX Builder] Warning: Failed to update Makefile. The bcrypt library may not be included in the build. Please check the file {makefile_path} and update it manually if necessary.')
    print(e)
    
NPROC = os.cpu_count() or 1
try:
    subprocess.run(['make', f'-j{NPROC}'], check=True)
    print(f'[NGINX Builder] Nginx built successfully.')
except subprocess.CalledProcessError as e:
    print(f'[NGINX Builder] Error: Failed to build Nginx. Please check the output for details.')
    print(e)
    
### STRIP the binary
try:
    subprocess.run(['aarch64-w64-mingw32-strip', 'objs/nginx.exe'], check=True)
    print(f'[NGINX Builder] Stripped the binary successfully.')
except Exception:
    print(f'[NGINX Builder] Warning: Failed to strip the binary. The final executable may be larger than necessary. Please check if aarch64-w64-mingw32-strip is installed and try stripping the binary manually if necessary.')
    
### Download offical NGINX ZIP
NGINX_LINK = f'https://nginx.org/download/nginx-{NGINX_VERSION}.zip'
NGINX_ZIP = f'nginx-{NGINX_VERSION}.zip'

if not os.path.exists(NGINX_ZIP):
    print(f'[NGINX Builder] Downloading official Nginx ZIP...')
    subprocess.run(['curl', '-L', '-o', NGINX_ZIP, NGINX_LINK], check=True)
else:
    print(f'[NGINX Builder] Official Nginx ZIP already exists. Skipping download.')
    
# UNZIP
try:
    subprocess.run(['unzip', '-o', NGINX_ZIP], check=True)
    print(f'[NGINX Builder] Unzipped official Nginx ZIP successfully.')
except subprocess.CalledProcessError as e:
    print(f'[NGINX Builder] Error: Failed to unzip official Nginx ZIP. Please check the output for details.')
    print(e)
    
# Replace the built binary with the official one
try:
    os.remove(f'nginx-{NGINX_VERSION}/nginx.exe')
    shutil.copy('objs/nginx.exe', f'nginx-{NGINX_VERSION}/nginx.exe')
    print(f'[NGINX Builder] Replaced the official Nginx binary with the built one successfully.')
except Exception as e:
    print(f'[NGINX Builder] Error: Failed to replace the official Nginx binary. Please check the output for details.')
    print(e)

# Compress the final output
try:
    subprocess.run(['zip', '-r', f'nginx-{NGINX_VERSION}-windows-aarch64.zip', f'nginx-{NGINX_VERSION}'], check=True)
    print(f'[NGINX Builder] Compressed the final output successfully.')
except subprocess.CalledProcessError as e:
    print(f'[NGINX Builder] Error: Failed to compress the final output. Please check the output for details.')
    print(e)
    
shutil.copy(f'nginx-{NGINX_VERSION}-windows-aarch64.zip', f'/nginx-{NGINX_VERSION}-windows-aarch64.zip')
print(f'[NGINX Builder] Final output copied to /nginx-{NGINX_VERSION}-windows-aarch64.zip')

exit(0)
##### Clean all build files
os.chdir('/')
if os.path.exists('/nginx-build'):
    shutil.rmtree('/nginx-build')
print(f'[NGINX Builder] Cleaned build files.')