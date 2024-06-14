# -*- coding: utf-8 -*-
from typing import List, Optional, Sequence

from loguru import logger

Bohr = 0.52917721067  # Angstrom


@logger.catch
def _write_xyz_traj(
    structures: list,
    xyzfile: str = "aimdTraj.xyz",
):
    r"""保存xyz格式的轨迹文件

    Parameters
    ----------
    structures: list
        pymatgen的Structures列表
    xyzfile : str
        写入xyz格式的轨迹文件，默认为aimdTraj.xyz
    """
    import os

    if not isinstance(structures, list):  # single Structure
        structures = [structures]
    absxyz = os.path.abspath(xyzfile)
    if os.path.isfile(absxyz):
        logger.warning(
            f"{absxyz} already exists and will be overwritten!",
            category=UserWarning,
        )
    os.makedirs(os.path.dirname(absxyz), exist_ok=True)
    with open(absxyz, "w") as f:
        # Nstep
        for _, structure in enumerate(structures):
            elements = [s.species_string for s in structure.sites]
            f.write("%d\n" % len(elements))
            # lattice
            lm = structure.lattice.matrix
            f.write(
                'Lattice="%f %f %f %f %f %f %f %f %f" Properties=species:S:1:pos:R:3 pbc="T T T"\n'
                % (
                    lm[0, 0],
                    lm[0, 1],
                    lm[0, 2],
                    lm[1, 0],
                    lm[1, 1],
                    lm[1, 2],
                    lm[2, 0],
                    lm[2, 1],
                    lm[2, 2],
                )
            )
            # position and element
            poses = structure.cart_coords
            for j in range(len(elements)):
                f.write(
                    "%s %f %f %f\n"
                    % (elements[j], poses[j, 0], poses[j, 1], poses[j, 2])
                )

    print(f"==> {absxyz}")


@logger.catch
def _write_dump_traj(
    structures: list,
    dumpfile: str = "aimdTraj.dump",
):
    r"""保存为lammps的dump格式的轨迹文件，暂时只支持正交晶胞

    Parameters
    ----------
    structures: list
        pymatgen的Structures列表
    dumpfile : str
        dump格式的轨迹文件名，默认为aimdTraj.dump
    """
    import os

    if not isinstance(structures, list):  # single Structure
        structures = [structures]
    absdump = os.path.abspath(dumpfile)
    logger.warning(f"{absdump} already exists and will be overwritten!")
    os.makedirs(os.path.dirname(absdump), exist_ok=True)
    from dspawpy.io.read import _get_lammps_non_orthogonal_box

    with open(absdump, "w") as f:
        for n, structure in enumerate(structures):
            lat = structure.lattice.matrix
            elements = [s.species_string for s in structure.sites]
            poses = structure.cart_coords

            box_bounds = _get_lammps_non_orthogonal_box(lat)
            f.write("ITEM: TIMESTEP\n%d\n" % n)
            f.write("ITEM: NUMBER OF ATOMS\n%d\n" % (len(elements)))
            f.write("ITEM: BOX BOUNDS xy xz yz xx yy zz\n")
            f.write(
                "%f %f %f\n%f %f %f\n %f %f %f\n"
                % (
                    box_bounds[0][0],
                    box_bounds[0][1],
                    box_bounds[0][2],
                    box_bounds[1][0],
                    box_bounds[1][1],
                    box_bounds[1][2],
                    box_bounds[2][0],
                    box_bounds[2][1],
                    box_bounds[2][2],
                )
            )
            f.write("ITEM: ATOMS type x y z id\n")
            for i in range(len(elements)):
                f.write(
                    "%s %f %f %f %d\n"
                    % (
                        elements[i],
                        poses[i, 0],
                        poses[i, 1],
                        poses[i, 2],
                        i + 1,
                    )
                )
    print(f"==> {absdump}")


