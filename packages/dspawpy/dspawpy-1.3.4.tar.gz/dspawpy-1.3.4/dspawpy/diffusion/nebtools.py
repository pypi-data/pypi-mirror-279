# -*- coding: utf-8 -*-
from typing import Optional

from loguru import logger


@logger.catch
def _zip_folder(folder_path: str, output_path: str):
    import os

    absdir1 = os.path.abspath(folder_path)
    absdir2 = os.path.abspath(output_path)
    import zipfile

    with zipfile.ZipFile(absdir2, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(absdir1):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, absdir1))


@logger.catch
def get_distance(spo1, spo2, lat1, lat2):
    r"""根据两个结构的分数坐标和晶胞计算距离

    Parameters
    ----------
    spo1 : np.ndarray
        分数坐标列表1
    spo2 : np.ndarray
        分数坐标列表2
    lat1 : np.ndarray
        晶胞1
    lat2 : np.ndarray
        晶胞2

    Returns
    -------
    float
        距离

    Examples
    --------

    先读取结构信息

    >>> from dspawpy.io.structure import read
    >>> s1 = read('dspawpy_proj/dspawpy_tests/inputs/2.15/01/structure01.as')[0]
    >>> s2 = read('dspawpy_proj/dspawpy_tests/inputs/2.15/02/structure02.as')[0]

    计算两个构型的距离

    >>> from dspawpy.diffusion.nebtools import get_distance
    >>> dist = get_distance(s1.frac_coords, s2.frac_coords, s1.lattice.matrix, s2.lattice.matrix)
    >>> print('两个构型的距离为：', dist, 'Angstrom')
    两个构型的距离为： 0.476972808803491 Angstrom
    """
    import numpy as np

    diff_spo = spo1 - spo2  # 分数坐标差
    avglatv = 0.5 * (lat1 + lat2)  # 平均晶格矢量
    pbc_diff_spo = set_pbc(diff_spo)  # 笛卡尔坐标差
    # 分数坐标点乘平均晶胞，转回笛卡尔坐标
    pbc_diff_pos = np.dot(pbc_diff_spo, avglatv)  # 笛卡尔坐标差
    distance = np.sqrt(np.sum(pbc_diff_pos**2))

    return distance


@logger.catch
def get_neb_subfolders(directory: str = ".", return_abs: bool = False):
    r"""将directory路径下的子文件夹名称列表按照数字大小排序

    仅保留形如00，01数字类型的NEB子文件夹路径

    Parameters
    ----------
    subfolders : list
        子文件夹名称列表
    return_abs : bool, optional
        是否返回绝对路径, 默认否

    Returns
    -------
    subfolders : list
        排序后的子文件夹名称列表

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import get_neb_subfolders
    >>> directory = 'dspawpy_proj/dspawpy_tests/inputs/2.15'
    >>> get_neb_subfolders(directory)
    ['00', '01', '02', '03', '04']
    """
    import os

    absdir = os.path.abspath(directory)
    raw_subfolders = next(os.walk(absdir))[1]
    subfolders = []
    for subfolder in raw_subfolders:
        try:
            assert 0 <= int(subfolder) < 100
            subfolders.append(subfolder)
        except Exception:
            pass
    subfolders.sort()  # 从小到大排序
    if return_abs:
        subfolders = [
            os.path.abspath(os.path.join(absdir, subfolder)) for subfolder in subfolders
        ]
    return subfolders


@logger.catch
def plot_barrier(
    datafile: str = "neb.h5",
    directory: Optional[str] = None,
    ri: Optional[float] = None,
    rf: Optional[float] = None,
    ei: Optional[float] = None,
    ef: Optional[float] = None,
    method: str = "PchipInterpolator",
    figname: Optional[str] = "neb_barrier.png",
    show: bool = True,
    raw: bool = False,
    verbose: bool = False,
    **kwargs,
):
    r"""调用 scipy.interpolate 插值算法，拟合NEB能垒并绘图

    Parameters
    ----------
    datafile: str
        neb.h5或neb.json文件路径
    directory : str
        NEB计算路径
    ri : float
        初态反应坐标
    rf : float
        末态反应坐标
    ei : float
        初态自洽能量
    ef : float
        末态自洽能量
    method : str, optional
        插值算法, 默认'PchipInterpolator'
    figname : str, optional
        能垒图名称, 默认'neb_barrier.png'
    show : bool, optional
        是否展示交互界面, 默认True
    raw : bool, optional
        是否返回绘图数据到csv

    Raises
    ------
    ImportError
        指定了scipy.interpolate中不存在的插值算法
    ValueError
        传递给插值算法的参数不符合该算法要求

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import plot_barrier
    >>> import matplotlib.pyplot as plt

    对比不同插值算法

    >>> plot_barrier(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', method='interp1d', kind=2, figname=None, show=False)
    >>> plot_barrier(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', method='interp1d', kind=3, figname=None, show=False)
    >>> plot_barrier(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', method='CubicSpline', figname=None, show=False)
    >>> plot_barrier(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', method='pchip', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/barrier_comparison.png', show=False) # doctest: +ELLIPSIS
    ==> .../doctest/barrier_comparison.png

    尝试读取neb.h5文件或neb.json文件

    >>> plot_barrier(datafile='dspawpy_proj/dspawpy_tests/inputs/2.15/neb.h5', method='pchip', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/barrier_h5.png', show=False) # doctest: +ELLIPSIS
    ==> .../doctest/barrier_h5.png
    >>> plot_barrier(datafile='dspawpy_proj/dspawpy_tests/inputs/2.15/neb.json', method='pchip', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/barrier_json.png', show=False) # doctest: +ELLIPSIS
    ==> .../doctest/barrier_json.png
    """
    import os

    import numpy as np

    if directory is not None:
        # read data
        subfolders, resort_mfs, rcs, ens, dEs = _getef(os.path.abspath(directory))

    elif datafile:
        from dspawpy.io.utils import get_absfile

        absfile = get_absfile(
            datafile, task="neb", verbose=verbose
        )  # -> return either .h5 or .json
        if absfile.endswith(".h5"):
            from dspawpy.io.read import load_h5

            neb = load_h5(absfile)
            if "/BarrierInfo/ReactionCoordinate" in neb.keys():
                reaction_coordinate = neb["/BarrierInfo/ReactionCoordinate"]
                energy = neb["/BarrierInfo/TotalEnergy"]
            else:  # old version
                reaction_coordinate = neb["/Distance/ReactionCoordinate"]
                energy = neb["/Energy/TotalEnergy"]
        elif absfile.endswith(".json"):
            with open(absfile, "r") as fin:
                from json import load

                neb = load(fin)
            if "BarrierInfo" in neb.keys():
                reaction_coordinate = neb["BarrierInfo"]["ReactionCoordinate"]
                energy = neb["BarrierInfo"]["TotalEnergy"]
            else:  # old version
                reaction_coordinate = neb["Distance"]["ReactionCoordinate"]
                energy = neb["Energy"]["TotalEnergy"]
        else:
            raise ValueError("only h5 and json file are supported")

        x = reaction_coordinate  # 从neb.h5/json 读取的不需要累加

        y = [x - energy[0] for x in energy]
        # initial and final info
        if ri is not None:  # add initial reaction coordinate
            x.insert(0, ri)
        if rf is not None:  # add final reaction coordinate
            x.append(rf)

        if ei is not None:  # add initial energy
            y.insert(0, ei)
        if ef is not None:  # add final energy
            y.append(ef)

        rcs = np.array(x)
        dEs = np.array(y)

    else:
        raise ValueError("Please specify directory or datafile!")

    # import scipy interpolater
    try:
        interpolate_method = getattr(
            __import__("scipy.interpolate", fromlist=[method]), method
        )
    except Exception:
        raise ImportError(f"No scipy.interpolate.{method} method！")
    # call the interpolater to interpolate with given kwargs
    try:
        inter_f = interpolate_method(rcs, dEs, **kwargs)
    except Exception:
        raise ValueError(f"Please check whether {kwargs} is valid for {method}！")

    xnew = np.linspace(rcs[0], rcs[-1], 100)
    ynew = inter_f(xnew)

    if raw:
        import polars as pl

        pl.DataFrame({"x_raw": rcs, "y_raw": dEs}).write_csv(
            "raw_xy.csv",
        )
        pl.DataFrame({"x_interpolated": xnew, "y_interpolated": ynew}).write_csv(
            "raw_interpolated_xy.csv",
        )

    # plot
    import matplotlib.pyplot as plt  # noqa: E402

    if kwargs:
        plt.plot(xnew, ynew, label=method + str(kwargs))
    else:
        plt.plot(xnew, ynew, label=method)
    plt.scatter(rcs, dEs, c="r")
    plt.xlabel("Reaction Coordinate (Å)")
    plt.ylabel("Energy (eV)")
    plt.legend()

    plt.tight_layout()
    # save and show
    if figname:
        absfig = os.path.abspath(figname)
        os.makedirs(os.path.dirname(absfig), exist_ok=True)
        plt.savefig(absfig, dpi=300)
        print(f"==> {absfig}")
    if show:
        plt.show()


