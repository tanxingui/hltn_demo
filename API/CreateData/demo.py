import ssl, subprocess, os, sys
print("Python", sys.version)
print("OpenSSL 版本:", ssl.OPENSSL_VERSION)
print("动态库路径:")
if sys.platform == "win32":
    import ctypes
    dll = ctypes.CDLL("libssl-3-x64.dll")      # 3.x 正确文件名
    print("已加载", dll._name)
else:
    print(subprocess.check_output(["lsof", "-p", str(os.getpid()), "|", "grep", "libssl"], text=True))