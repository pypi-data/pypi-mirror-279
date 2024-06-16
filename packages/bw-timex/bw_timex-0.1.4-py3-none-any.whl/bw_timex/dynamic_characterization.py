import json
import os
import warnings
from collections.abc import Collection
from datetime import datetime
from typing import Callable, List, Optional, Tuple, Union

import bw2data as bd
import numpy as np
import pandas as pd


class DynamicCharacterization:
    """
    This class calculates dynamic characterization of life cycle inventories with temporal information.

    """

    def __init__(
        self,
        dynamic_inventory_df: pd.DataFrame,
        activity_dict: dict,
        biosphere_dict: dict,
        activity_time_mapping_dict_reversed: dict,
        biosphere_time_mapping_dict_reversed: dict,
        demand_timing_dict: dict,
        temporal_grouping: dict,
        method: tuple,
        characterization_function_dict: dict = None,
    ):
        """
        Initializes the DynamicCharacterization object. In case users don't provide own dynamic characterization functions, it adds dynamic characterization functions for the GHGs mentioned in the
        IPCC AR6 Chapter 7, if these GHG are also characterized in the selected static LCA method.

        Parameters
        ----------
        dynamic_inventory_df : pd.DataFrame
            Dynamic inventory, formatted as a DataFrame, which contains the timing, id and amount of emissions and the emitting activity.
        activity_dict : dict
            Dictionary mapping activity ids to their matrix index
        biosphere_dict : dict
            Dictionary mapping biosphere flow ids to their matrix index
        activity_time_mapping_dict_reversed : dict
            Reversed `activity_time_mapping_dict`: {time_mapping_id: ((('database', 'code'), datetime_as_integer)}
        biosphere_time_mapping_dict_reversed : dict
            Reversed `biosphere_time_mapping_dict`: {time_mapping_id: ((('database', 'code'), datetime_as_integer)}
        demand_timing_dict : dict
            A dictionary mapping the demand(s) to its timing
        temporal_grouping : str
            A string indicating the temporal grouping of the processes, e.g. 'year', 'month', 'day', 'hour'
        method : tuple
            Tuple of the selcted the LCIA method, e.g. `("EF v3.1", "climate change", "global warming potential (GWP100)")`
        characterization_function_dict : dict, optional
            A dictionary mapping biosphere flow ids to user-provided dynamic characterization functions, by default None.

        Returns
        -------
        None

        """
        self.dynamic_inventory_df = dynamic_inventory_df
        self.activity_dict = activity_dict
        self.biosphere_dict = biosphere_dict
        self.activity_time_mapping_dict_reversed = activity_time_mapping_dict_reversed
        self.biosphere_time_mapping_dict_reversed = biosphere_time_mapping_dict_reversed
        self.demand_timing_dict = demand_timing_dict
        self.temporal_grouping = temporal_grouping
        self.method = method

        if not characterization_function_dict:
            warnings.warn(
                f"No custom dynamic characterization functions provided. Using default dynamic characterization functions based on IPCC AR6 meant to work with biosphere3 flows. The flows that are characterized are based on the selection of the initially chosen impact category: {self.method}. You can look up the mapping in the bw_timex.dynamic_characterizer.characterization_function_dict."
            )
            self.add_default_characterization_functions()

        else:
            self.characterization_function_dict = characterization_function_dict  # user-provided characterization functions

    def characterize_dynamic_inventory(
        self,
        metric: (
            str | None
        ) = "GWP",  # available metrics are "radiative_forcing" and "GWP", defaulting to GWP
        time_horizon: int | None = 100,
        fixed_time_horizon: bool | None = False,
        cumsum: bool | None = True,
    ) -> Tuple[pd.DataFrame, str, bool, int]:
        """
        Characterizes the dynamic inventory, formatted as a Dataframe, by evaluating each emission (row in DataFrame) using given dynamic characterization functions.

        Available metrics are radiative forcing [W/m2] and GWP [kg CO2eq], defaulting to `radiative_forcing`.

        The `characterization_functions` are already created during __init__ and stored in the dictionary `DynamicCharacterization.characterization_function_dict`.
        In this method, they are applied to each row of the timeline-DataFrame for the duration of `time_horizon`, defaulting to 100 years.
        The `fixed_time_horizon` parameter determines whether the evaluation time horizon for all emissions is calculated from the
        functional unit (`fixed_time_horizon=True`), regardless of when the actual emission occurs, or from the time of the emission itself(`fixed_time_horizon=False`).
        The former is the implementation of the Levasseur approach (https://doi.org/10.1021/es9030003), while the latter is how conventional LCA is done.
        The Levasseur approach means that earlier emissions are characterized for a longer time period than later emissions.

        Parameters
        ----------
        metric : str, optional
            the metric for which the dynamic LCIA should be calculated. Default is "GWP". Available: "GWP" and "radiative_forcing"
        time_horizon: int, optional
            the time horizon for the dynamic characterization. Default is 100 years.
        fixed_time_horizon: bool, optional
            If True, the time horizon is calculated from the time of the functional unit (FU) instead of the time of emission. Default is False.
        cumsum: bool, optional
            whether to calculate the cumulative sum of the characterization results. Default is True.

        Returns
        -------
        pd.DataFrame
            characterized dynamic inventory
        """

        if metric not in {"radiative_forcing", "GWP"}:
            raise ValueError(
                f"Metric must be either 'radiative_forcing' or 'GWP', not {metric}"
            )

        if metric == "GWP":
            warnings.warn(
                "Using bw_timex's default CO2 characterization function for GWP reference."
            )

        time_res_dict = {
            "year": "%Y",
            "month": "%Y%m",
            "day": "%Y%m%d",
            "hour": "%Y%m%d%M",
        }

        self.characterized_inventory = pd.DataFrame()

        for _, row in self.dynamic_inventory_df.iterrows():

            if (
                row.flow not in self.characterization_function_dict.keys()
            ):  # skip uncharacterized biosphere flows
                continue

            if metric == "radiative_forcing":  # radiative forcing in W/m2

                if (
                    not fixed_time_horizon
                ):  # fixed_time_horizon = False: conventional approach, emission is calculated from t emission for the length of time horizon
                    self.characterized_inventory = pd.concat(
                        [
                            self.characterized_inventory,
                            self.characterization_function_dict[
                                row.flow
                            ](  # here the dynamic characterization function is called and applied to the emission of the row
                                row,
                                period=time_horizon,
                            ),
                        ]
                    )

                else:  # fixed_time_horizon = True: Levasseur approach: time_horizon for all emissions starts at timing of FU + time_horizon
                    # e.g. an emission occuring n years before FU is characterized for time_horizon+n years
                    timing_FU = [value for value in self.demand_timing_dict.values()]
                    end_TH_FU_list = [x + time_horizon for x in timing_FU]

                    if len(end_TH_FU_list) > 1:
                        warnings.warn(
                            f"There are multiple functional units with different timings. The first one ({str(end_TH_FU_list[0])}) will be used as a basis for the fixed time horizon in dynamic characterization."
                        )

                    end_TH_FU = datetime.strptime(
                        str(end_TH_FU_list[0]), time_res_dict[self.temporal_grouping]
                    )

                    timing_emission = (
                        row.date.to_pydatetime()
                    )  # convert 'pandas._libs.tslibs.timestamps.Timestamp' to datetime object
                    new_TH = round(
                        (end_TH_FU - timing_emission).days / 365.25
                    )  # time difference in integer years between emission timing and end of time horizon of FU

                    self.characterized_inventory = pd.concat(
                        [
                            self.characterized_inventory,
                            self.characterization_function_dict[row.flow](
                                row,
                                period=new_TH,
                            ),
                        ]
                    )

            if metric == "GWP":  # scale radiative forcing to GWP [kg CO2 equivalent]
                if (
                    not fixed_time_horizon
                ):  # fixed_time_horizon = False: conventional approach, emission is calculated from t emission for the length of time_horizon

                    radiative_forcing_ghg = self.characterization_function_dict[
                        row.flow
                    ](
                        row,
                        period=time_horizon,
                    )

                    row["amount"] = 1  # convert 1 kg CO2 equ.
                    radiative_forcing_co2 = characterize_co2(row, period=time_horizon)

                    ghg_integral = radiative_forcing_ghg["amount"].sum()
                    co2_integral = radiative_forcing_co2["amount"].sum()
                    co2_equiv = ghg_integral / co2_integral

                    row_data = {
                        "date": radiative_forcing_ghg.loc[
                            0, "date"
                        ],  # start date of emission
                        "amount": co2_equiv,  # ghg emission in kg CO2-equ
                        "flow": radiative_forcing_ghg.loc[0, "flow"],
                        "activity": radiative_forcing_ghg.loc[0, "activity"],
                    }

                    row_df = pd.DataFrame([row_data])
                    self.characterized_inventory = pd.concat(
                        [self.characterized_inventory, row_df], ignore_index=True
                    )

                else:  # fixed_time_horizon = True: Levasseur approach: time_horizon for all emissions starts at timing of FU + time_horizon
                    # e.g. an emission occuring n years before FU is characterized for time_horizon+n years
                    timing_FU = [value for value in self.demand_timing_dict.values()]
                    end_TH_FU_list = [x + time_horizon for x in timing_FU]

                    if len(end_TH_FU_list) > 1:
                        warnings.warn(
                            f"There are multiple functional units with different timings. The first one ({str(end_TH_FU_list[0])}) will be used as a basis for the fixed time horizon in dynamic characterization."
                        )

                    end_TH_FU = datetime.strptime(
                        str(end_TH_FU_list[0]), time_res_dict[self.temporal_grouping]
                    )

                    timing_emission = row.date.to_pydatetime()
                    new_TH = round(
                        (end_TH_FU - timing_emission).days / 365.25
                    )  # time difference in integer years between emission timing and end of TH of FU

                    radiative_forcing_ghg = self.characterization_function_dict[
                        row.flow
                    ](
                        row,
                        period=new_TH,
                    )  # indidvidual emissions are calculated for t_emission until t_FU + time_horizon

                    row["amount"] = 1  # convert 1 kg CO2 equ.
                    radiative_forcing_co2 = characterize_co2(
                        row, period=time_horizon
                    )  # reference substance CO2 is calculated for length of time horizon!

                    ghg_integral = radiative_forcing_ghg["amount"].sum()
                    co2_integral = radiative_forcing_co2["amount"].sum()
                    co2_equiv = ghg_integral / co2_integral

                    row_data = {
                        "date": radiative_forcing_ghg.loc[
                            0, "date"
                        ],  # start date of emission
                        "amount": co2_equiv,  # ghg emission in CO2 equiv
                        "flow": radiative_forcing_ghg.loc[0, "flow"],
                        "activity": radiative_forcing_ghg.loc[0, "activity"],
                    }
                    row_df = pd.DataFrame([row_data])
                    self.characterized_inventory = pd.concat(
                        [self.characterized_inventory, row_df], ignore_index=True
                    )

            # sort by date
            if "date" in self.characterized_inventory:
                self.characterized_inventory.sort_values(
                    by="date", ascending=True, inplace=True
                )
                self.characterized_inventory.reset_index(drop=True, inplace=True)

            if cumsum and "amount" in self.characterized_inventory:
                self.characterized_inventory["amount_sum"] = (
                    self.characterized_inventory["amount"].cumsum()
                )  # TODO: there is also an option for cumulative results in the characterization functions themselves. Rethink where this is handled best and to avoid double cumsum

        if self.characterized_inventory.empty:
            raise ValueError(
                "There are no flows to characterize. Please make sure your time horizon matches the timing of emissions and make sure there are characterization functions for the flows in the dynamic inventories."
            )

        # remove rows with zero amounts to make it more readable
        self.characterized_inventory = self.characterized_inventory[
            self.characterized_inventory["amount"] != 0
        ]

        # add meta data and reorder
        self.characterized_inventory["activity_name"] = self.characterized_inventory[
            "activity"
        ].map(lambda x: self.activity_time_mapping_dict_reversed.get(x)[0])

        self.characterized_inventory["flow_name"] = self.characterized_inventory[
            "flow"
        ].apply(lambda x: bd.get_node(id=x)["name"])

        self.characterized_inventory = self.characterized_inventory[
            [
                "date",
                "amount",
                "flow",
                "flow_name",
                "activity",
                "activity_name",
                "amount_sum",
            ]
        ]
        self.characterized_inventory.reset_index(drop=True, inplace=True)
        self.characterized_inventory.sort_values(
            by="date", ascending=True, inplace=True
        )

        return self.characterized_inventory

    def add_default_characterization_functions(self):
        """
        Add default dynamic characterization functions for CO2, CH4, N2O and other GHGs, based on IPCC AR6 Chapter 7 decay curves.

        Please note: Currently, only CO2, CH4 and N2O include climate-carbon feedbacks.

        This has not yet been added for other GHGs. Refer to https://esd.copernicus.org/articles/8/235/2017/esd-8-235-2017.html"
        "Methane, non-fossil" is currently also excluded from the default characterization functions, as it has a different static CF than fossil methane and we need to check the correct value (#TODO)

        Parameters
        ----------
        None

        Returns
        -------
        None but adds default dynamic characterization functions to the `characterization_function_dict` attribute of the DynamicCharacterization object.

        """
        self.characterization_function_dict = dict()

        # load pre-calculated decay multipliers for GHGs (except for CO2, CH4, N2O & CO)
        filepath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data", "decay_multipliers.json"
        )

        with open(filepath) as json_file:
            decay_multipliers = json.load(json_file)

        # look up which GHGs are characterized in the selected static LCA method
        method_data = bd.Method(self.method).load()

        # the bioflow-identifier stored in the method data can be the database id or the tuple (database, code)
        def get_bioflow_node(identifier):
            if (
                isinstance(identifier, Collection) and len(identifier) == 2
            ):  # is code tuple
                return bd.get_node(database=identifier[0], code=identifier[1])
            elif isinstance(identifier, int):  # id is an int
                return bd.get_node(id=identifier)
            else:
                raise ValueError(
                    "The flow-identifier stored in the selected method is neither an id nor the tuple (database, code). No automatic matching possible."
                )

        bioflow_nodes = set(
            get_bioflow_node(identifier) for identifier, _ in method_data
        )

        for node in bioflow_nodes:
            if "carbon dioxide" in node["name"].lower():
                if "soil" in node.get("categories", []):
                    self.characterization_function_dict[node.id] = (
                        characterize_co2_uptake  # negative emission because uptake by soil
                    )

                else:
                    self.characterization_function_dict[node.id] = characterize_co2

            elif (
                "methane, fossil" in node["name"].lower()
                or "methane, from soil or biomass stock" in node["name"].lower()
            ):
                # TODO Check why "methane, non-fossil" has a CF of 27 instead of 29.8, currently excluded
                self.characterization_function_dict[node.id] = characterize_ch4

            elif "dinitrogen monoxide" in node["name"].lower():
                self.characterization_function_dict[node.id] = characterize_n2o

            elif "carbon monoxide" in node["name"].lower():
                self.characterization_function_dict[node.id] = characterize_co

            else:
                cas_number = node.get("CAS number")
                if cas_number:
                    decay_series = decay_multipliers.get(cas_number)
                    if decay_series is not None:
                        self.characterization_function_dict[node.id] = (
                            create_generic_characterization_function(
                                np.array(decay_series)
                            )
                        )