@logger.catch
def plot_neb_converge(
    neb_dir: str,
    image_key: str = "01",
    show: bool = True,
    figname: str = "neb_conv.png",
    raw=False,
    verbose: bool = False,
):
    """指定NEB计算路径，绘制NEB收敛过程图

    Parameters
    ----------
    neb_dir : str
        neb.h5 / neb.json 文件路径或者包含 neb.h5 / neb.json 文件的文件夹路径
    image_key : str
        第几个构型，默认 "01"
    show : bool
        是否交互绘图
    image_name : str
        NEB收敛图名称，默认 "neb_conv.png"
    raw : bool
        是否输出绘图数据到csv文件

    Returns
    -------
    ax1, ax2 : matplotlib.axes.Axes
        两个子图的Axes对象

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import plot_neb_converge
    >>> result = plot_neb_converge(neb_dir='dspawpy_proj/dspawpy_tests/inputs/2.15', image_key='01', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/neb_converge1.png',show=False) # doctest: +ELLIPSIS
    ==> ...dspawpy_proj/dspawpy_tests/outputs/doctest/neb_converge1.png
    >>> result = plot_neb_converge(neb_dir='dspawpy_proj/dspawpy_tests/inputs/2.15/neb.h5', image_key='02', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/neb_converge2.png',show=False) # doctest: +ELLIPSIS
    ==> ...dspawpy_proj/dspawpy_tests/outputs/doctest/neb_converge2.png
    >>> result = plot_neb_converge(neb_dir='dspawpy_proj/dspawpy_tests/inputs/2.15/neb.json', image_key='03', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/neb_converge3.png',show=False, raw=True) # doctest: +ELLIPSIS
    ==> ...dspawpy_proj/dspawpy_tests/outputs/doctest/neb_converge3.png
    """
    import os

    import numpy as np

    from dspawpy.io.utils import get_absfile

    absfile = get_absfile(neb_dir, "neb", verbose=verbose)
    if absfile.endswith("h5"):
        import h5py

        neb_total = h5py.File(absfile)
        # new output (>=2022B)
        if "/LoopInfo/01/MaxForce" in neb_total.keys():
            maxforce = np.array(neb_total.get("/LoopInfo/" + image_key + "/MaxForce"))
        else:  # old output
            maxforce = np.array(neb_total.get("/Iteration/" + image_key + "/MaxForce"))

        if "/LoopInfo/01/TotalEnergy" in neb_total.keys():  # new output (>=2022B)
            total_energy = np.array(
                neb_total.get("/LoopInfo/" + image_key + "/TotalEnergy")
            )
        else:  # old output
            total_energy = np.array(
                neb_total.get("/Iteration/" + image_key + "/TotalEnergy")
            )

    elif absfile.endswith("json"):
        with open(absfile, "r") as fin:
            from json import load

            neb_total = load(fin)
        if "LoopInfo" in neb_total.keys():
            neb = neb_total["LoopInfo"][image_key]
        else:
            neb = neb_total["Iteration"][image_key]
        maxforce = []
        total_energy = []
        for n in neb:
            maxforce.append(n["MaxForce"])
            total_energy.append(n["TotalEnergy"])

        maxforce = np.array(maxforce)
        total_energy = np.array(total_energy)

    else:
        raise ValueError("Only h5 and json file are supported")

    x = np.arange(len(maxforce))

    force = maxforce
    energy = total_energy

    if raw:
        import polars as pl

        pl.DataFrame({"x": x, "force": force, "energy": energy}).write_csv(
            "neb_conv.csv",
        )

    import matplotlib.pyplot as plt  # noqa: E402

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(x, force, label="Max Force", c="black")
    ax1.set_xlabel("Number of ionic step")
    ax1.set_ylabel("Force (eV/Å)")
    ax2 = ax1.twinx()
    ax2.plot(x, energy, label="Energy", c="r")  # type: ignore
    ax2.set_xlabel("Number of ionic step")
    ax2.set_ylabel("Energy (eV)")
    ax2.ticklabel_format(useOffset=False)  # y轴坐标显示绝对值而不是相对值
    fig.legend(loc=1, bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)

    plt.tight_layout()
    # save and show
    if figname:
        absfig = os.path.abspath(figname)
        os.makedirs(os.path.dirname(absfig), exist_ok=True)
        plt.savefig(absfig, dpi=300)
        print(f"==> {absfig}")
    if show:
        plt.show()

    return ax1, ax2


@logger.catch
def printef(directory: str):
    """打印NEB计算时各构型的能量和受力

    Parameters
    ----------
    directory : str
        NEB计算的目录，默认为当前目录

    Returns
    -------
    打印各构型的能量和受力

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import printef
    >>> printef(directory='dspawpy_proj/dspawpy_tests/inputs/2.15')
    shape: (5, 5)
    ┌────────────┬─────────────┬──────────┬───────────────┬──────────┐
    │ FolderName ┆ Force(eV/Å) ┆ RC(Å)    ┆ Energy(eV)    ┆ E-E0(eV) │
    │ ---        ┆ ---         ┆ ---      ┆ ---           ┆ ---      │
    │ str        ┆ f32         ┆ f32      ┆ f32           ┆ f32      │
    ╞════════════╪═════════════╪══════════╪═══════════════╪══════════╡
    │ 00         ┆ 0.180272    ┆ 0.0      ┆ -39637.097656 ┆ 0.0      │
    │ 01         ┆ 0.026337    ┆ 0.542789 ┆ -39637.019531 ┆ 0.079814 │
    │ 02         ┆ 0.024798    ┆ 1.0868   ┆ -39636.878906 ┆ 0.218265 │
    │ 03         ┆ 0.234429    ┆ 1.588367 ┆ -39637.0      ┆ 0.100043 │
    │ 04         ┆ 0.014094    ┆ 2.089212 ┆ -39637.089844 ┆ 0.008414 │
    └────────────┴─────────────┴──────────┴───────────────┴──────────┘
    """
    import numpy as np

    from dspawpy.diffusion.nebtools import _getef

    arr = np.array(_getef(directory))
    data = {
        "FolderName": arr[0],
        "Force(eV/Å)": arr[1],
        "RC(Å)": arr[2],
        "Energy(eV)": arr[3],
        "E-E0(eV)": arr[4],
    }
    import polars as pl

    _df = pl.DataFrame(data)
    col_names = [col_name for col_name in _df.columns if col_name != "FolderName"]
    df = _df.with_columns(pl.col(col_names).cast(pl.Float32, strict=False))
    print(df)


