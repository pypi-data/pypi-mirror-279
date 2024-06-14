menus = {
    "CN": {
        0: """
======================================
|  1: update更新                     
|  2: structure结构转化              
|  3: volumetricData数据处理         
|  4: band能带数据处理               
|  5: dos态密度数据处理              
|  6: bandDos能带和态密度共同显示    
|  7: optical光学性质数据处理        
|  8: neb过渡态计算数据处理          
|  9: phonon声子计算数据处理         
|  10: aimd分子动力学模拟数据处理    
|  11: Polarization铁电极化数据处理  
|  12: ZPE零点振动能数据处理         
|  13: TS的热校正能                  
|                                    
|  q: 退出                           
======================================
--> 输入数字后回车选择功能：""",
        3: """
=== 3 volumetricData数据处理 ===

1: volumetricData可视化
2: 差分volumetricData可视化
3: volumetricData面平均

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        4: """
=== 4 band能带数据处理 ===

1: 普通能带
2: 将能带投影到每一种元素分别作图，数据点大小表示该元素对该轨道的贡献
3: 能带投影到不同元素的不同轨道
4: 将能带投影到不同原子的不同轨道
5: 能带反折叠处理
6. band-compare能带对比图处理

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        5: """
=== 5 dos态密度数据处理 ===

1: 总的态密度
2: 将态密度投影到不同的轨道上
3: 将态密度投影到不同的元素上
4: 将态密度投影到不同原子的不同轨道上
5: 将态密度投影到不同原子的分裂d轨道(t2g, eg)上
6: d-带中心分析

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        6: """
=== 6 bandDos能带和态密度共同显示 ===

1: 将能带和态密度显示在一张图上
2: 将能带和投影态密度显示在一张图上

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        8: """
=== 8 neb过渡态计算数据处理 ===

1: 输入文件之生成中间构型
2: 绘制能垒图
3: 过渡态计算概览
4: NEB链可视化
5: 计算构型间距
6: neb续算

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        9: """
=== 9 phonon声子计算数据处理 ===

1: 声子能带数据处理
2: 声子态密度数据处理
3: 声子热力学数据处理

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        10: """
=== 10 aimd分子动力学模拟数据处理 ===

1: 轨迹文件转换格式为.xyz或.dump
2: 动力学过程中能量、温度等变化曲线
3: 均方位移（MSD）
4. 均方根偏差（RMSD）
5. 径向分布函数（RDF）

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        13: """
=== 13 TS的热校正能 ===

1: 吸附质
2: 理想气体

0: 返回主菜单
--> 输入数字后回车选择功能：""",
    },
    "EN": {
        0: """
====================================
|  1: dspawpy upgrading
|  2: structure file transforming
|  3: volumetric data processing
|  4: band plotting
|  5: dos plotting  
|  6: bandDos aligned plotting
|  7: optical data processing 
|  8: neb pre&post processing 
|  9: phonon data processing 
|  10: aimd data processing 
|  11: polarization data processing 
|  12: ZPE correction 
|  13: entropy correction
|  
|  q: quit
====================================

--> enter a number and press 'Enter' to select corresponding action: """,
        3: """
=== 3 volumetric data processing ===

1: volumetricData visualization 
2: volumetricData difference visualization 
3: planer averaged volumetricData 

0: return to main menu 
--> enter a number and press 'Enter' to select corresponding action: """,
        4: """
=== 4 band plotting ===

1: regular band plotting 
2: element projected band plotting (contributions are represented by point size)
3: element's orbital projected band plotting (contributions are represented by point size)
4: atom's orbital projected band plotting (contributions are represented by point size)
5: band unfolding plotting 
6. band-compare plotting
  
0: return to main menu 
--> enter a number and press 'Enter' to select corresponding action: """,
        5: """
=== 5 dos plotting ===

1: total dos plotting 
2: orbital projected dos plotting 
3: element projected dos plotting 
4: atom's orbital projected dos plotting 
5: atom's split d orbital (t2g, eg) projected dos plotting 
6: d-band center analysis
  
0: return to main menu 
--> enter a number and press 'Enter' to select corresponding action: """,
        6: """
=== 6 bandDos aligned plotting ===

1: regular band and total dos aligned plotting 
2: regular band and projected dos aligned plotting 

0: return to main menu 
--> enter a number and press 'Enter' to select corresponding action: """,
        8: """
=== 8 neb calculation pre&post processing ===

1: input structure file preparing : structure interpolation 
2: barrier plotting 
3: NEB calculation inspecting
4: NEB movie
5: root mean square displacement between structures calculating 
6: neb restarting 

0: return to main menu 
--> enter a number and press 'Enter' to select corresponding action: """,
        9: """
=== 9 phonon calculation post processing ===

1: phonon band plotting
2: phonon dos plotting
3: thermo data from phonon

0: return to main menu 
--> enter a number and press 'Enter' to select corresponding action: """,
        10: """
=== 10 aimd calculation post processing ===

1: trajectory file transforming
2: calculation monitoring: energy, temperature, volume...
3: MSD deriving
4. RMSD deriving
5. RDF deriving

0: return to main menu 
--> enter a number and press 'Enter' to select corresponding action: """,
        13: """
=== 13 entropy thermal correction ===

1: adsorption entropy correction
2: ideal gas entropy correction

0: return to main menu 
--> enter a number and press 'Enter' to select corresponding action: """,
    },
}

logo = {
    "CN": r"""
********这是dspawpy命令行交互小工具，预祝您使用愉快********
    ( )
   _| |  ___  _ _      _ _  _   _   _  _ _    _   _
 /'_` |/',__)( '_`\  /'_` )( ) ( ) ( )( '_`\ ( ) ( )
( (_| |\__, \| (_) )( (_| || \_/ \_/ || (_) )| (_) |
 \__,_)(____/| ,__/'`\__,_) \___x___/ | ,__/  \__, |
             | |                      | |    ( )_| |
             (_)                      (_)     \___/
""",
    "EN": r"""
This is a command line interactive tool based on dspawpy, enjoy
    ( )
   _| |  ___  _ _      _ _  _   _   _  _ _    _   _
 /'_` |/',__)( '_`\  /'_` )( ) ( ) ( )( '_`\ ( ) ( )
( (_| |\__, \| (_) )( (_| || \_/ \_/ || (_) )| (_) |
`\__,_)(____/| ,__/'`\__,_)`\___x___/'| ,__/'`\__, |
             | |                      | |    ( )_| |
             (_)                      (_)    `\___/'
""",
}

Dupdate = {
    "CN": [
        "更新dspawpy将执行",
        "执行成功",
        "请重新运行程序，使安装生效",
        "执行失败",
    ],
    "EN": [
        "To update dspawpy, will run",
        "Success",
        "Please re-run this cli to use new version",
        "Failed",
    ],
}


Dcheck = {
    "CN": [
        "正在联网检查dspawpy版本... 使用 -s True 启动可跳过",
        "无法导入 requests 库",
        "requests联网检查dspawpy版本超时",
        "requests联网检查dspawpy版本时出现异常: ",
        "联网检查dspawpy版本失败: ",
        "最新版本号 > 当前导入的，可使用功能1升级",
        "最新版本号 = 当前导入的",
        "联网检查失败，请确认网络连接是否正常",
    ],
    "EN": [
        "Checking dspawpy version online... Use -s True to skip",
        "Unable to import requests library",
        "Online check for dspawpy version timed out via requests",
        "Exception occurred while checking dspawpy version online with requests: ",
        "Failed to check dspawpy version online: ",
        "Latest version number > current imported one, feature 1 can be used to upgrade",
        "Latest version number = current imported one",
        "Online check failed, please check if the network connection is normal",
    ],
}


Dio = {
    "CN": {
        "ins": "输入结构文件，括号中星号代表任意字符(*.h5/*.json/*.pdb/*.as/*.hzw/*.cif/*POSCAR*/*CHGCAR*/vasprun*.xml*/...): ",
        "outs": "输出结构文件，括号中星号代表任意字符(*.json/*.pdb/*.as/*.hzw/*.xyz/*.dump/*.cif*/*.mcif*/*POSCAR*/...): ",
        "tcharge": "体系总电荷密度(例如rho.h5/json): ",
        "pcharge": "体系各组分电荷密度(例如rho.h5/json直接回车表示跳过): ",
        "inits": "初态构型(例如initial_structure.as): ",
        "fins": "末态构型(例如final_structure.as): ",
        "band": "电子能带(例如band.h5/json): ",
        "pband": "电子投影能带(例如pband.h5/json): ",
        "phband": "声子能带(例如phonon.h5/json): ",
        "wband": "瓦尼尔能带(例如wannier.h5/json): ",
        "dos": "电子态密度(例如dos.h5/json): ",
        "pdos": "电子投影态密度(例如pdos.h5/json): ",
        "phdos": "声子投影态密度(例如phonon.h5/json): ",
        "optical": "光学性质数据(例如optical.h5/json): ",
        "sysjson": "体系数据(例如sys.json): ",
        "polarization": "铁电极化: ",
        "neb": "过渡态数据文件(例如neb.h5/json)或整个过渡态计算文件夹: ",
        "txt": "文本文件: ",
        "inf": "文件路径（包含文件名和后缀，直接回车表示跳过）: ",
        "outf": "文件输出路径（包含文件名和后缀，直接回车表示跳过）: ",
        "ind": "文件夹路径（直接回车表示当前路径）: ",
        "outd": "文件夹输出路径（直接回车表示当前路径）: ",
        "figure": "图片保存路径（包含文件名和后缀）: ",
        "nebdir": "过渡态文件夹: ",
        "import": "成功导入依赖库，dspawpy现在开始处理数据...",
    },
    "EN": {
        "ins": "Input structure file, asterisk in parentheses stands for any character(*.h5/*.json/*.pdb/*.as/*.hzw/*.cif/*POSCAR*/*CHGCAR*/vasprun*.xml*/...): ",
        "outs": "Output structure file, asterisk in parentheses stands for any character(*.json/*.pdb/*.as/*.hzw/*.xyz/*.dump/*.cif*/*.mcif*/*POSCAR*/...): ",
        "tcharge": "Total charge density (e.g. rho.h5/json): ",
        "pcharge": "Charge density of individuals (e.g. rho.h5/json): ",
        "inits": "Initial structure (e.g. initial_structure.as): ",
        "fins": "Final structure (e.g. final_structure.as): ",
        "band": "Electronic band (e.g. band.h5/json): ",
        "pband": "Projected electronic band (e.g. pband.h5/json): ",
        "phband": "Phonon band (e.g. phonon.h5/json): ",
        "wband": "Wannier band (e.g. wannier.h5/json): ",
        "dos": "Electronic density of states (e.g. dos.h5/json): ",
        "pdos": "Projected electronic density of states (e.g. pdos.h5/json): ",
        "phdos": "Projected phonon density of states (e.g. phonon.h5/json): ",
        "optical": "Optical properties data (e.g. optical.h5/json): ",
        "sysjson": "System data (e.g. sys.json): ",
        "polarization": "polarization: ",
        "neb": "NEB data file (e.g. neb.h5/json) or whole neb folder: ",
        "txt": ".txt file: ",
        "inf": "File path (including file name and suffix, press Enter to skip): ",
        "outf": "File output path (including file name and suffix, press Enter to skip): ",
        "ind": "Folder path (press Enter to use current path): ",
        "outd": "Folder output path (press Enter to use current path): ",
        "figure": "Figure (including file name and suffix): ",
        "nebdir": "NEB folder: ",
        "import": "Successfully imported dependencies, dspawpy is now processing data...",
    },
}


Dresponse = {
    "CN": [
        "没有以空格分隔，请重试",
        "参数长度不为2",
        "不全是数字，请重试",
        "未检测到数据集，请检查文件",
        "仅支持h5和json格式",
        "可使用VESTA软件打开",
        "未能成功读取能带数据！请检查数据文件",
        "IDPP插值失败，请检查构型是否合理",
        "已成功自动转为线性插值",
        "已将插值后的构型保存到",
        "插值方法默认使用pchip，如果要用其他方法，请参考官网的示例脚本",
        "版本过老",
        "对于多个文件，必须手动指定timestep",
        "******** 感谢使用dspawpy ********",
        "上一个任务已结束，是否开始下一个任务？(y/n): ",
    ],
    "EN": [
        "Not separated by space, please retry",
        "Parameter length is not 2",
        "Not all are numbers, please retry",
        "No data set detected, please check file",
        "Only support h5 and json format",
        "Can be opened by VESTA software",
        "Failed to read wannier band data! Please check the data file",
        "IDPP interpolation failed, please check if the structure is reasonable",
        "Successfully converted to linear interpolation",
        "The interpolated configuration has been saved to",
        "The interpolation method defaults to pchip, if you want to use other methods, please refer to the example script on the official website",
        "Version is too old",
        "For multiple datafiles, you must manually specify the timestep. It will default to 1.0fs.",
        "******** thanks for using dspawpy ********",
        "The previous task was finished, do you want to start the next task? (y/n): ",
    ],
}

# 请选择
Dselect = {
    "CN": [
        "请选择下列数据集其中之一（按Tab键查看可选项，直接回车表示选择结束）: ",
        "请选择沿着哪个或哪些轴平均（按Tab键查看可选项，直接回车表示选择结束）: ",
        "请选择输出格式（按Tab键查看可选项，直接回车表示选择结束）: ",
        "请选择是否平移费米能级到0 (y/n): ",
        "请选择一种元素（按Tab键查看可选项，直接回车表示选择结束）: ",
        "请选择该元素的原子轨道（按Tab键查看可选项，用空格分隔）: ",
        ">> 已选的轨道元素字典: ",
        "请选择一个原子序号（按Tab键查看可选项，直接回车表示选择结束）: ",
        "请选择该原子的多个原子轨道（注意，pymatgen暂不支持单个轨道；按Tab键查看可选项，用空格分隔）: ",
        "请选择原子或元素（按Tab键查看可选项，以空格隔开，直接回车表示选择结束）: ",
        "请选择插值方法（按Tab键查看可选项，直接回车表示选择结束）: ",
        "请选择是否将插值链另外保存成xyz或者json文件（用于可视化）？ (y/n): ",
        "请选择第几个离子步（从1开始计数，-1表示最新构型）: ",
        "请选择计算MSD的类型（按Tab键查看可选项，直接回车等同于'xyz'，表示计算所有分量）: ",
        "请选择一个中心元素（按Tab键查看可选项，直接回车表示选择结束）: ",
        "请选择一个对象元素（按Tab键查看可选项，直接回车表示选择结束）: ",
        "请选择一个物理量（按Tab键查看可选项，直接回车表示全选）",
        "请选择一个轴（按Tab键查看可选项，直接回车表示全选）",
    ],
    "EN": [
        "Please select one of the following data sets: ",
        "Please select average along which axis or axes: ",
        "Please select output format: ",
        "Please select whether to shift the Fermi level to 0 (y/n): ",
        "Please select one element (press Enter to finish): ",
        "Please select atomic orbitals of this element (separated by space): ",
        "Please select orbital element dictionary: : ",
        "Please select an atomic index (press Enter to finish): ",
        "Please select orbital of this atom (separated by space): ",
        "Please select atom or element (separated by space, press Enter to finish): ",
        "Please select interpolation method: ",
        "Please select whether to save the interpolated chain as a separate xyz or json file for visualization? (y/n): ",
        "Please select which ionic step (counting from 1, -1 indicates the latest configuration): ",
        "Please select type of MSD calculation, optional xyz, xy, xz, yz, x, y, z, (press Enter is equivalent to 'xyz', indicating calculation of all components): ",
        "Please select a center element: ",
        "Please select an object element: ",
        "Please select a physical quantity: ",
        "Please select an axis: ",
    ],
}

# 请输入
Dparameter = {
    "CN": [
        "时间步长（fs），直接回车将尝试从文件中自动读取，失败则此数值将设为1.0: ",
        "最小半径, 单位埃（默认0）: ",
        "最大半径, 单位埃（默认10）: ",
        "格点数（默认101）: ",
        "sigma值（用于一维高斯函数平滑处理，默认0，不处理）: ",
        "数据点绘图时重复次数（默认2）: ",
        "温度(K, 默认298.15): ",
        "压强(Pa, 默认101325.0): ",
        "初末态之间插入几个构型: ",
        "x轴范围（先小后大，以空格分隔，直接回车可跳过设置）: ",
        "y轴范围（先小后大，以空格分隔，直接回车可跳过设置）: ",
        "备份文件夹: ",
        "第1个构型路径（包含文件名）: ",
        "第2个构型路径（包含文件名）: ",
    ],
    "EN": [
        "Time step (fs), press Enter to try to read automatically from the file, if failed, this value will be set to 1.0: ",
        "Minimum radius, in Å (default 0): ",
        "Maximum radius, in Å (default 10): ",
        "Number of grid points (default 101): ",
        "Sigma value (used for one-dimensional Gaussian function smoothing, default 0, no processing): ",
        "Y-axis lower and upper limits, separated by space (default not specified): ",
        "Number of repetitions when plotting data points (default 2): ",
        "Temperature (K, default 298.15): ",
        "Pressure (Pa, default 101325.0): ",
        "Number of configurations inserted between initial and final states: ",
        "X-axis range (small to large, separated by space, press Enter to skip setting): ",
        "Y-axis range (small to large, separated by space, press Enter to skip setting): ",
        "1st structure path: ",
        "2nd structure path: ",
    ],
}

if __name__ == "__main__":
    i = 0
    for item in [menus, Dupdate, Dcheck, Dio, Dresponse, Dselect, Dparameter]:
        i += 1
        cn_length = len(item["CN"])
        en_length = len(item["EN"])

        if cn_length == en_length:
            print("No missing translations.")
        else:
            print(i)
            print(
                f"Missing translations. CN has {cn_length} items, EN has {en_length} items."
            )