@logger.catch
def write_VESTA(
    in_filename: str,
    data_type: str,
    out_filename: str = "DS-PAW.cube",
    subtype: Optional[str] = None,
    format: str = "cube",
    compact: bool = False,
    inorm: bool = False,
    gridsize: Optional[Sequence[int]] = None,
):
    """从包含电子体系信息的json或h5文件中读取数据并写入VESTA格式的文件中

    Parameters
    ----------
    in_filename : str
        包含电子体系信息的json或h5文件路径
    data_type: str
        数据类型，支持 "rho", "potential", "elf", "pcharge", "rhoBound"
    out_filename : str
        输出文件路径, 默认 "DS-PAW.cube"
    subtype : Optional[str]
        用于指定data_type的数据子类型，默认为None，将读取 potential 的 TotalElectrostaticPotential 数据
    format : str
        输出的数据格式，支持 "cube" 和 "vesta" （"vasp"），默认为 "cube"，大小写不敏感
    compact : bool
        每个格点的数据都换行，通过减少空格数量减小文件体积（不会影响VESTA软件的解析），默认为False
    inorm : bool
        是否归一化体积数据，使其总和为1，默认为False
    gridsize: Optional[Sequence[int]]
        重新定义的格点数，格式为 (ngx, ngy, ngz)，默认为None，即使用原始格点数

    Returns
    --------
    out_filename : file
        VESTA格式的文件

    Examples
    --------
    >>> from dspawpy.io.write import write_VESTA
    >>> write_VESTA("dspawpy_proj/dspawpy_tests/inputs/2.2/rho.json", "rho", out_filename='dspawpy_proj/dspawpy_tests/outputs/doctest/rho.cube') # doctest: +ELLIPSIS
    ==> ...dspawpy_proj/dspawpy_tests/outputs/doctest/rho.cube

    >>> from dspawpy.io.write import write_VESTA
    >>> write_VESTA(
    ...     in_filename="dspawpy_proj/dspawpy_tests/inputs/2.7/potential.h5",
    ...     data_type="potential",
    ...     out_filename="dspawpy_proj/dspawpy_tests/outputs/doctest/my_potential.txt",
    ...     subtype='TotalElectrostaticPotential', # or 'TotalLocalPotential'
    ...     format='txt',
    ...     gridsize=(50,50,50), # all integer, can be larger or less than the original gridsize
    ... ) # doctest: +ELLIPSIS
    Interpolating volumetric data...
    volumetric data interpolated
    ==> .../my_potential.txt
    >>> write_VESTA(
    ...     in_filename="dspawpy_proj/dspawpy_tests/inputs/2.8/elf.h5",
    ...     data_type="elf",
    ...     out_filename="dspawpy_proj/dspawpy_tests/outputs/doctest/elf.txt",
    ...     format='txt',
    ... ) # doctest: +ELLIPSIS
    ==> .../elf.txt
    >>> write_VESTA(
    ...     in_filename="dspawpy_proj/dspawpy_tests/inputs/2.9/pcharge.h5",
    ...     data_type="pcharge",
    ...     out_filename="dspawpy_proj/dspawpy_tests/outputs/doctest/pcharge.txt",
    ...     format='txt',
    ... ) # doctest: +ELLIPSIS
    ==> .../pcharge.txt

    >>> with open("dspawpy_proj/dspawpy_tests/outputs/doctest/my_potential.txt") as t:
    ...     contents = t.readlines()
    ...     for line in contents[:10]:
    ...         print(line.strip())
    # 2 atoms
    # 50 50 50 grid size
    # x y z value
    0.000 0.000 0.000      0.3279418
    0.055 0.055 0.000     -0.0740864
    0.110 0.110 0.000     -0.8811762
    0.165 0.165 0.000     -2.1283864
    0.220 0.220 0.000     -4.0559144
    0.275 0.275 0.000     -6.8291031
    0.330 0.330 0.000    -10.1550910
    """
    from dspawpy.io.read import load_h5
    from dspawpy.io.structure import read

    if in_filename.endswith(".h5"):
        data = load_h5(in_filename)
        structure = read(in_filename)[0]
        grid = data["/AtomInfo/Grid"]  # get grid array
        if data_type == "rho" or data_type == "rhoBound":
            vd = data["/Rho/TotalCharge"]
        elif data_type == "potential":
            if subtype is None:
                subtype = "TotalElectrostaticPotential"
            vd = data[f"/Potential/{subtype}"]
        elif data_type == "elf":
            vd = data["/ELF/TotalELF"]
        elif data_type == "pcharge":
            vd = data["/Pcharge/1/TotalCharge"]
        else:
            raise NotImplementedError(
                f"{data_type}, {subtype}, Only support rho/potential/elf/pcharge/rhoBound"
            )

    elif in_filename.endswith(".json"):
        with open(in_filename, "r") as fin:
            from json import load

            data = load(fin)
        structure = read(in_filename)[0]
        grid = data["AtomInfo"]["Grid"]  # get grid array
        if data_type == "rho" or data_type == "rhoBound":
            vd = data["Rho"]["TotalCharge"]
        elif data_type == "potential":
            if subtype is None:
                subtype = "TotalElectrostaticPotential"
            vd = data["Potential"][subtype]
        elif data_type == "elf":
            vd = data["ELF"]["TotalELF"]
        elif data_type == "pcharge":
            vd = data["Pcharge"][0]["TotalCharge"]
        else:
            raise NotImplementedError(
                f"{data_type}, {subtype}, Only support rho/potential/elf/pcharge/rhoBound"
            )

    else:
        raise NotImplementedError("Only support json/h5 format")

    _write_specific_format(
        structure,
        grid,
        vd,
        out_filename,
        gridsize,
        format=format,
        compact=compact,
        inorm=inorm,
    )