@logger.catch
def restart(directory: str = ".", output: str = "bakfile"):
    """将旧NEB任务归档压缩，并在原路径下准备续算

    Parameters
    ----------
    directory : str
        旧NEB任务所在路径，默认当前路径
    output : str
        备份文件夹路径，默认将在当前路径新建一个bakfile文件夹用于备份；
        也可以任意指定一个路径，但不能与当前路径相同

    Examples
    ----------
    >>> from dspawpy.diffusion.nebtools import restart
    >>> from shutil import copytree
    >>> copytree('dspawpy_proj/dspawpy_tests/inputs/2.15', 'dspawpy_proj/dspawpy_tests/outputs/doctest/neb4bk2', dirs_exist_ok=True)
    'dspawpy_proj/dspawpy_tests/outputs/doctest/neb4bk2'
    >>> restart(directory='dspawpy_proj/dspawpy_tests/outputs/doctest/neb4bk2', output='dspawpy_proj/dspawpy_tests/outputs/doctest/neb_backup') # doctest: +ELLIPSIS
    ==> ...dspawpy_proj/dspawpy_tests/outputs/doctest/neb_backup

    续算准备工作可能需要较长时间才能完成，请耐心等待
    """
    import os
    import shutil

    absolute_output = os.path.abspath(output)
    absdir = os.path.abspath(directory)

    if os.path.isdir(absolute_output):
        from datetime import datetime

        shutil.move(
            absolute_output,
            absolute_output + "_" + datetime.now().strftime("%Y%m%d%H%M%S"),
        )
        logger.warning(
            f"{absolute_output} already exists, renamed to {absolute_output}_datetime"
        )

    subfolders = get_neb_subfolders(absdir, return_abs=True)  # 获取子文件夹路径
    os.makedirs(absolute_output, exist_ok=True)  # 创建bakfile文件夹
    # 先处理子文件夹00，01...
    for subfolder_old in subfolders:
        folder_index = subfolder_old.split("/")[-1]  # 00，01...
        subfolder_back = os.path.join(absolute_output, folder_index)  # 子文件夹备份到此
        shutil.move(subfolder_old, subfolder_back)
        os.makedirs(subfolder_old, exist_ok=True)  # 原文件夹清空了

        latestStructureFile = f"{subfolder_back}/latestStructure{folder_index}.as"
        structureFile = f"{subfolder_back}/structure{folder_index}.as"

        # 将结构文件复制到原路径下用于续算，有ls则用之，否则用s代替，都没有则报错
        s_in_old = f"{subfolder_old}/structure{folder_index}.as"
        if os.path.isfile(latestStructureFile):
            shutil.copy(latestStructureFile, s_in_old)
        elif os.path.isfile(structureFile):
            shutil.copy(structureFile, s_in_old)
        else:
            raise FileNotFoundError(f"{latestStructureFile}和{structureFile}都不存在！")

        # 暂时放到备份主路径下，如果都没有，前面就已经报错了
        ls_bk = os.path.join(absdir, f"latestStructure{folder_index}.as")
        s_bk = os.path.join(absdir, f"structure{folder_index}.as")
        if os.path.isfile(latestStructureFile):
            shutil.copy(latestStructureFile, ls_bk)
        if os.path.isfile(structureFile):
            shutil.copy(structureFile, s_bk)

        # 处理备份路径下的子文件夹
        zf = f"{absolute_output}/{folder_index}.zip"
        _zip_folder(subfolder_back, zf)  # 压缩子文件夹
        # 清空备份子文件夹
        for file in os.listdir(subfolder_back):
            os.remove(os.path.join(subfolder_back, file))

        # 将压缩包、结构文件移入
        shutil.move(zf, f"{subfolder_back}/{folder_index}.zip")
        if os.path.isfile(ls_bk) and os.path.isfile(s_bk):
            shutil.move(ls_bk, f"{subfolder_back}/latestStructure{folder_index}.as")
            shutil.move(s_bk, f"{subfolder_back}/structure{folder_index}.as")
        elif os.path.isfile(ls_bk):
            shutil.move(ls_bk, f"{subfolder_back}/latestStructure{folder_index}.as")
        elif os.path.isfile(s_bk):
            shutil.move(s_bk, f"{subfolder_back}/structure{folder_index}.as")
        else:
            raise FileNotFoundError(f"Both {ls_bk} and {s_bk} not found")

    # 再处理老NEB文件夹主目录下的单个文件
    # 备份neb.h5,neb.json和DS-PAW.log
    tmp_dir = os.path.join(absolute_output, "tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    if os.path.isfile(f"{absdir}/neb.h5"):
        shutil.move(f"{absdir}/neb.h5", f"{tmp_dir}/neb.h5")

    if os.path.isfile(f"{absdir}/neb.json"):
        shutil.move(f"{absdir}/neb.json", f"{tmp_dir}/neb.json")

    if len(os.listdir(tmp_dir)) > 0:  # 如果有数据文件
        _zip_folder(tmp_dir, f"{absolute_output}/neb_data.zip")
        for f in os.listdir(tmp_dir):
            os.remove(os.path.join(tmp_dir, f))
        os.removedirs(tmp_dir)

    if os.path.isfile(f"{absdir}/DS-PAW.log"):
        shutil.move(f"{absdir}/DS-PAW.log", f"{absolute_output}/DS-PAW.log")

    print(f"==> {absolute_output}")


@logger.catch
def set_pbc(spo):
    """根据周期性边界条件将分数坐标分量移入 [-0.5, 0.5) 区间

    Parameters
    ----------
    spo : np.ndarray or list
        分数坐标列表

    Returns
    -------
    pbc_spo : np.ndarray
        符合周期性边界条件的分数坐标列表

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import set_pbc
    >>> set_pbc([-0.6, 1.2, 2.3])
    array([0.4, 0.2, 0.3])
    """
    # wrap into [-0.5, 0.5)
    import numpy as np

    pbc_spo = np.mod(np.array(spo) + 0.5, 1.0) - 0.5

    return pbc_spo


@logger.catch
def summary(
    directory: str = ".",
    raw=False,
    show_converge=False,
    outdir: Optional[str] = None,
    **kwargs,
):
    r"""NEB任务完成总结，依次执行以下步骤：

    - 1. 打印各构型受力、反应坐标、能量、与初始构型的能量差
    - 2. 绘制能垒图
    - 3. 绘制并保存结构优化过程的能量和受力收敛过程图

    Parameters
    ----------
    directory : str
        NEB路径, 默认当前路径
    raw : bool
        是否保存绘图数据到csv文件
    show_converge : bool
        是否展示结构优化过程的能量和受力收敛过程图，默认不展示
    outdir : str
        收敛过程图保存路径，默认为directory
    **kwargs : dict
        传递给plot_barrier的参数

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import summary
    >>> directory = 'dspawpy_proj/dspawpy_tests/inputs/2.15' # NEB计算路径，默认当前路径
    >>> summary(directory, show=False, figname='dspawpy_proj/dspawpy_tests/outputs/doctest/neb_barrier.png') # doctest: +ELLIPSIS
    shape: (5, 5)
    ┌────────────┬─────────────┬──────────┬───────────────┬──────────┐
    │ FolderName ┆ Force(eV/Å) ┆ RC(Å)    ┆ Energy(eV)    ┆ E-E0(eV) │
    │ ---        ┆ ---         ┆ ---      ┆ ---           ┆ ---      │
    │ str        ┆ f32         ┆ f32      ┆ f32           ┆ f32      │
    ╞════════════╪═════════════╪══════════╪═══════════════╪══════════╡
    │ 00         ┆ 0.180272    ┆ 0.0      ┆ -39637.097656 ┆ 0.0      │
    │ 01         ┆ 0.026337    ┆ 0.542789 ┆ -39637.019531 ┆ 0.079814 │
    │ 02         ┆ 0.024798    ┆ 1.0868   ┆ -39636.878906 ┆ 0.218265 │
    │ 03         ┆ 0.234429    ┆ 1.588367 ┆ -39637.0      ┆ 0.100043 │
    │ 04         ┆ 0.014094    ┆ 2.089212 ┆ -39637.089844 ┆ 0.008414 │
    └────────────┴─────────────┴──────────┴───────────────┴──────────┘
    ==> .../doctest/neb_barrier.png
    ==> .../doctest/01/converge.png
    ==> .../doctest/02/converge.png
    ==> .../doctest/03/converge.png

    >>> summary(directory, show=False, figname='dspawpy_proj/dspawpy_tests/outputs/doctest/neb_barrier.png', outdir="dspawpy_proj/dspawpy_tests/outputs/doctest/neb_summary") # doctest: +ELLIPSIS
    shape: (5, 5)
    ┌────────────┬─────────────┬──────────┬───────────────┬──────────┐
    │ FolderName ┆ Force(eV/Å) ┆ RC(Å)    ┆ Energy(eV)    ┆ E-E0(eV) │
    │ ---        ┆ ---         ┆ ---      ┆ ---           ┆ ---      │
    │ str        ┆ f32         ┆ f32      ┆ f32           ┆ f32      │
    ╞════════════╪═════════════╪══════════╪═══════════════╪══════════╡
    │ 00         ┆ 0.180272    ┆ 0.0      ┆ -39637.097656 ┆ 0.0      │
    │ 01         ┆ 0.026337    ┆ 0.542789 ┆ -39637.019531 ┆ 0.079814 │
    │ 02         ┆ 0.024798    ┆ 1.0868   ┆ -39636.878906 ┆ 0.218265 │
    │ 03         ┆ 0.234429    ┆ 1.588367 ┆ -39637.0      ┆ 0.100043 │
    │ 04         ┆ 0.014094    ┆ 2.089212 ┆ -39637.089844 ┆ 0.008414 │
    └────────────┴─────────────┴──────────┴───────────────┴──────────┘
    ==> .../doctest/neb_barrier.png
    ==> .../doctest/neb_summary/01/converge.png
    ==> .../doctest/neb_summary/02/converge.png
    ==> .../doctest/neb_summary/03/converge.png

    若inifin=false，用户必须将自洽的scf.h5或system.json放到初末态子文件夹中
    """
    import os

    # 1. 绘制能垒图
    absdir = os.path.abspath(directory)
    printef(absdir)

    # 2. 打印各构型受力、反应坐标、能量、与初始构型的能量差
    import matplotlib.pyplot as plt  # noqa: E402

    plt.clf()  # 清空画布再画图
    plot_barrier(directory=absdir, raw=raw, **kwargs)

    # 3. 绘制并保存结构优化过程的能量和受力收敛过程图到各构型文件夹中
    subfolders = get_neb_subfolders(absdir)
    for subfolder in subfolders[1 : len(subfolders) - 1]:
        if outdir:
            absolute_output = os.path.abspath(outdir)
            os.makedirs(os.path.join(absolute_output, subfolder), exist_ok=True)
            pngfile = f"{absolute_output}/{subfolder}/converge.png"
        else:
            pngfile = (
                f"dspawpy_proj/dspawpy_tests/outputs/doctest/{subfolder}/converge.png"
            )

        plot_neb_converge(
            neb_dir=absdir,
            image_key=subfolder,
            figname=pngfile,
            raw=raw,
            show=show_converge,
        )
    plt.clf()


@logger.catch
def write_movie_json(
    preview: bool = False,
    directory: str = ".",
    step: int = -1,
    dst: Optional[str] = None,
):
    DeprecationWarning("Please use write_json_chain() instead")
    write_json_chain(preview=preview, directory=directory, step=step, dst=dst)


@logger.catch
def write_json_chain(
    preview: bool = False,
    directory: str = ".",
    step: int = -1,
    dst: Optional[str] = None,
    ignorels=False,
):
    r"""NEB计算或者初始插值后，读取信息，保存为 neb_chain*.json 文件

    用 Device Studio 打开该文件可以观察结构等信息

    Parameters
    ----------
    preview : bool
        是否预览模式，默认否
    directory : str
        计算结果所在目录. 默认当前路径
    step: int
        - 离子步编号. 默认-1，读取整个NEB计算过程信息；此时优先级为latestStructure.as > h5 > json
        - 0表示初插结构（未完成离子步）；
        - 1表示第一个离子步，以此类推
    dst : str
        保存路径，默认为directory
    ignorels : bool
        当step=-1时是否忽略latestStructure.as文件，默认否

    Examples
    ----------
    >>> from dspawpy.diffusion.nebtools import write_json_chain

    NEB计算完成后要观察轨迹变化全过程，只需指定NEB计算路径即可

    >>> write_json_chain(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    structure info collected from latestStructure.as
    ==> .../doctest/neb_chain_last.json

    NEB计算完成后要观察第n离子步结构，请设置step为n，注意step从1开始计数

    >>> write_json_chain(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', step=1, dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    ==> .../doctest/neb_chain_1.json

    如果指定的step数超过NEB实际完成的离子步，将会自动修改为最后一步

    >>> write_json_chain(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', step=10, dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    ==> .../doctest/neb_chain_10.json
    >>> write_json_chain(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', step=100, dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    ==> .../doctest/neb_chain_last.json

    另外，如需预览初插结构，请将preview设置为True，并将directory指定为NEB计算主路径

    >>> write_json_chain(preview=True, directory='dspawpy_proj/dspawpy_tests/inputs/2.15', dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    ==> .../doctest/neb_chain_init.json
    """
    import os

    absdir = os.path.abspath(directory)
    if preview:  # preview mode
        raw = get_raw_from_structure(absdir)
    else:
        if step == 0:  # try preview mode to save time
            raw = get_raw_from_structure(absdir)
        elif step == -1:  # 优先级 latestStructure.as > h5 > json
            if ignorels:
                raw = get_raw_from_h5_json(absdir, step)
            else:
                try:  # read ls.as
                    raw = _from_structures(absdir, ls=True)
                    print("structure info collected from latestStructure.as")
                except FileNotFoundError:
                    raw = get_raw_from_h5_json(absdir, step)
        else:
            raw = get_raw_from_h5_json(absdir, step)

    new = []
    assert raw is not None
    if dst is not None:
        abs_dst = os.path.abspath(dst)
        os.makedirs(abs_dst, exist_ok=True)
        new.append(f"{abs_dst}/{raw[0]}")
        for i in range(1, len(raw)):
            new.append(raw[i])
        _dump_neb_chain_json(new)
    else:
        _dump_neb_chain_json(raw)


@logger.catch
def write_xyz(
    preview: bool = False,
    directory: str = ".",
    step: int = -1,
    dst: Optional[str] = None,
):
    DeprecationWarning("Please use write_xyz_chain() instead")
    write_xyz_chain(preview=preview, directory=directory, step=step, dst=dst)


@logger.catch
def get_raw_from_structure(dire: str):
    try:
        raw = _from_structures(dire)
        return raw
    except FileNotFoundError:
        print("No structure file")
    except Exception as e:
        print(e)


@logger.catch
def get_raw_from_h5_json(dire: str, step: int):
    try:
        raw = _from_h5(dire, step)
        return raw
    except FileNotFoundError:
        try:
            raw = _from_json(dire, step)
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)


