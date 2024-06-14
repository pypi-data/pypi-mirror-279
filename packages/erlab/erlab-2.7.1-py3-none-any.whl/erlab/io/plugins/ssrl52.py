"""Data loader for beamline 5-2 at SSRL."""

import datetime
import os
import re
from typing import ClassVar

import h5netcdf
import numpy as np
import pandas as pd
import xarray as xr

import erlab.io.utils
from erlab.io.dataloader import LoaderBase


class SSRL52Loader(LoaderBase):
    name = "ssrl"
    aliases = ("ssrl52", "bl5-2")

    name_map: ClassVar[dict] = {
        "eV": ["Kinetic Energy", "Binding Energy"],
        "alpha": "ThetaX",
        "beta": ["ThetaY", "YDeflection", "DeflectionY"],
        "delta": ["A", "a"],  # azi
        "chi": ["T", "t"],  # polar
        "xi": ["F", "f"],  # tilt
        "x": "X",
        "y": "Y",
        "z": "Z",
        "hv": ["BL_energy", "BL_photon_energy"],
        "temp_sample": ["TB", "sample_stage_temperature"],
        "sample_workfunction": "WorkFunction",
    }

    coordinate_attrs = ("beta", "delta", "chi", "xi", "hv", "x", "y", "z")

    additional_attrs: ClassVar[dict] = {
        "configuration": 3,
        "sample_workfunction": 4.5,
    }

    always_single: bool = True
    skip_validate: bool = True

    @property
    def file_dialog_methods(self):
        return {"SSRL BL5-2 Raw Data (*.h5)": (self.load, {})}

    def load_single(self, file_path: str | os.PathLike) -> xr.DataArray:
        with h5netcdf.File(file_path, mode="r", phony_dims="sort") as ncf:
            attrs = dict(ncf.attrs)
            compat_mode = "data" in ncf.groups  # Compatibility with older data
            for k, v in ncf.groups.items():
                ds = xr.open_dataset(xr.backends.H5NetCDFStore(v, autoclose=True))

                if k.casefold() == "Beamline".casefold():
                    attrs[k] = ds.attrs
                    hv = ds.attrs.get("energy", None)
                    hv = ds.attrs.get("photon_energy", hv)
                    if hv is not None:
                        attrs["hv"] = hv

                    attrs["polarization"] = ds.attrs.get("polarization")

                else:
                    # Merge group attributes
                    attrs = attrs | ds.attrs

                if k.casefold() == "Data".casefold():
                    if compat_mode:
                        if "exposure" in ds.variables:
                            ds = ds.rename_vars(counts="spectrum", exposure="time")
                        else:
                            ds = ds.rename_vars(counts="spectrum")
                    elif "Time" in ds.variables:
                        ds = ds.rename_vars(Count="spectrum", Time="time")
                    else:
                        ds = ds.rename_vars(Count="spectrum")

                    # List of dicts containing scale and label info for each axis
                    axes: list[dict[str, float | int | str]] = [
                        dict(v.groups[g].attrs) for g in v.groups
                    ]

                    for i, ax in enumerate(axes):
                        # Unify case for compatibility with old data
                        axes[i] = {name.lower(): val for name, val in ax.items()}

                    # Apply dim labels
                    data = ds.rename_dims(
                        {f"phony_dim_{i}": ax["label"] for i, ax in enumerate(axes)}
                    ).load()

                    # Apply coordinates
                    is_hvdep: bool = False
                    for i, ax in enumerate(axes):
                        if compat_mode:
                            cnt = v.dimensions[f"phony_dim_{i}"].size
                        else:
                            cnt = int(ax["count"])

                        if (
                            isinstance(ax["offset"], str)
                            and ax["label"] == "Kinetic Energy"
                        ):
                            is_hvdep = True
                            # For hv dep scans, EKin is given for each scan
                            data = data.rename({ax["label"]: "Binding Energy"})
                            ax["label"] = "Binding Energy"
                            # ax['offset'] will be something like "MapInfo:Data:Axes0:Offset"
                            seg: str = ax["offset"][8:]
                            # Take first kinetic energy
                            offset = np.array(ncf["MapInfo"][seg])[0]

                            if isinstance(ax["delta"], str):
                                delta = np.array(ncf["MapInfo"][ax["delta"][8:]])
                                # may be ~1e-8 difference between values
                                delta = np.mean(delta)
                            else:
                                delta = float(ax["delta"])

                        else:
                            offset = float(ax["offset"])
                            delta = float(ax["delta"])

                        mn, mx = (offset, offset + (cnt - 1) * delta)
                        coord = np.linspace(mn, mx, cnt)

                        if len(data[ax["label"]]) != cnt:
                            # For premature data
                            coord = coord[: len(data[ax["label"]])]

                        data = data.assign_coords({ax["label"]: coord})

        if is_hvdep:
            data = data.rename(energy="hv")

        if "time" in data.variables:
            # Normalize by dwell time
            data = data["spectrum"] / data["time"]
        else:
            data = data["spectrum"]

        data = data.assign_attrs(attrs)
        return self.process_keys(data)

    def identify(
        self,
        num: int,
        data_dir: str | os.PathLike,
        zap: bool = False,
    ):
        if zap:
            target_files = erlab.io.utils.get_files(
                data_dir, extensions=(".h5",), contains="zap"
            )
        else:
            target_files = erlab.io.utils.get_files(
                data_dir, extensions=(".h5",), notcontains="zap"
            )

        for file in target_files:
            match = re.match(r"(.*?)_" + str(num).zfill(4) + r".h5", file)
            if match is not None:
                return [file], {}

        raise FileNotFoundError(f"No files found for scan {num} in {data_dir}")

    # def post_process(
    #     self, data: xr.DataArray | xr.Dataset
    # ) -> xr.DataArray | xr.Dataset:
    #     data = super().post_process(data)

    #     if "eV" in data.coords:
    #         data = data.assign_coords(eV=-data.eV.values)

    #     return data

    def load_zap(self, identifier, data_dir):
        return self.load(identifier, data_dir, zap=True)

    def generate_summary(
        self, data_dir: str | os.PathLike, exclude_zap: bool = False
    ) -> pd.DataFrame:
        files: dict[str, str] = {}

        if exclude_zap:
            target_files = erlab.io.utils.get_files(
                data_dir, extensions=(".h5",), notcontains="zap"
            )
        else:
            target_files = erlab.io.utils.get_files(data_dir, extensions=(".h5",))

        for pth in target_files:
            base_name = os.path.splitext(os.path.basename(pth))[0]
            files[base_name] = pth

        summary_attrs: dict[str, str] = {
            "Type": "Description",
            "Lens Mode": "LensModeName",
            "Region": "RegionName",
            "T(K)": "temp_sample",
            "Pass E": "PassEnergy",
            "Polarization": "polarization",
            "hv": "hv",
            # "Entrance Slit": "Entrance Slit",
            # "Exit Slit": "Exit Slit",
            "x": "x",
            "y": "y",
            "z": "z",
            "polar": "chi",
            "tilt": "xi",
            "azi": "delta",
            "DA": "beta",
        }

        cols = ["File Name", "Path", "Time", *summary_attrs.keys()]

        data_info = []

        for name, path in files.items():
            data = self.load(path)

            data_info.append(
                [
                    name,
                    path,
                    datetime.datetime.fromtimestamp(data.attrs["CreationTimeStamp"]),
                ]
            )

            for k, v in summary_attrs.items():
                try:
                    val = data.attrs[v]
                except KeyError:
                    try:
                        val = data.coords[v].values
                        if val.size == 1:
                            val = val.item()
                    except KeyError:
                        val = ""

                if k == "Pass E":
                    val = round(val)

                elif k == "Polarization":
                    if np.iterable(val):
                        val = np.round(np.asarray(val), 3).astype(float)
                    else:
                        val = [float(np.round(val, 3))]
                    val = [
                        {0.0: "LH", 0.5: "LV", 0.25: "RC", -0.25: "LC"}.get(v, v)
                        for v in val
                    ]

                    if len(val) == 1:
                        val = val[0]

                data_info[-1].append(val)

            del data

        return (
            pd.DataFrame(data_info, columns=cols)
            .sort_values("Time")
            .set_index("File Name")
        )
