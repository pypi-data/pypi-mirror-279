import configparser
from pathlib import Path

import matplotlib.pyplot as plt
import sklearn

from geocif import geocif as gc
from geocif import logger as log

plt.style.use("default")
sklearn.set_config(transform_output="pandas")

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


def run(inputs, logger, parser, section, item, type, values):
    if type == "str":
        original_value = parser.get(section, item)
    elif type == "bool":
        original_value = parser.getboolean(section, item)
    elif type == "int":
        original_value = parser.getint(section, item)
    elif type == "float":
        original_value = parser.getfloat(section, item)

    for value in values:
        if type == "str":
            parser.set(section, item, value)
        elif type == "bool":
            parser.set(section, item, str(value))
        elif type == "int":
            parser.set(section, item, str(value))
        elif type == "float":
            parser.set(section, item, str(value))

        gc.execute_models(inputs, logger, parser)

    parser.set(section, item, original_value)

    return parser


def main(path_config_files=[Path("../config/geocif.txt")]):
    logger, parser = log.setup_logger_parser(path_config_files)
    inputs = gc.gather_inputs(parser)

    logger.info("=============================")
    logger.info("\tStarting GEOCIF Experiments")
    logger.info("=============================")

    # Experiment 1: include_lat_lon
    logger.info("Experiment 1: include_lat_lon")
    parser = run(
        inputs, logger, parser, "experiments", "include_lat_lon", "bool", [True, False]
    )

    # Experiment 2: feature_selection
    logger.info("Experiment 2: feature_selection")
    parser = run(
        inputs,
        logger,
        parser,
        "experiments",
        "feature_selection",
        "str",
        ["SelectKBest", "BorutaPy", "Leshy", "RFECV", "RFE"],
    )

    # Experiment 3: lag_years
    logger.info("Experiment 3: lag_years")
    parser = run(
        inputs, logger, parser, "experiments", "lag_years", "int", [1, 2, 3, 4, 5]
    )

    # Experiment 4: lag_yield_as_feature
    logger.info("Experiment 4: lag_yield_as_feature")
    parser = run(
        inputs,
        logger,
        parser,
        "experiments",
        "lag_yield_as_feature",
        "bool",
        [True, False],
    )

    # Experiment 5: median_years
    logger.info("Experiment 5: median_years")
    parser = run(
        inputs, logger, parser, "experiments", "median_years", "int", [2, 3, 4, 5]
    )

    # Experiment 6: median_yield_as_feature
    logger.info("Experiment 6: median_yield_as_feature")
    parser = run(
        inputs,
        logger,
        parser,
        "experiments",
        "median_yield_as_feature",
        "bool",
        [True, False],
    )

    # Experiment 7: analogous_year_yield_as_feature
    logger.info("Experiment 7: analogous_year_yield_as_feature")
    parser = run(
        inputs,
        logger,
        parser,
        "experiments",
        "analogous_year_yield_as_feature",
        "bool",
        [True, False],
    )

    # Experiment 8: optimize
    logger.info("Experiment 8: optimize")
    parser = run(
        inputs, logger, parser, "experiments", "optimize", "bool", [True, False]
    )


if __name__ == "__main__":
    main()