@logger.catch
def write_xyz_chain(
    preview: bool = False,
    directory: str = ".",
    step: int = -1,
    dst: Optional[str] = None,
    ignorels=False,
):
    r"""
    将NEB结构链条写成xyz轨迹文件用于可视化

    Parameters
    ----------
    preview : bool
        是否预览模式，默认否
    directory : str
        计算结果所在目录. 默认当前路径
    step: int
        - 离子步编号. 默认-1，读取整个NEB计算过程信息；此时优先级为latestStructure.as > h5 > json
        - 0表示初插结构（未完成离子步）；
        - 1表示第一个离子步，以此类推
    dst : str
        保存路径，默认为directory
    ignorels : bool
        当step=-1时是否忽略latestStructure.as文件，默认否

    Examples
    ----------
    >>> from dspawpy.diffusion.nebtools import write_xyz_chain

    NEB计算完成后要观察轨迹变化全过程，只需指定NEB计算路径即可

    >>> write_xyz_chain(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    structure info collected from latestStructure.as
    ==> .../doctest/neb_chain_last.xyz

    NEB计算完成后要观察第n离子步结构，请设置step为n，注意step从1开始计数

    >>> write_xyz_chain(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', step=1, dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    ==> .../doctest/neb_chain_1.xyz

    如果指定的step数超过NEB实际完成的离子步，会被自动修改为最后一步

    >>> write_xyz_chain(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', step=10, dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    ==> .../doctest/neb_chain_10.xyz

    另外，如需预览初插结构，请将preview设置为True，并将directory指定为NEB计算主路径

    >>> write_xyz_chain(preview=True, directory='dspawpy_proj/dspawpy_tests/inputs/2.15', dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    ==> .../doctest/neb_chain_init.xyz
    """
    import os

    absdir = os.path.abspath(directory)
    if preview:  # preview mode, write neb_chain_init.xyz from structure.as
        raw = get_raw_from_structure(absdir)
    else:
        if step == 0:  # try preview mode to save time
            raw = get_raw_from_structure(absdir)
        elif step == -1:  # 优先级 latestStructure.as > h5 > json
            if ignorels:
                raw = get_raw_from_h5_json(absdir, step)
            else:
                try:  # read ls.as
                    raw = _from_structures(absdir, ls=True)
                    print("structure info collected from latestStructure.as")
                except FileNotFoundError:
                    raw = get_raw_from_h5_json(absdir, step)
        else:
            raw = get_raw_from_h5_json(absdir, step)

    new = []
    assert raw is not None
    if dst is not None:
        abs_dst = os.path.abspath(dst)
        os.makedirs(abs_dst, exist_ok=True)
        new.append(f"{abs_dst}/{raw[0]}")
        for i in range(1, len(raw)):
            new.append(raw[i])
        _dump_neb_xyz(new)
    else:
        _dump_neb_xyz(raw)