@logger.catch
def write_delta_rho_vesta(
    total: str,
    individuals: List[str],
    output: str = "delta_rho.cube",
    format: str = "cube",
    compact: bool = False,
    inorm: bool = False,
    gridsize: Optional[Sequence] = None,
):
    """电荷密度差分可视化

    DeviceStudio暂不支持大文件，临时写成可以用VESTA打开的格式

    Parameters
    ----------
    total : str
        体系总电荷密度文件路径，可以是h5或json格式
    individuals : list of str
        体系各组分电荷密度文件路径，可以是h5或json格式
    output : str
        输出文件路径，默认 "delta_rho.cube"
    format : str
        输出的数据格式，支持 "cube" 和 "vasp"，默认为 "cube"
    compact : bool
        每个格点的数据都换行，通过减少空格数量减小文件体积（不会影响VESTA软件的解析），默认为False
    inorm : bool
        是否归一化体积数据，使其总和为1，默认为False
    gridsize: tuple
        重新定义的格点数，格式为 (ngx, ngy, ngz)，默认为None，即使用原始格点数

    Returns
    -------
    output : file
        电荷差分（total-individual1-individual2-...）后的电荷密度文件，

    Examples
    --------
    >>> from dspawpy.io.write import write_delta_rho_vesta
    >>> write_delta_rho_vesta(total='dspawpy_proj/dspawpy_tests/inputs/supplement/AB.h5',
    ...     individuals=['dspawpy_proj/dspawpy_tests/inputs/supplement/A.h5', 'dspawpy_proj/dspawpy_tests/inputs/supplement/B.h5'],
    ...     output='dspawpy_proj/dspawpy_tests/outputs/doctest/delta_rho.cube') # doctest: +ELLIPSIS
    ==> ...dspawpy_proj/dspawpy_tests/outputs/doctest/delta_rho.cube
    """
    import os

    from dspawpy.io.read import load_h5
    from dspawpy.io.structure import read

    abstotal = os.path.abspath(total)
    structure = read(abstotal)[0]

    if abstotal.endswith(".h5"):
        dataAB = load_h5(abstotal)
        rho = dataAB["/Rho/TotalCharge"]
        grid = dataAB["/AtomInfo/Grid"]
    elif abstotal.endswith(".json"):
        with open(abstotal, "r") as f1:
            from json import load

            dataAB = load(f1)
            rho = dataAB["Rho"]["TotalCharge"]
            grid = dataAB["AtomInfo"]["Grid"]

    else:
        raise ValueError(f"file format must be either h5 or json: {abstotal}")

    import numpy as np

    for individual in individuals:
        absindividual = os.path.abspath(individual)
        if absindividual.endswith(".h5"):
            data_individual = load_h5(absindividual)
            rho_individual = np.array(data_individual["/Rho/TotalCharge"])
        elif absindividual.endswith(".json"):
            with open(absindividual, "r") as f2:
                from json import load

                data_individual = load(f2)
                rho_individual = np.array(data_individual["Rho"]["TotalCharge"])
        else:
            raise ValueError(f"file format must be either h5 or json: {absindividual}")

        rho -= rho_individual

    _write_specific_format(
        structure,
        grid,
        rho,
        output,
        gridsize,
        format=format,
        compact=compact,
        inorm=inorm,
    )


