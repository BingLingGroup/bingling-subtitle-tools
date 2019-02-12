# 冰灵工具箱

<img src="icon/bingling.png" width="128px">

冰灵工具箱能对[.ass](http://moodub.free.fr/video/ass-specs.doc)(Advanced SubStation Alpha)字幕文件进行批量处理。

## 目录

1. [用到的其他开源项目](#用到的其他开源项目)
2. [本项目的开源许可](#本项目的开源许可)
3. [安装](#安装)
4. [介绍](#介绍)
5. [功能](#功能)
6. [命令行选项](#命令行选项)
7. [配置文件](#配置文件)
8. [构建\(Build\)](#构建Build)
9. [问题反馈](#问题反馈)

## 用到的其他开源项目

- [asstosrt](https://github.com/sorz/asstosrt) - [file_io.py](../bingling_subtitle_tools/file_io.py)中有部分代码参考此项目，这是其采用的[MIT协议声明文件](notice/asstosrt/MIT_LICENSE)
- [Chardet](https://github.com/chardet/chardet) - [file_io.py](../bingling_subtitle_tools/file_io.py)用到了该模块，这是其采用[LGPL协议](https://github.com/chardet/chardet/blob/master/LICENSE)
- [kennethreitz/setup.py](https://github.com/kennethreitz/setup.py) - [setup.py](../setup.py)参考此项目，这是其采用的[MIT协议声明文件](notice/kennethreitz_setup_py/MIT_LICENSE)

## 本项目的开源许可

[GPLv3](../LICENSE)

## 安装

### windows用户直接[下载](https://github.com/BingLingGroup/bingling-subtitle-tools/releases/download/v0.0.2/bingling_subtitle_tools_win.7z)使用

#### 独立程序优点

- windows用户解压后可以直接使用，不需要python环境和pip包管理器。

#### 独立程序缺点

- 不能跨平台使用。
- 除非加上路径，否则无法在别的目录使用程序。

本程序使用Nuitka和mingw-w64进行编译，详见[构建\(Build\)](#构建Build)。

解压后，可以编辑文件夹内的config.py配置文件，然后点击run.bat让程序读取该[配置](#配置文件)并运行。

### 使用pip通过setup.py安装

#### setup.py优点

- 可以在绝大多数目录下，启动命令行，直接输入bingling_subtitle_tools来使用程序。

- 不需要考虑平台问题。

#### setup.py缺点

- 需要额外安装python环境和pip包管理器。

推荐windows用户使用[chocolatey包管理器](https://chocolatey.org/)安装python，这样配置系统环境变量和升级相关软件包更方便。

已有[python环境](https://www.python.org/)和[pip包管理器](https://pypi.org/project/pip/)的情况，下载源代码压缩包。源代码压缩包可以是项目主页的"Clone or download--Download ZIP"得到，或者是"[Release页面](https://github.com/BingLingGroup/bingling-subtitle-tools/releases)--Source code(zip)"。

解压后，切换到setup.py所在目录，然后运行这条命令。这句命令最后有一个"."表示当前目录。

    pip install .

或者windows用户也可以选择直接运行[pip_install.bat](../build_cmds/pip_install.bat)。

不建议使用[easy_install](../build_cmds/easy_install.bat)工具直接安装，因为easy_install无法对程序进行卸载操作。

### 使用pip卸载

[pip_uninstall.bat](../build_cmds/pip_uninstall.bat)

    pip uninstall bingling_subtitle_tools

## 介绍

冰灵工具箱是一个用python写的命令行程序，需要python版本在3.4以上，但是不限特定平台。目前的功能可以做到分离不同样式的.ass文本和删除.ass部分(section)。采用[GPLv3](../LICENSE)开源协议，该协议[简体中文译本](https://jxself.org/translations/gpl-3.zh.shtml)。

本程序[图标](icon/bingling.svg)使用[inkscape](https://inkscape.org/zh/)绘制，[图标](icon/bingling.svg)字体使用[思源宋体](https://source.typekit.com/source-han-serif/cn/)，该字体采用[SIL授权协议](https://github.com/adobe-fonts/source-han-serif/blob/release/LICENSE.txt)。

## 功能

### 已实现功能

- [x] 批量分离并导出多语言字幕的不同语言部分的纯文本内容（不同语言使用的样式不同，且每种语言在不同的字幕行上）
  - [x] 支持导出这些字幕的时间轴部分到单独的文件中(但没有.ass文件的其他部分，不能被aegisub直接打开)
  - [x] 支持按照不同样式分类导出其纯文本部分
  - [x] 支持消除文本部分的.ass[标签](https://aegi.vmoe.info/docs/3.2/ASS_Tags/)(override codes/tags)
  - [x] ……
- [x] 批量删除恼人的[Aegisub Project Garbage]部分
  - [x] 支持覆盖保存
  - [x] 支持删除多个指定的.ass部分(section)
  - [x] ……

### 未实现功能

- [ ] 批量分离多语言字幕文件为单语言字幕文件
- [ ] 批量分离时间轴为单独的字幕文件
- [ ] 批量合并多语言字幕文本和时间轴
- [ ] 支持指定编码输出
- [ ] ……

## 命令行选项

冰灵工具箱作为命令行程序，支持使用命令行选项参数对程序进行操作，以下为选项和参数的使用方法。

- arg_num指的是该选项需要的参数个数，default指的是该选项不使用时默认的参数值。

- 非全局的子选项只有在特定选项输入后才起作用，子选项标注在各自父选项的标题下面。

- 确保有引号包围着含空格的输入参数。

### 命令行选项概览

    bingling_subtitle_tools [-h] [-c CONFIG] [-i [INPUT_ [INPUT_ ...]]]
                            [-o [OUTPUT [OUTPUT ...]] [-es]
                            [-fn [FIELD_NAME]] [-msg[STRING]]
                            [-nts [STRING [STRING...]]]
                            [-ft [FIELD_CONTENT[FIELD_CONTENT ...]]]
                            [-te] [-rn] [-koc] [-nfe [-lo] [-ds]
                            [-sc SECTION_NAME[SECTION_NAME ...]]
                            [-nt [STRING]] [-ow] [-v]

### 全局选项

    -h, --help          显示帮助信息并退出
    -v, --version       显示当前程序版本并退出
    -c CONFIG, --config CONFIG
                        指定一个存储着命令行选项和参数的配置文件，
                        现在只支持.py格式。
                        如果使用了这个选项，其他命令行选项都会被忽略。
                        [arg_num = 1]
    -i [INPUT_ [INPUT_ ...]], --input [INPUT_ [INPUT_ ...]]
                        输入待处理文件所在文件夹名，
                        程序会处理所有该文件夹内的.ass文件。
                        [arg_num ≥ 0]
                        [default: 程序当前运行目录]
    -o [OUTPUT [OUTPUT ...]], --output [OUTPUT [OUTPUT ...]]
                        输出文件所在文件夹，只有当输出文件夹存在
                        并且和输入文件夹有相同数量才会起作用。
                        否则程序会使用默认路径。
                        [arg_num ≥ 0]
                        [default: 在输入文件夹下
                        建立一个名叫"new"的新文件夹]

### 简易文本导出选项("export simply" option)

此选项可根据.ass的事件(event)，也就是根据一行时间轴内容中的特定字段(field)的内容(field content)进行分类导出。前面所说的分离导出多样式字幕的不同部分的纯文本内容的功能就是这个选项实现的。类似于aegisub中的“导出字幕--Plain-Text”，但是支持多文件批量操作和根据特定.ass事件字段进行筛选的功能。

需要指出的是，一般来讲没必要使用"--no-forced-encoding"选项，一是windows10对utf-8无BOM编码没有支持问题，aegisub3.2.2也可以正常读取，二是[python官方文档](https://docs.python.org/3/library/codecs.html#encodings-and-unicode)建议使用无BOM编码。

>In UTF-8, the use of the BOM is discouraged and should generally be avoided.

    -es, --exp-smp      启动简易文本导出功能。
                        [arg_num = 0]
    -fn [FIELD_NAME], --field-name [FIELD_NAME]
                        用于分离.ass文件不同部分的字段，
                        输入选项但不输入参数表示使用默认参数。
                        [arg_num = 0 或 1]
                        [default: Style]
    -msg [STRING], --custom-msg [STRING]
                        在输出文件的首行写入一段自定义信息。
                        输入选项但不输入参数表示不添加自定义信息。
                        [arg_num = 0 或 1]
                        [default: # Exported by
                        BingLingSubtitleTools+(当前版本号)]
    -nts [STRING [STRING ...]],
    --name-tails [STRING [STRING ...]]
                        多个输出文件名后缀，在扩展名之前，不是修改扩展名。
                        输出文件扩展名总为txt。
                        输入选项但不输入参数表示
                        按照前面所输入的字段名取出字段内容作为文件名后缀。
                        只有当文件名后缀的数量和filter选项的参数数量一致
                        才会起作用。
                        一个字段内容对应一个输出文件名后缀，
                        和filter选项的顺序一致。
                        默认参数中的"..., ..."意思是默认有两个参数。
                        类似的表示方法说明后面不再赘述。
                        [arg_num ≥ 0]  
                        [default: ["_CN", "_EN"]]
    -ft [FIELD_CONTENT [FIELD_CONTENT ...]], 
    --filter [FIELD_CONTENT [FIELD_CONTENT ...]]
                        用于筛选字幕事件，也就是字幕行的字段内容。
                        输入选项但不输入参数表示禁用筛选功能，
                        此时所有字幕行都会根据前面指定的字段，
                        全部按照不同的字段内容分类输出。
                        [arg_num≥ 0]
                        [default: ["中文字幕", "英文字幕"]]
    -te, --text-excluded  
                        允许输出不包含文本的事件部分，也就是时间轴部分。
                        这部分文件会加上额外的文件名后缀"_t"。
                        [arg_num = 0]
    -rn, --rename-number  
                        允许将输出名称重命名为类似Exx的格式，
                        其中xx来自于文件名中已经有的数字。
                        注意此修改只是将原来的文件名修改为Exx，
                        前面选项中指定的文件名后缀依然会添加。
                        [arg_num = 0]
    -koc, -es: --keep-override-code
                        导出时保留.ass标签，而不是默认删除它们。
                        [arg_num = 0]
    -nfe, --no-forced-encoding
                        禁用默认情况下强制输出文件编码为无BOM的utf-8格式，
                        同时也是禁用unix LF(Line Feed)行尾序列
                        而让输出文件保持检测到的输入编码
                        并启用windows CR(Carriage Return)LF行尾序列。
                        [arg_num = 0]
    -lo, --limited-output
                        限制输出文件夹为第一个"-o/--output"选项的参数。
                        [arg_num = 0]

### 部分删除选项("delete section" option)

    -ds, --del-sect     启动部分删除功能
                        [arg_num = 0]
    -sc SECTION_NAME [SECTION_NAME ...], --sect-name SECTION_NAME [SECTION_NAME ...]
                        要删除的部分名称。
                        [arg_num > 0]
                        [default: ["[Aegisub Project Garbage]"]]
    -nt [STRING], --name-tail [STRING]
                        一个输出文件名后缀。
                        输入选项但不输入参数表示不使用文件名后缀。
                        [arg_num = 0 or 1]
                        [default: _new]
    -ow, --overwrite    [警告] 允许覆盖输入文件。
                        使用这个选项会忽略"-o/--output"选项
                        提供的输出路径参数
                        和"-nt/--name-tail"选项提供的文件名后缀。
                        而不使用这个选项会阻止任何企图覆盖输入文件的请求。
                        [arg_num = 0]

## 配置文件

以上命令行选项也可以使用配置文件进行设置，详见[example_config.py](example_config.py)。

## 构建\(Build\)

构建之前确保自己电脑上已经有python环境和pip包管理器。

### 使用Nuitka编译

[Nuitka](http://nuitka.net/)是一个python的替代编译器，可以编译出脱离python运行环境运行的可执行文件。

使用前先安装Nuitka。

    pip install Nuitka

之后确保自己电脑上有64位C++编译环境，并已添加在系统环境变量中。如windows也可以使用[mingw-w64](http://mingw-w64.org/doku.php/download/mingw-builds)进行编译，但一定要确定其命令可在命令行下可用，确保已添加到系统环境变量中，不然会出现如此[问题](https://github.com/Nuitka/Nuitka/issues/35)。

然后参照Nuitka的[文档](http://nuitka.net/doc/user-manual.html)配置参数进行编译。

windows编译可以使用[nuitka_build.bat](../build_cmds/nuitka_build.bat)，或者是会自动输出日志文件的批处理[nuitka_build_log.bat](../build_cmds/nuitka_build_log.bat)。

编译产生的文件会输出在../.build_and_dist/bingling_subtitle_tools.build和../.build_and_dist/bingling_subtitle_tools.dist文件夹中。其中exe文件在../.build_and_dist/bingling_subtitle_tools.dist中。

### Nuitka编译的windows发布\(release\)包制作

在编译完成，确定相关文件生成，且7z.exe在系统环境变量或者在[该文件夹](../build_cmds/)中可以使用时，可以点击[create_release.bat](../build_cmds/create_release.bat)制作windows发布包。

该发布包会产生在../.release文件夹中。

### 使用Pyintaller打包

[Pyinstaller](https://www.pyinstaller.org/)是一个python的打包程序，可以将python依赖环境和python源代码打包成可执行文件，以便在没有python环境的电脑上运行。

使用前先安装Pyinstaller。

    pip install Pyinstaller

然后参照Pyinstaller的[文档](https://pyinstaller.readthedocs.io/en/stable/)配置参数进行编译。

windows编译可以使用[pyinstaller_build.bat](../build_cmds/pyinstaller_build.bat)或者参照[pyinstaller_build.spec](../build_cmds/pyinstaller_build.spec)进行编译。

编译产生的文件会输出在../.build_and_dist/pyinstaller.build文件夹中。

## 问题反馈

目前程序仍处在早期开发阶段，有任何问题可以来[这里](https://github.com/BingLingGroup/bingling-subtitle-tools/issues)讨论。