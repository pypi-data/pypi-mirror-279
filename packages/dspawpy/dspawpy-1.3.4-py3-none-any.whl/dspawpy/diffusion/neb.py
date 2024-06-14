# -*- coding: utf-8 -*-
from loguru import logger


class NEB:
    @logger.catch
    def __init__(self, initial_structure, final_structure, nimages: int):
        self.nimages = nimages
        from dspawpy.diffusion.pathfinder import IDPPSolver

        self.iddp = IDPPSolver.from_endpoints(
            endpoints=[initial_structure, final_structure],
            nimages=self.nimages - 2,
            sort_tol=0,  # 锁定原子编号
        )

    @logger.catch
    def linear_interpolate(self):
        return self.iddp.structures

    @logger.catch
    def idpp_interpolate(
        self,
        maxiter: int = 1000,
        tol: float = 1e-5,
        gtol: float = 1e-3,
        step_size: float = 0.05,
        max_disp: float = 0.05,
        spring_const: float = 5.0,
    ):
        return self.iddp.run(maxiter, tol, gtol, step_size, max_disp, spring_const)


@logger.catch
def write_neb_structures(
    structures: list,
    coords_are_cartesian: bool = True,
    fmt: str = "as",
    path: str = ".",
    prefix="structure",
):
    r"""插值并生成中间构型文件

    Parameters
    ----------
    structures: list
        构型列表
    coords_are_cartesian: bool
        坐标是否为笛卡尔坐标
    fmt: str
        结构文件类型，默认为 "as"
    path: str
        保存路径
    prefix: str
        文件名前缀，默认为 "structure"，这样的话生成的就是 structure00.as, structure01.as, ...

    Returns
    -------
    file
        保存构型文件

    Examples
    --------

    先读取as文件创建structure对象

    >>> from dspawpy.io.structure import read
    >>> init_struct = read("dspawpy_proj/dspawpy_tests/inputs/2.15/00/structure00.as")[0]
    >>> final_struct = read("dspawpy_proj/dspawpy_tests/inputs/2.15/04/structure04.as")[0]

    然后，插值并生成中间构型文件

    >>> from dspawpy.diffusion.neb import NEB,write_neb_structures
    >>> neb = NEB(init_struct,final_struct,8)
    >>> structures = neb.linear_interpolate()   #线性插值

    插值完成的构型可指定保存到neb文件夹下

    >>> write_neb_structures(structures, path="dspawpy_proj/dspawpy_tests/outputs/doctest/11neb_interpolate_structures") # doctest: +ELLIPSIS
    ==> ...dspawpy_proj/dspawpy_tests/outputs/doctest/11neb_interpolate_structures/00/structure00.as
    ==> ...dspawpy_proj/dspawpy_tests/outputs/doctest/11neb_interpolate_structures/01/structure01.as
    ==> ...dspawpy_proj/dspawpy_tests/outputs/doctest/11neb_interpolate_structures/02/structure02.as
    ==> ...dspawpy_proj/dspawpy_tests/outputs/doctest/11neb_interpolate_structures/03/structure03.as
    ==> ...dspawpy_proj/dspawpy_tests/outputs/doctest/11neb_interpolate_structures/04/structure04.as
    ==> ...dspawpy_proj/dspawpy_tests/outputs/doctest/11neb_interpolate_structures/05/structure05.as
    ==> ...dspawpy_proj/dspawpy_tests/outputs/doctest/11neb_interpolate_structures/06/structure06.as
    ==> ...dspawpy_proj/dspawpy_tests/outputs/doctest/11neb_interpolate_structures/07/structure07.as
    """
    if fmt is None:
        fmt = "as"
    import os

    absdir = os.path.abspath(path)
    N = len(str(len(structures)))
    if N <= 2:
        N = 2
    from dspawpy.io.structure import write

    for i, structure in enumerate(structures):
        path_name = str(i).zfill(N)
        os.makedirs(os.path.join(absdir, path_name), exist_ok=True)
        filename = os.path.join(absdir, path_name, "%s%s.%s" % (prefix, path_name, fmt))
        write(structure, filename, fmt, coords_are_cartesian)