def IRF_co2(year) -> callable:
    """
    Impulse Resonse Function (IRF) of CO2

    Parameters
    ----------
    year : int
        The year after emission for which the IRF is calculated.

    Returns
    -------
    float
        The IRF value for the given year.

    """
    alpha_0, alpha_1, alpha_2, alpha_3 = 0.2173, 0.2240, 0.2824, 0.2763
    tau_1, tau_2, tau_3 = 394.4, 36.54, 4.304
    exponentials = lambda year, alpha, tau: alpha * tau * (1 - np.exp(-year / tau))
    return (
        alpha_0 * year
        + exponentials(year, alpha_1, tau_1)
        + exponentials(year, alpha_2, tau_2)
        + exponentials(year, alpha_3, tau_3)
    )


def characterize_co2(
    series,
    period: int | None = 100,
    cumulative: bool | None = False,
) -> pd.DataFrame:
    """
    Calculate the cumulative or marginal radiative forcing (CRF) from CO2 for each year in a given period.

    Based on characterize_co2 from bw_temporalis, but updated numerical values from IPCC AR6 Ch7 & SM.

    If `cumulative` is True, the cumulative CRF is calculated. If `cumulative` is False, the marginal CRF is calculated.
    Takes a single row of the TimeSeries Pandas DataFrame (corresponding to a set of (`date`/`amount`/`flow`/`activity`).
    For each year in the given period, the CRF is calculated.
    Units are watts/square meter/kilogram of CO2.

    Returns
    -------
    A TimeSeries dataframe with the following columns:
    - date: datetime64[s]
    - amount: float
    - flow: str
    - activity: str

    See also
    --------
    Joos2013: Relevant scientific publication on CRF: https://doi.org/10.5194/acp-13-2793-2013
    Schivley2015: Relevant scientific publication on the numerical calculation of CRF: https://doi.org/10.1021/acs.est.5b01118
    Forster2023: Updated numerical values from IPCC AR6 Chapter 7 (Table 7.15): https://doi.org/10.1017/9781009157896.009
    """

    # functional variables and units (from publications listed in docstring)
    radiative_efficiency_ppb = (
        1.33e-5  # W/m2/ppb; 2019 background co2 concentration; IPCC AR6 Table 7.15
    )

    # for conversion from ppb to kg-CO2
    M_co2 = 44.01  # g/mol
    M_air = 28.97  # g/mol, dry air
    m_atmosphere = 5.135e18  # kg [Trenberth and Smith, 2005]

    radiative_efficiency_kg = (
        radiative_efficiency_ppb * M_air / M_co2 * 1e9 / m_atmosphere
    )  # W/m2/kg-CO2

    date_beginning: np.datetime64 = series["date"].to_numpy()
    date_characterized: np.ndarray = date_beginning + np.arange(
        start=0, stop=period, dtype="timedelta64[Y]"
    ).astype("timedelta64[s]")

    decay_multipliers: np.ndarray = np.array(
        [radiative_efficiency_kg * IRF_co2(year) for year in range(period)]
    )

    forcing = pd.Series(data=series.amount * decay_multipliers, dtype="float64")

    if not cumulative:
        forcing = forcing.diff(periods=1).fillna(0)

    return pd.DataFrame(
        {
            "date": pd.Series(data=date_characterized, dtype="datetime64[s]"),
            "amount": forcing,
            "flow": series.flow,
            "activity": series.activity,
        }
    )


