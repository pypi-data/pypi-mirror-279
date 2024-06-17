from datetime import datetime, timedelta
from typing import Any

import typer
from validio_sdk.graphql_client.input_types import TimeRangeInput

from validio_cli import (
    AsyncTyper,
    ConfigDir,
    Namespace,
    OutputFormat,
    OutputFormatOption,
    OutputSettings,
    _format_relative_time,
    get_client_and_config,
    output_json,
    output_text,
)
from validio_cli.bin.entities import validators

app = AsyncTyper(help="Incidents from validators")


@app.async_command(
    help="""List all incidents.

By default you will get incidents from the last hour. You can specify a time
range for when the incident occurred by specifying when the incident ended.

You can list incidents in different ways:

* Listing all incidents

* Listing all incidents for a specific validator with --validator

* Listing all incidents for a specific segment with --segment

* Listing all incidents for a specific validator and segment with --validator
and --segment together
"""
)
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    namespace: str = Namespace(),
    ended_before: datetime = typer.Option(
        datetime.utcnow(),
        help="The incident ended before this timestamp",
    ),
    ended_after: datetime = typer.Option(
        (datetime.utcnow() - timedelta(hours=1)),
        help="The incident ended after this timestamp",
    ),
    validator: str = typer.Option(..., help="Validator to fetch incidents for"),
    segment: str = typer.Option(None, help="Segment to fetch incidents for"),
) -> None:
    vc, cfg = await get_client_and_config(config_dir)

    if validator is not None:
        validator_id = await validators.get_validator_id(vc, cfg, validator, namespace)
        if validator_id is None:
            return None

    # TODO(UI-2006): These should all support namespace

    incidents = await vc.get_validator_incidents(
        id=validator_id,
        range=TimeRangeInput(
            start=ended_after,
            end=ended_before,
        ),
        segment_id=segment,
    )

    if not incidents:
        return output_text(None, {})

    if output_format == OutputFormat.JSON:
        return output_json(incidents)

    return output_text(
        incidents.incidents,
        fields={
            "validator": OutputSettings(
                pass_full_object=True,
                reformat=lambda _: incidents.typename__,
            ),
            "bound": OutputSettings(
                pass_full_object=True,
                reformat=lambda x: (
                    f"{format_number(x.lower_bound)} - "
                    f"{format_number(x.upper_bound)}"
                ),
            ),
            "value": OutputSettings(reformat=format_number),
            "deviation": OutputSettings(reformat=format_number),
            "severity": None,
            "status": None,
            "age": OutputSettings(
                pass_full_object=True,
                reformat=lambda x: _format_relative_time(x.end_time),
            ),
        },
    )


def calculate_operator(item: Any) -> str:
    type_ = item.typename__[len("ValidatorMetricWith") :]
    if type_ == "DynamicThreshold":
        operator = item.decision_bounds_type
    else:
        operator = item.operator

    return f"{type_}/{operator}"


def calculate_bound(item: Any) -> str:
    type_ = item.typename__[len("ValidatorMetricWith") :]
    if type_ == "DynamicThreshold":
        bound = f"{item.lower_bound:.2f} - {item.upper_bound:.2f}"
    elif type_ == "FixedThreshold":
        bound = item.bound
    else:
        bound = "-"

    return bound


def format_number(item: Any) -> str:
    if item % 1 == 0:
        return str(item)
    if (item * 10) % 1 == 0:
        return f"{item:.1f}"
    if (item * 100) % 1 == 0:
        return f"{item:.2f}"
    if (item * 1000) % 1 == 0:
        return f"{item:.3f}"

    return f"{item:.3f}..."


if __name__ == "__main__":
    typer.run(app())
