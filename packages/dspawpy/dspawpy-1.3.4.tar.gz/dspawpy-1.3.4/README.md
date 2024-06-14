![Pyversion](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fgeojson-rewind%2Fjson)
![PyPI](https://img.shields.io/pypi/v/dspawpy?label=pypi%20package)
![PyPI - Downloads](https://static.pepy.tech/badge/dspawpy/month)

# Introduction （简介）

dspawpy is a post-processing tool mainly for DFT package [DS-PAW](https://cloud.hzwtech.com/web/product-service?id=10), providing some functions of data capture, conversion, structure conversion, and drawing. （dspawpy 主要是 [DS-PAW](https://cloud.hzwtech.com/web/product-service?id=10) 软件的后处理辅助工具，提供一些数据抓取、换算、结构转化、绘图功能）

## Installation （安装）

Either by pip: （通过pip安装）

```bash
pip install dspawpy -U --user
```

Or by conda: （通过conda安装）

```bash
conda install -c conda-forge dspawpy
```

## CHANGELOG （版本更新简述）

### 1.3.3

- BUG修复： 修正cli功能2的提示词中的细节错误，写明具体的文件名匹配规则
- BUG修复： 修正cli功能12和13的提示词中的细节

### 1.3.2

- 重要变更： 使用python3.8以下版本将无法启动程序
- 重要变更： 正式用 polars 库替换 pandas 库
- BUG修复： 移除setup.py中已不存在的ecli入口
- BUG修复： wannier.json 不存在 SpinType 键导致读取失败
- BUG修复： 瓦尼尔能带对比时，未正确读取 system.json 中的费米能级信息

### 1.3.1

- BUG修复： 修复userscripts和cli中的一些问题
- BUG修复： 修复json文件读取函数中的导包语句缺失问题
- 功能强化： 10.2 支持读取aimd.json文件绘制物理量变化曲线图（仅无法读取压力变化）

### 1.3.0

- 重要变更： 不再支持python3.8（不含）以下版本
- 重要变更： 合并cli.py和cli_en.py，通过命令行选项 -l 或 --language 切换交互提示语言
- 重构： 命令行交互程序增加静默运行模式，便于编程调用
- 重构： 命令行交互程序大幅提高可读性，在等待用户输入同时多线程动态载入最终调用的函数
- 重构： 懒导入——将导包语句从文件开头尽量移入函数中，避免导入不必要模块，减少导包耗时
- 重构： 绝大多数参数补充类型提示，解决所有已知的静态检查问题
- 体验优化： cli在输入部分参数时增加Tab键获取提示的功能
- 体验优化： cli增加命令行参数帮助菜单
- 体验优化： 全局使用 loguru 库的 catch 修饰器，控制报错信息的详细程度
- 体验优化:  average_along_axis potential类型支持自动判断内部subtype类型为 TotalLocalPotential 的情况
- 体验优化： 用 polars 库替换了 pandas 库，加速处理多维数据
- BUG修复： write_vesta 插值体积数据部分变量未及时更新
- BUG修复： rdf 修复 density 变量缺失的问题
- BUG修复： cli 8.4 neb 


### 1.2.2

- BUG修复： dos和band读取非线性自旋算例的 h5/json 输出文件时，对自旋判断不准

### 1.2.0

- 体验优化： cli将导包语句从文件开头移入函数中，大幅减少python脚本的import时间
- 体验优化： cli增加模糊匹配功能
- 体验优化： optical绘图默认绘制全部数据以便查看
- 体验优化： neb备份时如果目标文件夹已存在，将原先的改名成附加时间戳的文件夹
- BUG修复： dos非线性自旋时无法读取h5/json数据

### 1.1.9

- BUG修复： 修复cli的一些已知bug

### 1.1.8

- 功能强化： 体数据（volumetric data）支持自定义网格插值（调用scipy的RegularGridInterpolator插值器）；增加 txt 格式支持，每行包含格点的 xyz 坐标和具体数值

### 1.1.7

- BUG修复： 修复conda install dspawpy后cli没有同步安装导致无法唤起的故障
- BUG修复： 移除 plot_dos 函数中 xlim、ylim两个参数类型提示，以避免python<3.9的运行错误
- BUG修复： 老版本python, pymatgen, monty等第三方库的兼容性问题

### 1.1.6

- 重要变更： cli 环境部署模块改成dspawpy更新模块，因为现在cli内置于dspawpy中，在hzw机器上唤起cli必定已经source环境了，不再需要原先的1.1功能；仅保留原先的1.2功能，即升级dspawpy
- BUG修复： 移除 plot_dos 函数中 xlim、ylim两个参数类型提示时使用的 | 符号（需要python3.10支持），以避免python<3.10的运行错误

### 1.1.5

- 功能强化： 从pmg中提取plot_dos函数，增加raw参数用于输出投影态密度绘图坐标点数据到dos_raw.csv，使用案例请参考辅助工具使用教程——dos部分

### 1.1.4

- BUG修复： cli 5-6 d带中心参数传递错误
- BUG修复： cli 7-1 内部传参错误
- BUG修复： structure结构写成文件时应采用元素符号而不是带电荷的species
- BUG修复： __init__.py 中版本号未及时更新(影响1.1.2和1.1.3两个版本)

### 1.1.3

- BUG修复： 增加cli所需两个依赖，移除python3.12的语法警告

### 1.1.2

- 功能强化： cli 默认调用 agg 作为matplotlib的绘图后端，避免在某些linux服务器上由于X11转发未设置导致的QT相关问题
- 功能强化： cli 优化NEB链功能提示语
- BUG修复： 兼容python3.12和numpy>1.24
- BUG修复： 用户脚本兼容新旧pymatgen
- BUG修复： NEB续算默认备份文件夹改名成backup

### 1.1.1

- 重要变更： cli并入dspapwy，不需要再去官网下载cli了
- 功能强化： cli多处细节优化，提升交互体验
- 功能强化： 增加 dump_bs_raw() 和 dump_dos_raw() 函数，功能有限

### 1.1.0

- BUG修复： io.write.write_VESTA() 和 io.write.write_delta_rho_vesta() 增加 inorm 参数，用于控制是否归一化（默认关闭）
- 功能强化： io.write.write_VESTA() 和 io.write.write_delta_rho_vesta() 增加 compact 参数，可以在不影响VESTA显示效果的前提下，减小写出的文件（如 .cube ）体积（默认关闭）
- 功能强化： 新增 bdplot() 函数（基于pymatgen的BSDOSPlotter类的get_plot函数优化），用于绘制能带态密度图，详见手册说明

### 1.0.9

- BUG修复： as结构文件中的原子自由度标签可以将 Fix_x Fix_y Fix_z 缩写为 Fix，其他内容不变
- 重要变更： 使用 diffusion.nebtools.write_json_chain/write_xyz_chain() 生成NEB链时如果step=-1，则优先读取 latestStructureXX.as，失败后尝试 nebXX.h5，最后尝试 nebXX.json；可以使用 ignorels 参数忽略 latestStructureXX.as

### 1.0.8

- BUG修复： 准备弃用的 build_Structures_from_datafile() 未返回结构，read() 不受影响；其他调用 build_Structures_from_datafile() 的函数改为调用 read
- BUG修复： 修复 io.read.get_band_data() 考虑自旋且设置了zero_to_efermi时，自旋向下能带数据解析错误的问题
- 功能强化： io.structure模块新增 read() 代替 build_Structures_from_datafile()，write() 代替 io.write.to_file()，convert() 封装 read() 和 write() 函数，便于快速调用

### 1.0.5

- 功能强化： to_file() 写pdb文件时，结构可以不含晶胞信息

### 1.0.4

- BUG修复： build_Structures_from_datafile()选择原子序号时上限设置，h5文件里最后一个离子步信息改成尝试读取
- 功能强化： build_Structures_from_datafile()支持读取pdb格式
- 细节修改： AIMD读不到PressureKinetic信息时增加相应警告

### 1.0.3

- BUG修复： 解决浮点数过大时volumetricData相关文件浮点数粘在一起的问题
- BUG修复： plot_barrier()读取neb.h5/json绘制能垒图时，反应坐标依旧累加
- BUG修复： plot_bandunfolding()能带反折叠费米能级被默认置零
- 功能强化： 新增cube格式用于保存volumetricData
- 功能强化： 全局支持相对路径与绝对路径混写
- 功能强化： datafile参数以及io.read以及diffusion.nebtools模块中的相应参数，可以是文件位置，也可以是文件所在的文件夹路径
- 功能强化： build_Structures_from_datafile()增加task参数，用于配合datafile为文件夹路径的情况
- 重要变更： 移除中文提示语句，精简提示信息
- 重要变更： volumetricData默认使用cube格式写入
- 重要变更： 移除thermo_correction()，一个单纯的外包装函数
- 细节修改： 保存图片或文件时，统一使用 ==> 标记文件绝对路径

### 1.0.2

- BUG修复：  当存在Fix或Mag信息时，structure.as 坐标类型可能解析错误的问题
- 功能强化： 预览NEB链条函数改名 write_xyz(json)_chain，增加dst参数制定保存路径
- 功能强化： potential 中数据集不预作限制
- 功能强化： get_lagtime_msd, get_lagtime_rmsd 自动从数据文件中读取timestep（以前必须手动指定）
- 细节修改： 优化部分提示语句

### 1.0.1

- BUG修复： to_file绑定filename参数，避免老版本pymatgen的兼容性问题
- BUG修复： average_along_axis的task参数改成大小写敏感，避免rhoBound任务类型解析错误
- 功能强化： 将文件存入不存在的目录前，先创建（支持相对路径）
- 功能强化： write_VESTA和average_along_axis增加subtype参数，指定TotalLocalPotential数据

### 1.0.0

- BUG修复： 文件开头增加utf8编码声明
- 功能强化： 电荷密度差分支持更多组分（不限二元）
- 重要变更： io.utils的getZPE、getTSads、getTSgas函数，增加参数用于将计算结果存入文件
- 重要变更： io.write.write_VESTA() data_type参数可选值从boundcharge改成rhoBound，且大小写敏感，从而保持与DS-PAW输出文件名相同

### 0.9.9

- BUG修复： 修复新版numpy不支持混用array和list生成数组的问题
- BUG修复： 修复从json文件读能带时zero_to_efermi不生效的问题
- 新增功能： build_Structures_from_datafile模块支持读取 neb.h5 和 phonon.h5 文件
- 重要变更： 移除io模块中冗余的 _json.py （相关功能已整合进其他模块中并有所加强）
- 重要变更： 删除 setup.py 中不需要的 joblib 依赖库

### 0.9.8

- BUG修复： to_file 和 build_Structures_from_datafile 接口统一
- BUG修复： io.write模块涉及的保存文件操作，当目标路径上层文件夹不存在时将自动创建
- BUG修复： io.read.get_band_data的zero_to_efermi参数设置为True时，数据的处理逻辑
- BUG修复： io.read.get_sinfo读取relax.json不再因FixLattice而报错
- 新增选项： nebtools的summary函数，新增show_converge用于控制是否显示收敛图，outdir用于指定收敛图的路径
- 新增功能： 写文件涉及的操作，支持传入路径，而不单是文件名
- 新增功能： nebtools的restart函数支持在Windows机器上操作，不必在旧NEB路径执行，备份路径可随意指定
- 新增功能： nebtools的get_neb_subfolder函数新增return_abs参数，用于返回子文件夹的绝对路径
- 重要变更： nebtools的restart函数删除inputin参数，采用压缩较快的zip方法，将生成zip压缩包而不是tar.xz
- 重要变更： io.read.get_band_data的zero_to_fermi参数改名zero_to_efermi

### 0.9.7

- BUG修复： get_rdf 元素对自己计算RDF时的索引
- 新增选项：to_file 增加 si 参数，支持读入单个structure以及Structure列表

### 0.9.6

- BUG修复： pymatgen支持的几类结构文件的读取接口

### 0.9.5

- 重要变更： get_band_data 的 shift_efermi 参数改名为 zero_to_fermi

### 0.9.4

- 新增功能： get_band_data 增加 shift_efermi 参数
- BUG修复： 电荷密度差分函数移除 numpy 多维数组的 shape 参数
- BUG修复： Fe_1 -> Fe+, Fe_2 -> Fe2+ 用于能带、态密度绘图

### 0.9.3

- 新增功能： 接入pymatgen支持的几类结构文件的读写操作
- 新增功能： 支持通过 `dspawpy.__version__` 查看版本号
- 重要变更： write_xyz_traj, write_dump_traj 并入 to_file 函数
- 细节优化： 大幅提高RDF计算效率

### 0.9.2

- 新增功能： 支持从as文件中解析磁矩和FIX信息
- 新增功能： 从h5/json文件中读取数据时支持指定读取的离子步（从1开始）

### 0.9.1

- 重要变更： 精简合并多个函数，统一调用方法
- 新增功能： 支持合并多个xyz和dump文件
- 细节优化： 读取h5或json文件后若无错误，不再打印空行
- 细节优化： 耗时的RDF计算显示进度百分比

### 0.9.0

- 重要变更： 一些函数合并、所在模块迁移，请确认版本
- 新增功能： 支持读取含多离子步计算结果的h5/json文件中的磁矩信息
- BUG修复： get_band_data 函数指定efermi不生效

### 0.8.9

- BUG修复： d_band 脚本运行错误

### 0.8.8

- 新增功能： 支持读取正在进行中的NEB信息，生成movie轨迹文件（可用DS打开观察）
- 新增功能： 支持NEB转XYZ轨迹文件（可用OVITO打开观察）
- 新增功能： plot_aimd 支持读取多个h5文件画在同一张图中
- BUG修复： 电荷差分处理json文件报错
- BUG修复： 极化曲线标记的数值错误
- BUG修复： neb_movie_*.json 中反应坐标重复累加错误

### 0.8.7

- 代码重构，大幅修改数据结构，加速处理过程
- 支持读取h5格式的输出文件
- 新增AIMD, NEB等部分常用功能

### 0.3.0

- 对应2021A版本DS-PAW，辅助处理一些常见数据文件