def characterize_co2_uptake(
    series,
    period: int | None = 100,
    cumulative: bool | None = False,
) -> pd.DataFrame:
    """
    The same as characterize_co2, but with a negative sign for uptake of CO2.

    Based on characterize_co2 from bw_temporalis, but updated numerical values from IPCC AR6 Ch7 & SM.

    Calculate the negative cumulative or marginal radiative forcing (CRF) from CO2-uptake for each year in a given period.

    If `cumulative` is True, the cumulative CRF is calculated. If `cumulative` is False, the marginal CRF is calculated.
    Takes a single row of the TimeSeries Pandas DataFrame (corresponding to a set of (`date`/`amount`/`flow`/`activity`).
    For each year in the given period, the CRF is calculated.
    Units are watts/square meter/kilogram of CO2.

    Returns
    -------
    A TimeSeries dataframe with the following columns:
    - date: datetime64[s]
    - amount: float
    - flow: str
    - activity: str

    See also
    --------
    Joos2013: Relevant scientific publication on CRF: https://doi.org/10.5194/acp-13-2793-2013
    Schivley2015: Relevant scientific publication on the numerical calculation of CRF: https://doi.org/10.1021/acs.est.5b01118
    Forster2023: Updated numerical values from IPCC AR6 Chapter 7 (Table 7.15): https://doi.org/10.1017/9781009157896.009
    """

    # functional variables and units (from publications listed in docstring)
    radiative_efficiency_ppb = (
        1.33e-5  # W/m2/ppb; 2019 background co2 concentration; IPCC AR6 Table 7.15
    )

    # for conversion from ppb to kg-CO2
    M_co2 = 44.01  # g/mol
    M_air = 28.97  # g/mol, dry air
    m_atmosphere = 5.135e18  # kg [Trenberth and Smith, 2005]

    radiative_efficiency_kg = (
        radiative_efficiency_ppb * M_air / M_co2 * 1e9 / m_atmosphere
    )  # W/m2/kg-CO2

    date_beginning: np.datetime64 = series["date"].to_numpy()
    date_characterized: np.ndarray = date_beginning + np.arange(
        start=0, stop=period, dtype="timedelta64[Y]"
    ).astype("timedelta64[s]")

    decay_multipliers: np.ndarray = np.array(
        [radiative_efficiency_kg * IRF_co2(year) for year in range(period)]
    )

    forcing = pd.Series(data=series.amount * decay_multipliers, dtype="float64")

    forcing = (
        -forcing
    )  # flip the sign of the characterization function for CO2 uptake and not release

    if not cumulative:
        forcing = forcing.diff(periods=1).fillna(0)

    return pd.DataFrame(
        {
            "date": pd.Series(data=date_characterized, dtype="datetime64[s]"),
            "amount": forcing,
            "flow": series.flow,
            "activity": series.activity,
        }
    )


