import logging
from typing import Literal

import click

from fhirmodels import constants as _c
from fhirmodels import fhir_package, generator

# Configure the logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@click.group()
def main():
    """
    This tool helps in generating FHIR models from specified FHIR packages.
    Use the available commands to interact with the tool.
    """
    pass


@main.command()
@click.option(
    "--version",
    "-v",
    default="R4",
    type=click.Choice(["R4", "R4B", "R5"]),
    help="FHIR version to generate models for. Options are: R4, R4B, R5. Defaults to R4.",
)
def generate(
    version: Literal["R4", "R4B", "R5"],
):
    """Generate models from FHIR packages.

    This command will generate model classes based on the specified FHIR version.
    """
    logger.info(f"Generating models for FHIR version: {version}")

    # Load the FHIR package
    package_loader = fhir_package.FhirPackageLoader()
    package = package_loader.load_from_version(fhir_version=version)

    # Generate model classes
    gen = generator.ModelGenerator(package=package)
    gen.generate_model_classes()
    logger.info("Model generation completed.")


if __name__ == "__main__":
    main()