@logger.catch
def to_file(
    structure,
    filename: str,
    fmt: Optional[str] = None,
    coords_are_cartesian: bool = True,
):
    r"""Deprecated. Use :func:`dspawpy.io.structure.write` instead."""
    logger.warning(
        "dspawpy.io.write.to_file is deprecated"
        "Use dspawpy.io.structure.write instead.",
        DeprecationWarning,
    )
    from dspawpy.io.structure import write

    write(structure, filename, fmt, coords_are_cartesian)


@logger.catch
def _write_atoms(fileobj, structure, idirect: bool = False):
    fileobj.write("DS-PAW Structure\n")
    fileobj.write("  1.00\n")
    lattice = structure.lattice.matrix.reshape(-1, 1)
    fileobj.write(
        "%20.14f %20.14f %20.14f\n" % (lattice[0][0], lattice[1][0], lattice[2][0])
    )
    fileobj.write(
        "%20.14f %20.14f %20.14f\n" % (lattice[3][0], lattice[4][0], lattice[5][0])
    )
    fileobj.write(
        "%20.14f %20.14f %20.14f\n" % (lattice[6][0], lattice[7][0], lattice[8][0])
    )

    elements = [s.species_string for s in structure.sites]
    elements_set = []
    elements_number = {}
    for e in elements:
        if e in elements_set:
            elements_number[e] = elements_number[e] + 1
        else:
            elements_set.append(e)
            elements_number[e] = 1

    for e in elements_set:
        fileobj.write("  " + e)
    fileobj.write("\n")

    for e in elements_set:
        fileobj.write("%5d " % (elements_number[e]))
    fileobj.write("\n")
    if idirect:
        fileobj.write("Direct\n")
        for p in structure.frac_coords:
            fileobj.write("%20.14f %20.14f %20.14f\n" % (p[0], p[1], p[2]))
    else:
        fileobj.write("Cartesian\n")
        for p in structure.cart_coords:
            fileobj.write("%20.14f %20.14f %20.14f\n" % (p[0], p[1], p[2]))