def characterize_co(
    series,
    period: int | None = 100,
    cumulative: bool | None = False,
) -> pd.DataFrame:
    """
    Calculate the cumulative or marginal radiative forcing (CRF) from CO for each year in a given period.

    This is exactly the same function as for CO2, it's just scaled by the ratio of molar masses of CO and CO2. This is because CO is very short-lived (lifetime ~2 months) and we assume that it completely reacts to CO2 within the first year.

    Based on characterize_co2 from bw_temporalis, but updated numerical values from IPCC AR6 Ch7 & SM.

    Calculate the cumulative or marginal radiative forcing (CRF) from CO2 for each year in a given period.

    If `cumulative` is True, the cumulative CRF is calculated. If `cumulative` is False, the marginal CRF is calculated.
    Takes a single row of the TimeSeries Pandas DataFrame (corresponding to a set of (`date`/`amount`/`flow`/`activity`).
    For each year in the given period, the CRF is calculated.
    Units are watts/square meter/kilogram of CO2.

    Returns
    -------
    A TimeSeries dataframe with the following columns:
    - date: datetime64[s]
    - amount: float
    - flow: str
    - activity: str

    See also
    --------
    Joos2013: Relevant scientific publication on CRF: https://doi.org/10.5194/acp-13-2793-2013
    Schivley2015: Relevant scientific publication on the numerical calculation of CRF: https://doi.org/10.1021/acs.est.5b01118
    Forster2023: Updated numerical values from IPCC AR6 Chapter 7 (Table 7.15): https://doi.org/10.1017/9781009157896.009
    """

    # functional variables and units (from publications listed in docstring)
    radiative_efficiency_ppb = (
        1.33e-5  # W/m2/ppb; 2019 background co2 concentration; IPCC AR6 Table 7.15
    )

    # for conversion from ppb to kg-CO2
    M_co2 = 44.01  # g/mol
    M_co = 28.01  # g/mol
    M_air = 28.97  # g/mol, dry air
    m_atmosphere = 5.135e18  # kg [Trenberth and Smith, 2005]

    radiative_efficiency_kg = (
        radiative_efficiency_ppb * M_air / M_co2 * 1e9 / m_atmosphere
    )  # W/m2/kg-CO2

    date_beginning: np.datetime64 = series["date"].to_numpy()
    date_characterized: np.ndarray = date_beginning + np.arange(
        start=0, stop=period, dtype="timedelta64[Y]"
    ).astype("timedelta64[s]")

    decay_multipliers: np.ndarray = np.array(
        [
            M_co2 / M_co * radiative_efficiency_kg * IRF_co2(year)
            for year in range(period)
        ]  # <-- Scaling from co2 to co is done here
    )

    forcing = pd.Series(data=series.amount * decay_multipliers, dtype="float64")

    if not cumulative:
        forcing = forcing.diff(periods=1).fillna(0)

    return pd.DataFrame(
        {
            "date": pd.Series(data=date_characterized, dtype="datetime64[s]"),
            "amount": forcing,
            "flow": series.flow,
            "activity": series.activity,
        }
    )