@logger.catch
def _dump_neb_xyz(raw):
    """根据之前收集到的各数据列表，dump json文件到output"""
    import os

    (
        output,
        subfolders,
        step,
        MaxForces,
        TotalEnergies,
        Poses,  # Nimage x Natom x 3 , read
        Latvs,  # Nimage x 9
        Elems,  # Nimage x Natom
        Fixs,  # Natom x 3
        reactionCoordinates,
        totalEnergies,
        maxForces,
        tangents,
        iDirects,
    ) = raw

    # 写入文件
    xyzfile = output[:-5] + ".xyz"
    absolute_output = os.path.abspath(xyzfile)
    Nstep = len(subfolders)  # 选定离子步，展示构型链
    with open(absolute_output, "w") as f:
        # Nstep
        for n in range(Nstep):
            elements = Elems[n]  # 针对每个构型
            # 原子数不会变，就是不合并的元素总数
            f.write("%d\n" % len(elements))
            # lattice
            f.write(
                'Lattice="%f %f %f %f %f %f %f %f %f" Properties=species:S:1:pos:R:3 pbc="T T T"\n'
                % (
                    Latvs[n, 0],
                    Latvs[n, 1],
                    Latvs[n, 2],
                    Latvs[n, 3],
                    Latvs[n, 4],
                    Latvs[n, 5],
                    Latvs[n, 6],
                    Latvs[n, 7],
                    Latvs[n, 8],
                )
            )
            # position and element
            for i in range(len(elements)):
                f.write(
                    "%s %f %f %f\n"
                    % (elements[i], Poses[n, i, 0], Poses[n, i, 1], Poses[n, i, 2])
                )
    print(f"==> {absolute_output}")


@logger.catch
def _from_structures(directory: str, ls: bool = False):
    """从structure00.as，structure01.as，...，中读取结构信息，
    写入neb_chain_init，以便用DeviceStudio打开观察

    Parameters
    ----------
    directory : str
        NEB计算路径，默认当前路径
    ls: bool
        是否是最新构型

    Returns
    -------
    用于json文件的各个数组
    """
    import os

    absdir = os.path.abspath(directory)
    if ls:
        output = "neb_chain_last.json"
    else:
        output = "neb_chain_init.json"
    step = 0

    subfolders = get_neb_subfolders(absdir)
    nimage = len(subfolders)
    import numpy as np

    reactionCoordinates = np.zeros(shape=nimage)  # optional
    totalEnergies = np.zeros(shape=nimage)  # optional
    maxForces = np.zeros(shape=nimage - 2)  # optional
    tangents = np.zeros(shape=nimage - 2)  # optional
    MaxForces = np.zeros(shape=(nimage - 2, step + 1))  # optional
    TotalEnergies = np.zeros(shape=(nimage - 2, step + 1))  # optional

    Poses = []  # nimage x Natom x 3 , read
    Elems = []  # nimage x Natom, read
    Latvs = []  # nimage x 9, read

    iDirects = []  # read coordinate type
    from dspawpy.io.structure import read

    for i, folder in enumerate(subfolders):
        if ls and i != 0 and i != len(subfolders) - 1:
            structure_path = os.path.join(absdir, folder, f"latestStructure{folder}.as")
        else:
            structure_path = os.path.join(absdir, folder, f"structure{folder}.as")
        if not os.path.isfile(structure_path):
            raise FileNotFoundError(f"No {structure_path}！")
        structure = read(structure_path, task="free")[0]
        pos = structure.cart_coords
        ele = [str(i) for i in structure.species]
        lat = structure.lattice.matrix
        Poses.append(pos)
        Elems.append(ele)
        Latvs.append(lat)
        with open(structure_path, "r") as f:
            lines = f.readlines()
            coordinateType = lines[6].split()[0]
            if coordinateType == "Direct":
                iDirect = True
            elif coordinateType == "Cartesian":
                iDirect = False
            else:
                raise ValueError(
                    f"coordinateType in {structure_path} is neither Direct nor Cartesian!"
                )
            iDirects.append(iDirect)
    Natom = len(Elems[0])

    # reshape data
    Poses = np.array(Poses).reshape((nimage, Natom, 3))
    Elems = np.array(Elems).reshape((nimage, Natom))
    Latvs = np.array(Latvs).reshape((nimage, 9))
    Fixs = np.zeros(shape=(Natom, 3))  # optional

    return (
        output,
        subfolders,
        step,
        MaxForces,
        TotalEnergies,
        Poses,
        Latvs,
        Elems,
        Fixs,
        reactionCoordinates,
        totalEnergies,
        maxForces,
        tangents,
        iDirects,
    )