@logger.catch
def _write_specific_format(
    structure,
    grid: Sequence[int],
    volumetricData: Sequence,
    filename: str,
    gridsize: Optional[Sequence[int]] = None,
    format: str = "cube",
    compact: bool = False,
    inorm: bool = False,
):
    import os

    absfile = os.path.abspath(filename)
    if os.path.isfile(absfile):
        logger.warning("%s already exists and will be overwritten!" % absfile)
    os.makedirs(os.path.dirname(absfile), exist_ok=True)

    import numpy as np

    vd = np.asarray(volumetricData)
    if inorm is True:
        vd /= np.sum(vd)

    ngx, ngy, ngz = grid
    reshaped_vd = vd.reshape(grid, order="F")  # ! dspaw output is in F order

    if gridsize is None:
        gridsize = grid
        interp_data = reshaped_vd
    else:
        oldngx = np.linspace(0, 1, ngx)
        oldngy = np.linspace(0, 1, ngy)
        oldngz = np.linspace(0, 1, ngz)
        from scipy.interpolate import RegularGridInterpolator

        rgi = RegularGridInterpolator((oldngx, oldngy, oldngz), reshaped_vd)

        print("Interpolating volumetric data...")
        newngx = np.linspace(0, 1, gridsize[0])
        newngy = np.linspace(0, 1, gridsize[1])
        newngz = np.linspace(0, 1, gridsize[2])
        X, Y, Z = np.meshgrid(newngx, newngy, newngz, indexing="ij")
        points = np.array([X.ravel(), Y.ravel(), Z.ravel()]).T
        interp_data = rgi(points).reshape(gridsize)
        print("volumetric data interpolated")

    if format.lower() == "cube":
        volume_in_Bohr3 = structure.volume / Bohr**3
        interp_data /= volume_in_Bohr3
        with open(absfile, "w") as fileobj:
            import time

            fileobj.write("Cube file written on " + time.strftime("%c"))
            fileobj.write("\nOUTER LOOP: X, MIDDLE LOOP: Y, INNER LOOP: Z\n")

            origin = np.zeros(3)
            fileobj.write(
                f"{len(structure.sites):5d} {origin[0]:12.6f} {origin[1]:12.6f} {origin[2]:12.6f}\n"
            )

            for i in range(3):
                n = gridsize[i]
                d = structure.lattice.matrix[i] / n / Bohr
                fileobj.write(f"{n:5d} {d[0]:12.6f} {d[1]:12.6f} {d[2]:12.6f}\n")

            positions = structure.cart_coords / Bohr
            species_string = [s.species_string for s in structure.sites]
            species_string = [
                s.replace("+", "").replace("-", "") for s in species_string
            ]
            symbols = "".join(species_string)  # SiH
            from dspawpy.io.utils import _symbols2numbers

            numbers = _symbols2numbers(symbols)
            for Z, (x, y, z) in zip(numbers, positions):
                fileobj.write(f"{Z:5d} {0:12.6f} {x:12.6f} {y:12.6f} {z:12.6f}\n")

            if compact:
                for ix in range(gridsize[0]):
                    for iy in range(gridsize[1]):
                        for iz in range(gridsize[2]):
                            fileobj.write(f"{interp_data[ix, iy, iz]:12.5e}\n")
            else:
                for ix in range(gridsize[0]):
                    for iy in range(gridsize[1]):
                        for iz in range(gridsize[2]):
                            fileobj.write(f"{interp_data[ix, iy, iz]:12.5e} ")
                            if iz % 6 == 5:
                                fileobj.write("\n")
                        fileobj.write("\n")

    elif format.lower() == "vesta" or format.lower() == "vasp":
        with open(absfile, "w") as file:
            _write_atoms(file, structure, idirect=True)
            file.write("%5d %5d %5d\n" % (gridsize[0], gridsize[1], gridsize[2]))
            count = 0
            if compact:
                interp_data.flatten().tofile(file, sep="\n", format="%.5e")
            else:
                for iz in range(gridsize[2]):
                    for iy in range(gridsize[1]):
                        for ix in range(gridsize[0]):
                            file.write(f"{interp_data[ix, iy, iz]:12.5e} ")
                            count += 1
                            if count % 5 == 0:
                                file.write("\n")

    elif format.lower() == "txt":
        with open(absfile, "w") as file:
            file.write(f"# {len(structure.sites)} atoms\n")
            file.write(f"# {gridsize[0]} {gridsize[1]} {gridsize[2]} grid size\n")
            file.write("# x y z value\n")
            for ix in range(gridsize[0]):
                for iy in range(gridsize[1]):
                    for iz in range(gridsize[2]):
                        matrix = structure.lattice.matrix
                        v_x = matrix[0] * ix / gridsize[0]
                        v_y = matrix[1] * iy / gridsize[1]
                        v_z = matrix[2] * iz / gridsize[2]
                        v_xyz = v_x + v_y + v_z
                        x, y, z = v_xyz
                        file.write(
                            f"{x:.3f} {y:.3f} {z:.3f} {interp_data[ix, iy, iz]:14.7f}\n"
                        )
            import time

            file.write(f"# {format} file written on {time.strftime('%c')}\n")

    else:
        raise NotImplementedError('only "cube", "vesta", "vasp", "txt" are supported.')

    print(f"==> {absfile}")