def characterize_ch4(
    series,
    period: int = 100,
    cumulative=False,
) -> pd.DataFrame:
    """
    Calculate the cumulative or marginal radiative forcing (CRF) from CH4 for each year in a given period.

    Based on characterize_methane from bw_temporalis, but updated numerical values from IPCC AR6 Ch7 & SM.

    This DOES include indirect effects of CH4 on ozone and water vapor, but DOES NOT include the decay to CO2.
    For more info on that, see the deprecated version of bw_temporalis.

    If `cumulative` is True, the cumulative CRF is calculated. If `cumulative` is False, the marginal CRF is calculated.
    Takes a single row of the TimeSeries Pandas DataFrame (corresponding to a set of (`date`/`amount`/`flow`/`activity`).
    For earch year in the given period, the CRF is calculated.
    Units are watts/square meter/kilogram of CH4.

    Parameters
    ----------
    series : array-like
        A single row of the TimeSeries dataframe.
    period : int, optional
        Time period for calculation (number of years), by default 100
    cumulative : bool, optional
        Should the RF amounts be summed over time?

    Returns
    -------
    A TimeSeries dataframe with the following columns:
    - date: datetime64[s]
    - amount: float
    - flow: str
    - activity: str

    See also
    --------
    Joos2013: Relevant scientific publication on CRF: https://doi.org/10.5194/acp-13-2793-2013
    Schivley2015: Relevant scientific publication on the numerical calculation of CRF: https://doi.org/10.1021/acs.est.5b01118
    Forster2023: Updated numerical values from IPCC AR6 Chapter 7 (Table 7.15): https://doi.org/10.1017/9781009157896.009
    """

    # functional variables and units (from publications listed in docstring)
    radiative_efficiency_ppb = 5.7e-4  # # W/m2/ppb; 2019 background cch4 concentration; IPCC AR6 Table 7.15. This number includes indirect effects.

    # for conversion from ppb to kg-CH4
    M_ch4 = 16.04  # g/mol
    M_air = 28.97  # g/mol, dry air
    m_atmosphere = 5.135e18  # kg [Trenberth and Smith, 2005]

    radiative_efficiency_kg = (
        radiative_efficiency_ppb * M_air / M_ch4 * 1e9 / m_atmosphere
    )  # W/m2/kg-CH4

    tau = 11.8  # Lifetime (years)

    date_beginning: np.datetime64 = series["date"].to_numpy()
    date_characterized: np.ndarray = date_beginning + np.arange(
        start=0, stop=period, dtype="timedelta64[Y]"
    ).astype("timedelta64[s]")

    decay_multipliers: list = np.array(
        [
            radiative_efficiency_kg * tau * (1 - np.exp(-year / tau))
            for year in range(period)
        ]
    )

    forcing = pd.Series(data=series.amount * decay_multipliers, dtype="float64")

    if not cumulative:
        forcing = forcing.diff(periods=1).fillna(0)

    return pd.DataFrame(
        {
            "date": pd.Series(data=date_characterized, dtype="datetime64[s]"),
            "amount": forcing,
            "flow": series.flow,
            "activity": series.activity,
        }
    )


