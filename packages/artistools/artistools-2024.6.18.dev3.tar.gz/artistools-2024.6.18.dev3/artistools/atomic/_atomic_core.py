from collections import namedtuple
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

import artistools as at


def parse_adata(fadata, phixsdict, ionlist):
    """Generate ions and their level lists from adata.txt."""
    firstlevelnumber = 1

    for line in fadata:
        if not line.strip():
            continue

        ionheader = line.split()
        Z = int(ionheader[0])
        ion_stage = int(ionheader[1])
        level_count = int(ionheader[2])
        ionisation_energy_ev = float(ionheader[3])

        if not ionlist or (Z, ion_stage) in ionlist:
            level_list = []
            for levelindex in range(level_count):
                row = fadata.readline().split()

                levelname = " ".join(row[4:]).strip("'") if len(row) >= 5 else None
                numberin = int(row[0])
                assert levelindex == numberin - firstlevelnumber
                phixstargetlist, phixstable = phixsdict.get((Z, ion_stage, numberin), ([], []))

                level_list.append((float(row[1]), float(row[2]), int(row[3]), levelname, phixstargetlist, phixstable))

            dflevels = pd.DataFrame(
                level_list, columns=["energy_ev", "g", "transition_count", "levelname", "phixstargetlist", "phixstable"]
            )

            yield Z, ion_stage, level_count, ionisation_energy_ev, dflevels

        else:
            for _ in range(level_count):
                fadata.readline()


def parse_transitiondata(ftransitions, ionlist):
    firstlevelnumber = 1

    for line in ftransitions:
        if not line.strip():
            continue

        ionheader = line.split()
        Z = int(ionheader[0])
        ion_stage = int(ionheader[1])
        transition_count = int(ionheader[2])

        if not ionlist or (Z, ion_stage) in ionlist:
            translist = []
            for _ in range(transition_count):
                row = ftransitions.readline().split()
                translist.append((
                    int(row[0]) - firstlevelnumber,
                    int(row[1]) - firstlevelnumber,
                    float(row[2]),
                    float(row[3]),
                    int(row[4]) == 1 if len(row) >= 5 else 0,
                ))

            yield Z, ion_stage, pd.DataFrame(translist, columns=["lower", "upper", "A", "collstr", "forbidden"])
        else:
            for _ in range(transition_count):
                ftransitions.readline()


def parse_phixsdata(fphixs, ionlist):
    firstlevelnumber = 1
    nphixspoints = int(fphixs.readline())
    phixsnuincrement = float(fphixs.readline())

    xgrid = np.linspace(1.0, 1.0 + phixsnuincrement * (nphixspoints + 1), num=nphixspoints + 1, endpoint=False)

    for line in fphixs:
        if not line.strip():
            continue

        ionheader = line.split()
        Z = int(ionheader[0])
        upperion_stage = int(ionheader[1])
        upperionlevel = int(ionheader[2]) - firstlevelnumber
        lowerion_stage = int(ionheader[3])
        lowerionlevel = int(ionheader[4]) - firstlevelnumber
        # threshold_ev = float(ionheader[5])

        assert upperion_stage == lowerion_stage + 1

        if upperionlevel >= 0:
            targetlist = [(upperionlevel, 1.0)]
        else:
            targetlist = []
            ntargets = int(fphixs.readline())
            for _ in range(ntargets):
                level, fraction = fphixs.readline().split()
                targetlist.append((int(level) - firstlevelnumber, float(fraction)))

        if not ionlist or (Z, lowerion_stage) in ionlist:
            phixslist = [float(fphixs.readline()) * 1e-18 for _ in range(nphixspoints)]
            phixstable = np.array(list(zip(xgrid, phixslist, strict=False)))

            yield Z, upperion_stage, upperionlevel, lowerion_stage, lowerionlevel, targetlist, phixstable

        else:
            for _ in range(nphixspoints):
                fphixs.readline()


@lru_cache(maxsize=8)
def get_levels(
    modelpath, ionlist=None, get_transitions: bool = False, get_photoionisations: bool = False, quiet: bool = False
) -> pd.DataFrame:
    """Return a pandas DataFrame of energy levels."""
    adatafilename = Path(modelpath, "adata.txt")

    transitionsdict = {}
    if get_transitions:
        transition_filename = Path(modelpath, "transitiondata.txt")
        if not quiet:
            print(f"Reading {transition_filename.relative_to(Path(modelpath).parent)}")
        with at.zopen(transition_filename) as ftransitions:
            transitionsdict = {
                (Z, ion_stage): dftransitions
                for Z, ion_stage, dftransitions in parse_transitiondata(ftransitions, ionlist)
            }

    phixsdict = {}
    if get_photoionisations:
        phixs_filename = Path(modelpath, "phixsdata_v2.txt")

        if not quiet:
            print(f"Reading {phixs_filename.relative_to(Path(modelpath).parent)}")
        with at.zopen(phixs_filename) as fphixs:
            for (
                Z,
                _upperion_stage,
                _upperionlevel,
                lowerion_stage,
                lowerionlevel,
                phixstargetlist,
                phixstable,
            ) in parse_phixsdata(fphixs, ionlist):
                phixsdict[(Z, lowerion_stage, lowerionlevel)] = (phixstargetlist, phixstable)

    level_lists = []
    iontuple = namedtuple("iontuple", "Z ion_stage level_count ion_pot levels transitions")

    with at.zopen(adatafilename) as fadata:
        if not quiet:
            print(f"Reading {adatafilename.relative_to(Path(modelpath).parent)}")

        for Z, ion_stage, level_count, ionisation_energy_ev, dflevels in parse_adata(fadata, phixsdict, ionlist):
            translist = transitionsdict.get((Z, ion_stage), pd.DataFrame())
            level_lists.append(iontuple(Z, ion_stage, level_count, ionisation_energy_ev, dflevels, translist))

    return pd.DataFrame(level_lists)


def parse_recombratefile(frecomb):
    for line in frecomb:
        Z, upper_ion_stage, t_count = (int(x) for x in line.split())
        arr_log10t = []
        arr_rrc_low_n = []
        arr_rrc_total = []
        for _ in range(int(t_count)):
            log10t, rrc_low_n, rrc_total = (float(x) for x in frecomb.readline().split())

            arr_log10t.append(log10t)
            arr_rrc_low_n.append(rrc_low_n)
            arr_rrc_total.append(rrc_total)

        recombdata_thision = pd.DataFrame({
            "log10T_e": arr_log10t,
            "rrc_low_n": arr_rrc_low_n,
            "rrc_total": arr_rrc_total,
        })

        recombdata_thision = recombdata_thision.eval("T_e = 10 ** log10T_e")

        yield Z, upper_ion_stage, recombdata_thision


@lru_cache(maxsize=4)
def get_ionrecombratecalibration(modelpath):
    """Read recombrates file."""
    recombdata = {}
    with Path(modelpath, "recombrates.txt").open("r", encoding="utf-8") as frecomb:
        for Z, upper_ion_stage, dfrrc in parse_recombratefile(frecomb):
            recombdata[(Z, upper_ion_stage)] = dfrrc

    return recombdata