@logger.catch
def _to_dspaw_as(structure, filename: str, coords_are_cartesian: bool = True):
    """write dspaw structure file of .as type"""
    import os

    absfile = os.path.abspath(filename)
    if os.path.isfile(absfile):
        logger.warning("%s already exists and will be overwritten!" % absfile)
    os.makedirs(os.path.dirname(absfile), exist_ok=True)
    with open(absfile, "w", encoding="utf-8") as file:
        file.write("Total number of atoms\n")
        file.write("%d\n" % len(structure))

        # ^ write lattice info
        if "LatticeFixs" in structure.sites[0].properties:
            lfinfo = structure.sites[0].properties["LatticeFixs"]
            if len(lfinfo) == 3:
                file.write("Lattice Fix\n")
                formatted_fts = []
                for ft in lfinfo:
                    if ft == "True":  # True
                        ft_formatted = "T"
                    else:
                        ft_formatted = "F"
                    formatted_fts.append(ft_formatted)
                for v in structure.lattice.matrix:
                    # write each element of formatted_fts in a line without [] symbol
                    file.write(f'{v} {formatted_fts}.strip("[").strip("]")\n')
            elif len(lfinfo) == 9:
                file.write("Lattice Fix_x Fix_y Fix_z\n")
                formatted_fts = []
                for ft in lfinfo:
                    if ft == "True":  # True
                        ft_formatted = "T"
                    else:
                        ft_formatted = "F"
                    formatted_fts.append(ft_formatted)
                fix_str1 = " ".join(formatted_fts[:3])
                fix_str2 = " ".join(formatted_fts[3:6])
                fix_str3 = " ".join(formatted_fts[6:9])
                v1 = structure.lattice.matrix[0]
                v2 = structure.lattice.matrix[1]
                v3 = structure.lattice.matrix[2]
                file.write(f" {v1[0]:5.8f} {v1[1]:5.8f} {v1[2]:5.8f} {fix_str1}\n")
                file.write(f" {v2[0]:5.8f} {v2[1]:5.8f} {v2[2]:5.8f} {fix_str2}\n")
                file.write(f" {v3[0]:5.8f} {v3[1]:5.8f} {v3[2]:5.8f} {fix_str3}\n")
            else:
                raise ValueError(
                    f"LatticeFixs should be a list of 3 or 9 bools, but got {lfinfo}"
                )
        else:
            file.write("Lattice\n")
            for v in structure.lattice.matrix:
                file.write("%.8f %.8f %.8f\n" % (v[0], v[1], v[2]))

        i = 0
        for site in structure:
            keys = []
            for key in site.properties:  # site.properties is a dictionary
                if key != "LatticeFixs":
                    keys.append(key)
            keys.sort()
            keys_str = " ".join(keys)  # sth like 'magmom fix
            if i == 0:
                if coords_are_cartesian:
                    file.write(f"Cartesian {keys_str}\n")
                else:
                    file.write(f"Direct {keys_str}\n")
            i += 1

            coords = site.coords if coords_are_cartesian else site.frac_coords
            raw = []
            for sortted_key in keys:  # site.properties is a dictionary
                raw_values = site.properties[sortted_key]
                if isinstance(raw_values, list):  # single True or False
                    values = raw_values
                else:
                    values = [raw_values]
                for v in values:
                    if v == "True":
                        value_str = "T"
                    elif v == "False":
                        value_str = "F"
                    else:
                        value_str = str(v)
                    raw.append(value_str)

            final_strs = " ".join(raw)  # sth like '0.0 T
            # remove all digits and +/- symbols
            sss = ""
            for char in site.species_string:
                if not char.isdigit() and char not in ["+", "-"]:
                    sss += char
            file.write(
                "%s %.8f %.8f %.8f %s\n"
                % (
                    sss,
                    coords[0],
                    coords[1],
                    coords[2],
                    final_strs,
                )
            )
    print(f"==> {absfile}")