@logger.catch
def _from_h5(directory: str, step: int):
    """从NEB路径下的h5文件读取 从第一步开始到指定step数 的结构和能量信息，
    写入json文件，以便用DeviceStudio打开观察。

    支持热读取结构信息（其他信息忽略）

    Parameters
    ----------
    directory : str
        NEB路径，默认当前路径
    step : int
        step数，默认-1，读取最后一个构型

    Returns
    -------
    用于json文件的各个数组
    """
    import os

    absdir = os.path.abspath(directory)
    # ^ 前期设置
    neb_h5 = os.path.abspath(os.path.join(absdir, "01", "neb01.h5"))
    from dspawpy.io.read import get_ele_from_h5

    ele = get_ele_from_h5(hpath=neb_h5)
    Natom = len(ele)
    import h5py

    data = h5py.File(neb_h5)
    import numpy as np

    try:
        total_steps = np.array(data.get("/NebSize"))[0]
    except Exception:
        print("Reading latest info for unfinished NEB task...")
        try:
            total_steps = np.array(data.get("/Structures/FinalStep"))[0]
        except Exception:
            raise ValueError(
                f"No finished ionic step detected, please check {neb_h5} file or wait for NEB task to finished at least one ionic step."
            )

    if step == -1:
        output = "neb_chain_last.json"
        step = total_steps
    elif step > total_steps:
        output = "neb_chain_last.json"
        step = total_steps
        logger.warning(
            "specified %s > %s, reading last step info..." % (step, total_steps)
        )
    else:
        output = "neb_chain_{}.json".format(step)

    # ^ 读取前，准备好json文件所需数组框架
    subfolders = get_neb_subfolders(absdir)
    nimage = len(subfolders)
    reactionCoordinates = np.zeros(shape=nimage)  # optional
    totalEnergies = np.zeros(shape=nimage)  # optional，每个构型最终能量
    maxForces = np.zeros(shape=nimage - 2)  # optional
    tangents = np.zeros(shape=nimage - 2)  # optional
    MaxForces = np.zeros(shape=(nimage - 2, step))  # optional
    TotalEnergies = np.zeros(
        shape=(nimage - 2, step)
    )  # optional，中间构型每个离子步能量
    # Sposes = []  # nimage x Natom x 3 , read
    Sposes = np.empty(shape=(nimage, Natom, 3))  # nimage x Natom x 3 , read
    Elems = []  # nimage x Natom, read
    Latvs = []  # nimage x 9, read
    Fixs = []  # Natom x 3, set

    for folder in subfolders:
        """如果是首尾两个构型，最多只有scf.h5文件，没有neb.h5文件
        用户如果算NEB的时候，不计算首尾构型的自洽，
         或者在别处算完了但是没有复制到首尾文件夹中并命名为scf.h5，
          便不能使用第一个功能
        """
        if folder == subfolders[0] or folder == subfolders[-1]:
            h5_path = os.path.join(absdir, folder, "scf.h5")
            spath = os.path.join(absdir, folder, f"structure{folder}.as")
            assert os.path.isfile(h5_path) or os.path.isfile(
                spath
            ), f"{h5_path} and {spath} are both missing!"
        else:
            h5_path = os.path.join(absdir, folder, f"neb{folder}.h5")
            assert os.path.isfile(h5_path), f"No {h5_path}!"

    # ^ 开始分功能读取数据
    from dspawpy.io.structure import read

    for i, folder in enumerate(subfolders):
        if folder == subfolders[0] or folder == subfolders[-1]:
            h5_path = os.path.join(absdir, folder, "scf.h5")
            spath = os.path.join(absdir, folder, f"structure{folder}.as")
            if os.path.isfile(h5_path):
                data = h5py.File(h5_path)
                # 不影响可视化，直接定为0
                if folder == subfolders[0]:
                    reactionCoordinates[i] = 0
                pos = np.array(data.get("/Structures/Step-1/Position")).reshape(
                    -1, 3
                )  # scaled
                lat = np.array(data.get("/Structures/Step-1/Lattice"))
                ele = get_ele_from_h5(hpath=h5_path)
                totalEnergies[i] = np.array(data.get("/Energy/TotalEnergy0"))
            else:
                structure = read(spath, task="neb")[0]
                pos = structure.frac_coords
                ele = [str(i) for i in structure.species]
                lat = structure.lattice.matrix
        else:
            h5_path = os.path.join(absdir, folder, f"neb{folder}.h5")
            data = h5py.File(h5_path)
            # reading...
            try:
                reactionCoordinates[i - 1] = np.array(data.get("/Distance/Previous"))[
                    -1
                ]
                maxForces[i - 1] = np.array(data.get("/MaxForce"))[-1]
                tangents[i - 1] = np.array(data.get("/Tangent"))[-1]
                if folder == subfolders[-2]:
                    reactionCoordinates[i + 1] = np.array(data.get("/Distance/Next"))[
                        -1
                    ]
                # read MaxForces and TotalEnergies
                nionStep = np.array(data.get("/MaxForce")).shape[0]
                assert (
                    step <= nionStep
                ), f"The number of finished ionic steps is {nionStep}"
                for j in range(step):
                    MaxForces[i - 1, j] = np.array(data.get("/MaxForce"))[j]
                    TotalEnergies[i - 1, j] = np.array(data.get("/TotalEnergy"))[j]
                totalEnergies[i] = np.array(data.get("/Energy/TotalEnergy0"))
            except Exception:
                pass  # 还没完成NEB计算，不影响读取结构信息用于可视化
            # read the latest structure for visualization
            pos = np.array(data.get(f"/Structures/Step-{step}/Position")).reshape(
                Natom, 3
            )  # scaled
            lat = np.array(data.get(f"/Structures/Step-{step}/Lattice"))
            ele = get_ele_from_h5(hpath=h5_path)

        Elems.append(ele)
        Sposes[i, :, :] = pos
        Latvs.append(lat)

    if os.path.isfile(os.path.join(absdir, "neb.h5")):
        tdata = h5py.File(os.path.join(absdir, "neb.h5"))
        # atom fix, not lattice
        # ignore this trivial message because it is not necessary for the visualization
        if "/UnrelaxStructure/Image00/Fix" in tdata:
            fix_array = np.array(tdata.get("/UnrelaxStructure/Image00/Fix"))
            for fix in fix_array:
                if fix == 0.0:
                    F = False
                elif fix == 1.0:
                    F = True
                else:
                    raise ValueError("Fix must be 0/1")
                Fixs.append(F)
        else:
            Fixs = np.full(shape=(Natom, 3), fill_value=False)
    else:
        Fixs = np.full(shape=(Natom, 3), fill_value=False)

    Elems = np.array(Elems).reshape((nimage, Natom))
    Latvs = np.array(Latvs).reshape((nimage, 9))
    Fixs = np.array(Fixs).reshape((Natom, 3))
    iDirects = [True for i in range(Natom)]  # only output direct coordinates

    return (
        output,
        subfolders,
        step,
        MaxForces,
        TotalEnergies,  #
        Sposes,
        Latvs,
        Elems,
        Fixs,
        reactionCoordinates,
        totalEnergies,
        maxForces,
        tangents,
        iDirects,
    )


@logger.catch
def _from_json(directory: str, step: int):
    """从NEB路径下的json文件读取 从第一步开始到指定step数 的结构和能量信息，
    写入json文件，以便用DeviceStudio打开观察

    Parameters
    ----------
    directory : str
        NEB路径，默认当前路径
    step : int
        step数，默认-1，读取最后一个构型

    Returns
    -------
    用于json文件的各个数组
    """

    import os
    from json import load

    import numpy as np

    absdir = os.path.abspath(directory)
    # ^ 前期设置
    neb_js = os.path.join(absdir, "01/neb01.json")
    with open(neb_js, "r") as f:
        data = load(f)
    total_steps = len(data)

    if step == -1:
        output = "neb_chain_last.json"
        step = total_steps
    elif step > total_steps:
        output = "neb_chain_last.json"
        step = total_steps
        logger.warning(
            "specified %s > %s, reading last step info..." % (step, total_steps)
        )
    else:
        output = f"neb_chain_{step}.json"

    # ^ 读取前，准备好json文件所需数组框架
    subfolders = get_neb_subfolders(absdir)
    nimage = len(subfolders)
    reactionCoordinates = np.zeros(shape=nimage)  # optional
    totalEnergies = np.zeros(shape=nimage)  # optional，每个构型最终能量
    maxForces = np.zeros(shape=nimage - 2)  # optional
    tangents = np.zeros(shape=nimage - 2)  # optional
    MaxForces = np.zeros(shape=(nimage - 2, step))  # optional
    TotalEnergies = np.zeros(
        shape=(nimage - 2, step)
    )  # optional，中间构型每个离子步能量
    Sposes = []  # nimage x Natom x 3 , read
    Elems = []  # nimage x Natom, read
    Latvs = []  # nimage x 9, read
    Fixs = []  # Natom x 3, set

    for folder in subfolders:
        """如果是首尾两个构型，最多只有system.json文件，没有neb*.json文件
        用户如果算NEB的时候，不计算首尾构型的自洽，
         或者在别处算完了但是没有复制到首尾文件夹中并命名为system.json，
          便不能使用第一个功能
        """
        if folder == subfolders[0] or folder == subfolders[-1]:
            js_path = os.path.join(absdir, folder, "system.json")
        else:
            js_path = os.path.join(absdir, folder, f"neb{folder}.json")
        assert os.path.isfile(js_path), f"No {js_path}"

    # ^ 开始分功能读取数据
    for i, folder in enumerate(subfolders):
        if i == 0:  # 初末态在NEB计算过程中不会优化结构
            # 1. 外部自洽后移动system.json
            js_path = os.path.join(absdir, folder, "system.json")
            # 2. 直接NEB计算，得到system00.json
            neb_js_path = os.path.join(absdir, folder, f"system{folder}.json")
            if os.path.isfile(neb_js_path):  # 优先读取neb计算得到的system00.json
                with open(neb_js_path, "r") as f:
                    data = load(f)

            elif os.path.isfile(js_path):
                with open(js_path, "r") as f:
                    data = load(f)

            else:
                raise FileNotFoundError(f"No {js_path}/{neb_js_path}")

            lat = data["AtomInfo"]["Lattice"]
            Latvs.append(lat)

            Natom = len(data["AtomInfo"]["Atoms"])  # 读取原子数
            for j in range(Natom):
                pos = data["AtomInfo"]["Atoms"][j]["Position"]  # scaled
                Sposes.append(pos)

            totalEnergies[i] = data["Energy"]["TotalEnergy0"]
            reactionCoordinates[i] = 0.0

        elif i > 0 and i < nimage - 1:  # 中间构型会优化结构
            # 读取晶胞矢量、原子坐标
            relax_json = os.path.join(absdir, folder, "relax.json")
            assert os.path.isfile(relax_json), f"No {relax_json}!"

            with open(relax_json, "r") as f:
                rdata = load(f)

            lat = rdata[step - 1]["Lattice"]  # 第step步优化后的晶胞
            Latvs.append(lat)

            Natom = len(rdata[0]["Atoms"])
            for j in range(Natom):  # for each atom
                pos = rdata[step - 1]["Atoms"][j][
                    "Position"
                ]  # 第step步优化后的原子坐标
                Sposes.append(pos)  # ! 输出的都是分数坐标

            # 读取能量和反应坐标
            nj = os.path.join(absdir, folder, f"neb{folder}.json")
            with open(nj, "r") as f:
                ndata = load(f)

            totalEnergies[i] = ndata[step - 1][
                "TotalEnergy"
            ]  # 读取第step步优化后的能量

            # 读取与前一个构型相比的反应坐标
            reactionCoordinates[i - 1] = ndata[step - 1]["ReactionCoordinate"][-2]
            tangents[i - 1] = ndata[step - 1]["Tangent"]
            if folder == subfolders[-2]:  # 末态前一个构型的计算结果中读取反应坐标
                reactionCoordinates[i + 1] = ndata[step - 1]["ReactionCoordinate"][-1]
            for j in range(step):
                MaxForces[i - 1, j] = ndata[j]["MaxForce"]
                # neb01.json中不存在TotalEnergy0，暂时读取TotalEnergy
                TotalEnergies[i - 1, j] = ndata[j]["TotalEnergy"]

        else:  # 末态构型
            js_path = os.path.join(absdir, folder, "system.json")
            neb_js_path = os.path.join(absdir, folder, f"system{folder}.json")
            if os.path.isfile(neb_js_path):  # 优先读取neb计算得到的json文件
                with open(neb_js_path, "r") as f:
                    data = load(f)

            elif os.path.isfile(js_path):
                with open(js_path, "r") as f:
                    data = load(f)

            else:
                raise FileNotFoundError(f"No {js_path}/{neb_js_path}")

            lat = data["AtomInfo"]["Lattice"]
            Latvs.append(lat)

            Natom = len(data["AtomInfo"]["Atoms"])  # 读取原子数
            for j in range(Natom):
                pos = data["AtomInfo"]["Atoms"][j]["Position"]  # scaled
                Sposes.append(pos)

            energy = data["Energy"]["TotalEnergy0"]
            totalEnergies[i] = energy

    # 读取原子元素
    tneb_js = os.path.join(absdir, "neb.json")
    with open(tneb_js, "r") as f:
        tdata = load(f)

    Natom = len(tdata["UnrelaxStructure"][0]["Atoms"])
    elems = []
    for k in range(Natom):
        ele = tdata["UnrelaxStructure"][0]["Atoms"][k]["Element"]
        elems.append(ele)

    for ni in range(nimage):
        Elems.append(elems)  # 重复nimage次，保持Elems结构一致

    for atom in range(Natom):
        fix_array = tdata["UnrelaxStructure"][1]["Atoms"][atom]["Fix"]  # (1,3)
        if fix_array == []:  # empty list
            fix_array = [0.0, 0.0, 0.0]
        for fix in fix_array:
            if fix == 0.0:
                F = False
            elif fix == 1.0:
                F = True
            else:
                raise ValueError("Fix should be 0.0/1.0 in json file!")
            Fixs.append(F)

    # 累加reactionCoordinates中的元素
    for i in range(1, len(reactionCoordinates)):
        reactionCoordinates[i] += reactionCoordinates[i - 1]

    # reshape data
    Sposes = np.array(Sposes).reshape((nimage, Natom, 3))
    Elems = np.array(Elems).reshape((nimage, Natom))
    Latvs = np.array(Latvs).reshape((nimage, 9))
    Fixs = np.array(Fixs).reshape((Natom, 3))
    iDirects = [True for i in range(Natom)]  # only output direct coordinates

    return (
        output,
        subfolders,
        step,
        MaxForces,
        TotalEnergies,
        Sposes,
        Latvs,
        Elems,
        Fixs,
        reactionCoordinates,
        totalEnergies,
        maxForces,
        tangents,
        iDirects,
    )


