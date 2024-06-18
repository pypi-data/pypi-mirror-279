# SeedMIP

使用步骤：
1. 使用激活码进行激活。
2. 编译并运行应用程序。
3. 其他测试及相关。

## 激活步骤
### 按照以下步骤，编译可执行程序 `license_main`
```
在根目录下
cd license
mkdir build
cd build
cmake ..
make
```
### 获取激活码后进行激活
```
1. 在license/build目录下执行
./license_main ***
将***替换成激活码
激活成功后，提示：SeedMip successfully activated! the license file is written to seedmip.lic，激活文件被写入当前目录的seedmip.lic
2. 将seedmip.lic移入SeedMIP主目录
```
### 设置环境变量
```
# 设置永久环境变量
修改 ~/.bashrc 文件，添加一行：export SEEDMIP_HOME=/home/user/SeedMIP-v-xx.xx
# 使环境变量设置生效
source ~/.bashrc

# 如果只想临时生效，可通过执行以下命令设置临时环境变量
export SEEDMIP_HOME=/home/user/SeedMIP-v-xx.xx
```


## 编译和运行
### 按照以下步骤，编译动态链接库 `libParaILP.so`
```
在根目录下
mkdir build
cd build
cmake ..
make
```

### 编译可执行文件main

```
在根目录下
g++ main.cpp -I"build/include" -L"build/lib" -lParaILP -Wl,-rpath="build/lib" -o main
```

### 运行

```
编译成功后
./main
```

### 编译python wrapper

```
确认build文件夹和libParaILP.so都编译齐全后
在根目录下
g++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` -I./build/include pySeedMIP.cpp -o pySeedMIP`python3-config --extension-suffix` -L./build/lib -lParaILP -Wl,-rpath="build/lib"
```

### 运行python测试程序

```
编译成功后
python pyMain.py
```

## 测试
### 测试相关参考以下repository
```
参考
https://github.com/seedmaas/SeedMIPTest
```
