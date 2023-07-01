# nginx-windows-arm
Unofficial ARM builds of NGINX on Windows.

## Compiler
Clang LLVM 16.0.6

## Target
Windows ARM

## Build
MacBook Pro M1 (Cross compile)

## Library version
LibreSSL 3.7.3 pcre 8.45 zlib 1.2.13

## Modules
same as official builds: --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_stub_status_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_auth_request_module --with-http_random_index_module --with-http_secure_link_module --with-http_slice_module --with-mail --with-stream --with-mail_ssl_module --with-stream_ssl_module

## Configure arguments
built by clang 16.0.6 (https://github.com/llvm/llvm-project.git 7cbf1a2591520c2491aa35339f227775f4d3adf6)
built with LibreSSL 3.7.3
TLS SNI support enabled
configure arguments: --prefix= --conf-path=conf/nginx.conf --pid-path=logs/nginx.pid --http-log-path=logs/access.log --error-log-path=logs/error.log --sbin-path=nginx.exe --http-client-body-temp-path=temp/client_body_temp --http-proxy-temp-path=temp/proxy_temp --http-fastcgi-temp-path=temp/fastcgi_temp --http-scgi-temp-path=temp/scgi_temp --http-uwsgi-temp-path=temp/uwsgi_temp --with-cc=aarch64-w64-mingw32-gcc --with-cpp=aarch64-w64-mingw32-g++ --with-pcre=pcre --with-openssl=libressl-3.7.3 --with-zlib=zlib-1.2.13 --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_stub_status_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_auth_request_module --with-http_random_index_module --with-http_secure_link_module --with-http_slice_module --with-mail --with-stream --with-mail_ssl_module --with-stream_ssl_module