@logger.catch
def _dump_neb_chain_json(raw):
    """根据之前收集到的各数据列表，dump json文件到output"""
    (
        output,
        subfolders,
        step,
        MaxForces,
        TotalEnergies,
        Poses,
        Latvs,
        Elems,
        Fixs,
        reactionCoordinates,
        totalEnergies,
        maxForces,
        tangents,
        iDirects,
    ) = raw

    IterDict = {}
    for s, sf in enumerate(subfolders):
        if sf == subfolders[0] or sf == subfolders[-1]:
            continue
        else:
            Eflist = []
            for _i in range(step):
                ef = {
                    "MaxForce": MaxForces[s - 1, _i],
                    "TotalEnergy": TotalEnergies[s - 1, _i],
                }
                Eflist.append(ef)
                iterDict = {sf: Eflist}  # construct sub-dict
                IterDict.update(iterDict)  # append sub-dict

    RSList = []
    """
    从外到内依次遍历 构型、原子（子字典）
    原子的键值对为：'Atoms': 原子信息列表
    原子信息列表是一个由字典组成的列表，每个字典对应一个原子的信息
    """
    for s, sf in enumerate(subfolders):
        pos = Poses[s]
        lat = Latvs[s]
        elem = Elems[s]
        atoms = []
        for i in range(len(elem)):
            atom = {
                "Element": elem[i],
                "Fix": Fixs[i].tolist(),
                "Mag": [],  # empty
                "Position": pos[i].tolist(),
                "Pot": "",
            }  # empty
            atoms.append(atom)
        if iDirects[s]:
            rs = {"Atoms": atoms, "CoordinateType": "Direct", "Lattice": lat.tolist()}
        else:
            rs = {
                "Atoms": atoms,
                "CoordinateType": "Cartesian",
                "Lattice": lat.tolist(),
            }
        RSList.append(rs)

    URSList = []  # DS似乎并不读取这部分信息，空置即可

    data = {
        "Distance": {"ReactionCoordinate": reactionCoordinates.tolist()},
        "Energy": {"TotalEnergy": totalEnergies.tolist()},
        "Force": {"MaxForce": maxForces.tolist(), "Tangent": tangents.tolist()},
        "Iteration": IterDict,
        "RelaxedStructure": RSList,
        "UnrelaxedStructure": URSList,
    }

    # ^ 将字典写入json文件
    import os

    absolute_output = os.path.abspath(output)
    with open(absolute_output, "w") as f:
        from json import dump

        dump(data, f, indent=4)

    print(f"==> {absolute_output}")