def characterize_n2o(
    series,
    period: int = 100,
    cumulative=False,
) -> pd.DataFrame:
    """
    Calculate the cumulative or marginal radiative forcing (CRF) from N2O for each year in a given period.

    Based on characterize_methane from bw_temporalis, but updated numerical values from IPCC AR6 Ch7 & SM.

    If `cumulative` is True, the cumulative CRF is calculated. If `cumulative` is False, the marginal CRF is calculated.
    Takes a single row of the TimeSeries Pandas DataFrame (corresponding to a set of (`date`/`amount`/`flow`/`activity`).
    For earch year in the given period, the CRF is calculated.
    Units are watts/square meter/kilogram of N2O.

    Parameters
    ----------
    series : array-like
        A single row of the TimeSeries dataframe.
    period : int, optional
        Time period for calculation (number of years), by default 100
    cumulative : bool, optional
        Should the RF amounts be summed over time?

    Returns
    -------
    A TimeSeries dataframe with the following columns:
    - date: datetime64[s]
    - amount: float
    - flow: str
    - activity: str

    See also
    --------
    Joos2013: Relevant scientific publication on CRF: https://doi.org/10.5194/acp-13-2793-2013
    Schivley2015: Relevant scientific publication on the numerical calculation of CRF: https://doi.org/10.1021/acs.est.5b01118
    Forster2023: Updated numerical values from IPCC AR6 Chapter 7 (Table 7.15): https://doi.org/10.1017/9781009157896.009
    """

    # functional variables and units (from publications listed in docstring)
    radiative_efficiency_ppb = 2.8e-3  # # W/m2/ppb; 2019 background cch4 concentration; IPCC AR6 Table 7.15. This number includes indirect effects.

    # for conversion from ppb to kg-CH4
    M_n2o = 44.01  # g/mol
    M_air = 28.97  # g/mol, dry air
    m_atmosphere = 5.135e18  # kg [Trenberth and Smith, 2005]

    radiative_efficiency_kg = (
        radiative_efficiency_ppb * M_air / M_n2o * 1e9 / m_atmosphere
    )  # W/m2/kg-N2O

    tau = 109  # Lifetime (years)

    date_beginning: np.datetime64 = series["date"].to_numpy()
    date_characterized: np.ndarray = date_beginning + np.arange(
        start=0, stop=period, dtype="timedelta64[Y]"
    ).astype("timedelta64[s]")

    decay_multipliers: list = np.array(
        [
            radiative_efficiency_kg * tau * (1 - np.exp(-year / tau))
            for year in range(period)
        ]
    )

    forcing = pd.Series(data=series.amount * decay_multipliers, dtype="float64")
    if not cumulative:
        forcing = forcing.diff(periods=1).fillna(0)

    return pd.DataFrame(
        {
            "date": pd.Series(data=date_characterized, dtype="datetime64[s]"),
            "amount": forcing,
            "flow": series.flow,
            "activity": series.activity,
        }
    )


