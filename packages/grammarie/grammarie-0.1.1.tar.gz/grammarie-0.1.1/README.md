# grammarie

Grammarie is a type of [Fae magic](https://kingkiller.fandom.com/wiki/Fae_magic) that is the craft
of making things be. This package helps you shape your data into its proper form.

More specifically, this package defines a set of types annotated in a way that let's Pydantic validate and/or coerce
data into the target type and form.

In the example below, data is provided with wrong types and formats, but are coerced by the types defined by the model
and its fields.

```python
from datetime import UTC, datetime
from pydantic import BaseModel
from grammarie import Decimal1, IntTimestampMS, LowercaseStr, UppercaseStr


class PowerTransformer(BaseModel):
    id: LowercaseStr
    name: UppercaseStr
    voltage_primary: Decimal1
    voltage_secondary: Decimal1
    installation_date: IntTimestampMS


transformers = [
    PowerTransformer(
        id="d37dca6f-6f23-4401-8cc8-e3ee422939e4",
        name="S Ulven T1 Transformator",
        voltage_primary=420.00056,
        voltage_secondary="132",
        installation_date="2023-05-03 11:15:01",
    ),
    PowerTransformer(
        id="26381360-959A-4D39-8049-D20889FAE0d6",
        name="S Ofoten T2 Transformator",
        voltage_primary="420",
        voltage_secondary=300,
        installation_date=datetime(2021, 8, 16, 8, 35, 1, tzinfo=UTC),
    ),
]

print(transformers)
# [
#     PowerTransformer(
#         id='d37dca6f-6f23-4401-8cc8-e3ee422939e4',
#         name='S ULVEN T1 TRANSFORMATOR',
#         voltage_primary=Decimal('420.0'),
#         voltage_secondary=Decimal('132.0'),
#         installation_date=1683105301000
#     ),
#     PowerTransformer(
#         id='26381360-959a-4d39-8049-d20889fae0d6',
#         name='S OFOTEN T2 TRANSFORMATOR',
#         voltage_primary=Decimal('420.0'),
#         voltage_secondary=Decimal('300.0'),
#         installation_date=1629102901000
#     )
# ]
```

## Installation

This package is available on PyPI and can be installed with pip, uv, pdm, poetry or any other package manager.

## Development

This project uses [Poetry](https://python-poetry.org/) to manage the environment and Python dependencies.
To install the development environment and run the test suite:
```bash
poetry install
poetry run pytest
```

It's recommended to also install the pre-commit hooks:
```bash
poetry run pre-commit install
```

This ensures that linting and formatting are run automatically on every commit.
