## 环境准备及运行

下载并安装 python3 解释器（推荐 3.9）：

https://www.python.org/downloads/

在命令行中，使用 pip 安装依赖包：

```shell
pip install pillow pygame
```

导航到游戏文件夹，运行 color_hit.py 进行游戏：

```shell
python color_hit.py
```

命令中的 pip 和 python 可能需要更改为 pip3 和 python3，取决于具体的环境变量。如果使用 conda 管理环境，先新建一个运行环境：

```shell
conda create -n game python==3.9
```

激活环境：

```shell
conda activate game
```

让 conda 同步 pip 安装的包：

```shell
conda config --set pip_interop_enabled true
```

然后使用 pip 安装 pillow 和 pygame 后运行游戏。

若要打包可以使用 pyinstaller，先安装 pyinstaller：

```shell
pip install pyinstaller
```

然后打包(注意在 Windows 上需要先将 pack.spec 中文件路径中的 "/" 修改为 "\\")：

```shell
pyinstaller -noconfirm pack.spec
```

打包完成后可执行文件及应用程序位于 dist 文件夹。当前 dist 中的 color_hit.app 是在 macOS arm64 上打包的，在其他平台可能无法运行。

## 更改游戏设置

游戏设置位于 src/config.py，里面的变量都有注释，可根据自己的需求进行更改。