def create_generic_characterization_function(decay_series) -> pd.DataFrame:
    """
    Creates a characterization function for a GHG based on a decay series, by calling the nested method `characterize_generic()`.

    Parameters
    ----------
    decay_series : np.ndarray
        A decay series for a specific GHG. This is retrieved from `../data/decay_multipliers.pkl`

    Returns
    -------
    A function called `characterize_generic`, which in turn returns a TimeSeries dataframe that contains the forcing of the emission of the row over the given period based on the decay series of that biosphere flow.

    """

    def characterize_generic(
        series,
        period: int = 100,
        cumulative=False,
    ) -> pd.DataFrame:
        """
        Uses lookup generated in /dev/calculate_metrics.ipynb
        Data originates from https://doi.org/10.1029/2019RG000691

        Parameters
        ----------
        series : array-like
            A single row of the dynamic inventory dataframe.
        period : int, optional
            Time period for calculation (number of years), by default 100
        cumulative : bool,
            cumulative impact

        Returns
        -------
        A TimeSeries dataframe that contains the forcing of the point emission from the row for each year in the given period.
          date: datetime64[s]
          amount: float (forcing at this timestep)
          flow: str
          activity: str

        See also
        --------
        Joos2013: Relevant scientific publication on CRF: https://doi.org/10.5194/acp-13-2793-2013
        Schivley2015: Relevant scientific publication on the numerical calculation of CRF: https://doi.org/10.1021/acs.est.5b01118
        Forster2023: Updated numerical values from IPCC AR6 Chapter 7 (Table 7.15): https://doi.org/10.1017/9781009157896.009

        """

        date_beginning: np.datetime64 = series["date"].to_numpy()

        dates_characterized: np.ndarray = date_beginning + np.arange(
            start=0, stop=period, dtype="timedelta64[Y]"
        ).astype("timedelta64[s]")

        decay_multipliers = decay_series[:period]

        forcing = pd.Series(data=series.amount * decay_multipliers, dtype="float64")

        if not cumulative:
            forcing = forcing.diff(periods=1).fillna(0)

        return pd.DataFrame(
            {
                "date": pd.Series(data=dates_characterized, dtype="datetime64[s]"),
                "amount": forcing,
                "flow": series.flow,
                "activity": series.activity,
            }
        )

    return characterize_generic