@logger.catch
def _getef(directory: str = "."):
    """读取NEB计算时各构型的能量和受力，NEB计算可以未收敛
    但如果初末态自洽在别处完成，请手动将其移入00等文件夹中！

    Parameters
    ----------
    directory: str
        NEB计算的路径，默认当前路径

    Returns
    -------
    subfolders: list
        构型文件夹名列表
    resort_mfs: list
        构型受力的最大分量列表
    rcs: list
        反应坐标列表
    ens: list
        电子总能列表
    dEs: list
        与初始构型的能量差列表
    """
    import os

    import numpy as np

    absdir = os.path.abspath(directory)
    subfolders = get_neb_subfolders(absdir)
    Nimage = len(subfolders)

    ens = []
    dEs = np.zeros(Nimage)
    rcs = [0]
    mfs = []

    # read energies
    import h5py

    count = 1
    for i, subfolder in enumerate(subfolders):
        if i == 0 or i == Nimage - 1:
            jsf = os.path.join(absdir, subfolder, f"system{subfolder}.json")
            old_jsf = os.path.join(absdir, subfolder, "system.json")
            hf = os.path.join(absdir, subfolder, "scf.h5")

            if os.path.isfile(hf):  # 优先读取h5文件内容
                data = h5py.File(hf)
                en = np.array(data.get("/Energy/TotalEnergy0"))[0]
                if i == 0 or i == Nimage - 1:
                    mf = np.max(np.abs(np.array(data.get("/Force/ForceOnAtoms"))))
                    mfs.append(mf)

            elif os.path.isfile(jsf):  # 其次读取json文件内容
                with open(jsf, "r") as f:
                    from json import load

                    data = load(f)
                en = data["Energy"]["TotalEnergy0"]
                if i == 0 or i == Nimage - 1:
                    mf = np.max(np.abs(data["Force"]["ForceOnAtoms"]))
                    mfs.append(mf)

            elif os.path.isfile(old_jsf):  # 兼容老json
                with open(old_jsf, "r") as f:
                    from json import load

                    data = load(f)
                en = data["Energy"]["TotalEnergy0"]
                if i == 0 or i == Nimage - 1:
                    mf = np.max(np.abs(data["Force"]["ForceOnAtoms"]))
                    mfs.append(mf)

            else:
                raise FileNotFoundError(f"No {jsf}/{old_jsf}/{hf} for {subfolder}")
            ens.append(en)

        else:
            jsf = os.path.join(absdir, subfolder, f"neb{subfolder}.json")
            sysjsf = os.path.join(absdir, subfolder, f"system{subfolder}.json")
            old_sysjsf = os.path.join(absdir, subfolder, "system.json")
            hf = os.path.join(absdir, subfolder, f"neb{subfolder}.h5")

            if os.path.isfile(hf):  # 优先读取h5文件内容
                data = h5py.File(hf)
                en = np.array(data.get("/Energy/TotalEnergy0"))[0]
                mf = np.array(data.get("/MaxForce"))[-1]
                # the key may change depends on your DS-PAW version
                if "/Distance/Previous" in data:
                    rc = np.array(data.get("/Distance/Previous"))[-1]
                elif "/ReactionCoordinate" in data:
                    rc = np.array(data.get("/ReactionCoordinate"))[-2]
                else:
                    raise KeyError(
                        f"Neither /Distance/Previous nor /ReactionCoordinate in {hf}"
                    )
                rcs.append(rc)
                if count == Nimage - 2:  # before final image
                    if "/Distance/Next" in data:
                        rc = np.array(data.get("/Distance/Next"))[-1]
                    elif "/ReactionCoordinate" in data:
                        rc = np.array(data.get("/ReactionCoordinate"))[-1]
                    else:
                        raise KeyError(
                            f"Neither /Distance/Next nor /ReactionCoordinate in {hf}"
                        )
                    rcs.append(rc)

            elif os.path.isfile(jsf):
                from json import load

                if os.path.isfile(sysjsf):
                    with open(sysjsf, "r") as f:
                        data = load(f)
                    en = data["Energy"]["TotalEnergy0"]
                elif os.path.isfile(old_sysjsf):  # 兼容旧版DS-PAW
                    with open(old_sysjsf, "r") as f:
                        data = load(f)
                    en = data["Energy"]["TotalEnergy0"]
                else:
                    raise FileNotFoundError(f"No {sysjsf}/{old_sysjsf}")

                with open(jsf, "r") as f:
                    data = load(f)
                Nion_step = len(data)
                # en = data[Nion_step - 1]["TotalEnergy"] # invalid
                mf = data[Nion_step - 1]["MaxForce"]  # 最后一步的最大受力
                rc = data[Nion_step - 1]["ReactionCoordinate"][0]  # 最后一步的反应坐标
                rcs.append(rc)
                if count == Nimage - 2:  # before final image
                    rc = data[Nion_step - 1]["ReactionCoordinate"][
                        1
                    ]  # 最后一步的反应坐标
                    rcs.append(rc)

            else:
                raise FileNotFoundError(f"No {hf}/{jsf}")

            ens.append(en)
            mfs.append(mf)

            # get dE
            dE = ens[count] - ens[0]
            dEs[i] = dE
            count += 1
    dEs[-1] = ens[Nimage - 1] - ens[0]

    # 从 nebXX.h5/json 读取的 rcs 需要改成累加值
    for i in range(1, len(rcs)):
        rcs[i] += rcs[i - 1]

    rcs = np.array(rcs)

    resort_mfs = [mfs[0]]
    final_mf = mfs[1]
    for j in range(2, len(mfs)):
        resort_mfs.append(mfs[j])
    resort_mfs.append(final_mf)

    return subfolders, resort_mfs, rcs, ens, dEs


# @logger.catch
# def plot_barrier_old(
#     datafile: str = "neb.h5",
#     directory: Optional[str] = None,
#     ri: Optional[float] = None,
#     rf: Optional[float] = None,
#     ei: Optional[float] = None,
#     ef: Optional[float] = None,
#     method: str = "PchipInterpolator",
#     figname: str = "neb_barrier.png",
#     show: bool = True,
#     raw: bool = False,
#     verbose: bool = False,
#     **kwargs,
# ):
#     r"""与plot_barrier()唯一的区别在于反应坐标视为累加值，而不是单个值"""
#     import os
#     from json import load
#
#     import numpy as np
#
#     if directory is not None:
#         # read data
#         subfolders, resort_mfs, rcs, ens, dEs = _getef(os.path.abspath(directory))
#
#     elif datafile:
#         from dspawpy.io.utils import get_absfile
#
#         absfile = get_absfile(
#             datafile, task="neb", verbose=verbose
#         )  # -> return either .h5 or .json
#         if absfile.endswith(".h5"):
#             from dspawpy.io.read import load_h5
#
#             neb = load_h5(absfile)
#             if "/BarrierInfo/ReactionCoordinate" in neb.keys():
#                 reaction_coordinate = neb["/BarrierInfo/ReactionCoordinate"]
#                 energy = neb["/BarrierInfo/TotalEnergy"]
#             else:  # old version
#                 reaction_coordinate = neb["/Distance/ReactionCoordinate"]
#                 energy = neb["/Energy/TotalEnergy"]
#         elif absfile.endswith(".json"):
#             with open(absfile, "r") as fin:
#                 neb = load(fin)
#             if "BarrierInfo" in neb.keys():
#                 reaction_coordinate = neb["BarrierInfo"]["ReactionCoordinate"]
#                 energy = neb["BarrierInfo"]["TotalEnergy"]
#             else:  # old version
#                 reaction_coordinate = neb["Distance"]["ReactionCoordinate"]
#                 energy = neb["Energy"]["TotalEnergy"]
#
#         else:
#             raise ValueError("Only h5 and json file are supported")
#
#         x = []
#         for c in reaction_coordinate:
#             if len(x) > 0:  # add previous reaction coordinate
#                 x.append(x[-1] + c)
#             else:
#                 x.append(c)
#
#         y = [x - energy[0] for x in energy]
#         # initial and final info
#         if ri is not None:  # add initial reaction coordinate
#             x.insert(0, ri)
#         if rf is not None:  # add final reaction coordinate
#             x.append(rf)
#
#         if ei is not None:  # add initial energy
#             y.insert(0, ei)
#         if ef is not None:  # add final energy
#             y.append(ef)
#
#         rcs = np.array(x)
#         dEs = np.array(y)
#
#     else:
#         raise ValueError("Please specify directory or datafile!")
#
#     # import scipy interpolater
#     try:
#         interpolate_method = getattr(
#             __import__("scipy.interpolate", fromlist=[method]), method
#         )
#     except Exception:
#         raise ImportError(f"No scipy.interpolate.{method} method！")
#     # call the interpolater to interpolate with given kwargs
#     try:
#         inter_f = interpolate_method(rcs, dEs, **kwargs)
#     except Exception:
#         raise ValueError(f"Please check whether {kwargs} is valid for {method}！")
#
#     xnew = np.linspace(rcs[0], rcs[-1], 100)
#     ynew = inter_f(xnew)
#
#     if raw:
#         import polars as pl
#
#         pl.DataFrame({"x_raw": rcs, "y_raw": dEs}).write_csv("raw_xy.csv")
#         pl.DataFrame({"x_interpolated": xnew, "y_interpolated": ynew}).write_csv(
#             "raw_interpolated_xy.csv"
#         )
#     # plot
#     import matplotlib.pyplot as plt  # noqa: E402
#
#     if kwargs:
#         plt.plot(xnew, ynew, label=method + str(kwargs))
#     else:
#         plt.plot(xnew, ynew, label=method)
#     plt.scatter(rcs, dEs, c="r")
#     plt.xlabel("Reaction Coordinate (Å)")
#     plt.ylabel("Energy (eV)")
#     plt.legend()
#
#     plt.tight_layout()
#     # save and show
#     if figname:
#         absfig = os.path.abspath(figname)
#         os.makedirs(os.path.dirname(absfig), exist_ok=True)
#         plt.savefig(absfig, dpi=300)
#         print(f"==> {absfig}")
#     if show:
#         plt.show()
