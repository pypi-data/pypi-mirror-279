# Can't use xarray, as TRANSP has a variable called X which itself has a dimension called X
import netCDF4 as nc
import numpy as np

from ..constants import deuterium_mass, electron_mass, hydrogen_mass
from ..file_utils import FileReader
from ..species import Species
from ..typing import PathLike
from ..units import UnitSpline
from ..units import ureg as units
from .kinetics import Kinetics


class KineticsReaderTRANSP(FileReader, file_type="TRANSP", reads=Kinetics):
    def read_from_file(
        self, filename: PathLike, time_index: int = -1, time: float = None
    ) -> Kinetics:
        """
        Reads in TRANSP profiles NetCDF file
        """
        # Open data file, get generic data
        with nc.Dataset(filename) as kinetics_data:
            time_cdf = kinetics_data["TIME3"][:]

            if time_index != -1 and time is not None:
                raise ValueError("Cannot set both `time` and `time_index`")

            if time is not None:
                time_index = np.argmin(np.abs(time_cdf - time))

            psi = kinetics_data["PLFLX"][time_index, :].data
            psi = psi - psi[0]
            psi_n = psi / psi[-1] * units.dimensionless

            unit_charge_array = np.ones(len(psi_n))

            rho = kinetics_data["RMNMP"][time_index, :].data
            rho = rho / rho[-1] * units.lref_minor_radius

            rho_func = UnitSpline(psi_n, rho)

            electron_temp_data = kinetics_data["TE"][time_index, :].data * units.eV
            electron_temp_func = UnitSpline(psi_n, electron_temp_data)

            electron_dens_data = (
                kinetics_data["NE"][time_index, :].data * 1e6 * units.meter**-3
            )
            electron_dens_func = UnitSpline(psi_n, electron_dens_data)

            if "OMEG_VTR" in kinetics_data.variables.keys():
                omega_data = (
                    kinetics_data["OMEG_VTR"][time_index, :].data * units.second**-1
                )
            elif "OMEGA" in kinetics_data.variables.keys():
                omega_data = (
                    kinetics_data["OMEGA"][time_index, :].data * units.second**-1
                )
            else:
                omega_data = electron_dens_data.m * 0.0 * units.second**-1

            omega_func = UnitSpline(psi_n, omega_data)

            electron_charge = UnitSpline(
                psi_n, -1 * unit_charge_array * units.elementary_charge
            )

            electron = Species(
                species_type="electron",
                charge=electron_charge,
                mass=electron_mass,
                dens=electron_dens_func,
                temp=electron_temp_func,
                omega0=omega_func,
                rho=rho_func,
            )

            result = {"electron": electron}

            # TRANSP only has one ion temp
            ion_temp_data = kinetics_data["TI"][time_index, :].data * units.eV
            ion_temp_func = UnitSpline(psi_n, ion_temp_data)

            # Go through each species output in TRANSP
            try:
                impurity_charge = int(kinetics_data["XZIMP"][time_index].data)
                impurity_mass = (
                    int(kinetics_data["AIMP"][time_index].data) * hydrogen_mass
                )
            except IndexError:
                impurity_charge = 0 * units.elementary_charge
                impurity_mass = 0 * units.kg

            possible_species = [
                {
                    "species_name": "deuterium",
                    "transp_name": "ND",
                    "charge": UnitSpline(
                        psi_n, 1 * unit_charge_array * units.elementary_charge
                    ),
                    "mass": deuterium_mass,
                },
                {
                    "species_name": "tritium",
                    "transp_name": "NT",
                    "charge": UnitSpline(
                        psi_n, 1 * unit_charge_array * units.elementary_charge
                    ),
                    "mass": 1.5 * deuterium_mass,
                },
                {
                    "species_name": "helium",
                    "transp_name": "NI4",
                    "charge": UnitSpline(
                        psi_n, 2 * unit_charge_array * units.elementary_charge
                    ),
                    "mass": 4 * hydrogen_mass,
                },
                {
                    "species_name": "helium3",
                    "transp_name": "NI4",
                    "charge": UnitSpline(
                        psi_n, 2 * unit_charge_array * units.elementary_charge
                    ),
                    "mass": 3 * hydrogen_mass,
                },
                {
                    "species_name": "impurity",
                    "transp_name": "NIMP",
                    "charge": UnitSpline(
                        psi_n,
                        impurity_charge * unit_charge_array * units.elementary_charge,
                    ),
                    "mass": impurity_mass,
                },
            ]

            for species in possible_species:
                if species["transp_name"] not in kinetics_data.variables:
                    continue

                density_data = (
                    kinetics_data[species["transp_name"]][time_index, :].data
                    * 1e6
                    * units.meter**-3
                )
                density_func = UnitSpline(psi_n, density_data)

                result[species["species_name"]] = Species(
                    species_type=species["species_name"],
                    charge=species["charge"],
                    mass=species["mass"],
                    dens=density_func,
                    temp=ion_temp_func,
                    omega0=omega_func,
                    rho=rho_func,
                )

            return Kinetics(kinetics_type="TRANSP", **result)

    def verify_file_type(self, filename: PathLike) -> None:
        """Quickly verify that we're looking at a TRANSP file without processing"""
        # Try opening data file
        # If it doesn't exist or isn't netcdf, this will fail
        try:
            data = nc.Dataset(filename)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"KineticsReaderTRANSP could not find {filename}"
            ) from e
        except OSError as e:
            raise ValueError(
                f"KineticsReaderTRANSP must be provided a NetCDF, was given {filename}"
            ) from e
        # Given it is a netcdf, check it has the attribute TRANSP_version
        try:
            data.TRANSP_version
        except AttributeError:
            # Failing this, check for expected data_vars
            var_names = ["TIME3", "PLFLX", "RMNMP", "TE", "TI", "NE"]
            if not np.all(np.isin(var_names, list(data.variables))):
                raise ValueError(
                    f"KineticsReaderTRANSP was provided an invalid NetCDF: {filename}"
                )
        finally:
            data.close()