@logger.catch
def _to_hzw(structure, filename: str):
    """write hzw structure file of .hzw type"""
    import os

    absfile = os.path.abspath(filename)

    if os.path.isfile(absfile):
        logger.warning("%s already exists and will be overwritten!" % absfile)
    os.makedirs(os.path.dirname(absfile), exist_ok=True)
    with open(absfile, "w", encoding="utf-8") as file:
        file.write("% The number of probes \n")
        file.write("0\n")
        file.write("% Uni-cell vector\n")

        for v in structure.lattice.matrix:
            file.write("%.6f %.6f %.6f\n" % (v[0], v[1], v[2]))

        file.write("% Total number of device_structure\n")
        file.write("%d\n" % len(structure))
        file.write("% Atom site\n")

        for site in structure:
            file.write(
                "%s %.6f %.6f %.6f\n"
                % (site.species_string, site.coords[0], site.coords[1], site.coords[2])
            )
    print(f"==> {absfile}")


@logger.catch
def _to_dspaw_json(structure, filename: str, coords_are_cartesian: bool = True):
    """write dspaw structure file of .json type"""
    import os

    absfile = os.path.abspath(filename)
    lattice = structure.lattice.matrix.flatten().tolist()
    atoms = []
    for site in structure:
        coords = site.coords if coords_are_cartesian else site.frac_coords
        atoms.append({"Element": site.species_string, "Position": coords.tolist()})

    coordinate_type = "Cartesian" if coords_are_cartesian else "Direct"
    d = {"Lattice": lattice, "CoordinateType": coordinate_type, "Atoms": atoms}
    if os.path.isfile(absfile):
        logger.warning("%s already exists and will be overwritten!" % absfile)
    os.makedirs(os.path.dirname(absfile), exist_ok=True)
    with open(absfile, "w", encoding="utf-8") as file:
        from json import dump

        dump(d, file, indent=4)
    print(f"==> {absfile}")


@logger.catch
def _to_pdb(structures, filename: str):
    """write pdb structure file of .pdb type"""
    import os

    absfile = os.path.abspath(filename)
    if not isinstance(structures, list):
        structures = [structures]
    if os.path.isfile(absfile):
        logger.warning("%s already exists and will be overwritten!" % absfile)
    os.makedirs(os.path.dirname(absfile), exist_ok=True)
    with open(absfile, "w", encoding="utf-8") as file:
        for i, s in enumerate(structures):
            file.write("MODEL         %d\n" % (i + 1))
            file.write("REMARK   Converted from Structures\n")
            file.write("REMARK   Converted using dspawpy\n")
            # may lack lattice info
            if hasattr(s, "lattice"):
                lengths = s.lattice.lengths
                angles = s.lattice.angles
                file.write(
                    "CRYST1{0:9.3f}{1:9.3f}{2:9.3f}{3:7.2f}{4:7.2f}{5:7.2f}\n".format(
                        lengths[0],
                        lengths[1],
                        lengths[2],
                        angles[0],
                        angles[1],
                        angles[2],
                    )
                )
            for j, site in enumerate(s):
                file.write(
                    "%4s%7d%4s%5s%6d%4s%8.3f%8.3f%8.3f%6.2f%6.2f%12s\n"
                    % (
                        "ATOM",
                        j + 1,
                        site.species_string,
                        "MOL",
                        1,
                        "    ",
                        site.coords[0],
                        site.coords[1],
                        site.coords[2],
                        1.0,
                        0.0,
                        site.species_string,
                    )
                )
            file.write("TER\n")
            file.write("ENDMDL\n")

    print(f"==> {absfile}")
