"""Parse a Pydantic model so it is usable by SQLAlchemy."""

from __future__ import annotations

def is_pydantic(obj: object) -> bool:
    """Check whether an object is pydantic.

    Params:
        obj (object): An arbitrary Python object to evaluate

    Returns:
        (bool): `True` if `obj` is of Pydantic type `ModelMetaClass`
        (bool): `False` if `obj` is not of Pydatic type `ModelMetaClass`

    """
    return type(obj).__class__.__name__ == "ModelMetaclass"


def parse_pydantic_schema(schema):
    """Iterate through pydantic schema and parses nested schemas to a dictionary containing SQLAlchemy models.

    Only works if nested schemas have specified the Meta.orm_model.

    Make sure to add this line to Pydantic schemas that have an ORM class:

    ``` py linenums="1"
    class Meta:
        orm_model = "SQLAModelName"
    ```
    """
    parsed_schema: dict = dict(schema)

    for key, value in parsed_schema.items():
        try:
            if isinstance(value, list) and len(value):
                if is_pydantic(value[0]):
                    parsed_schema[key] = [
                        schema.Meta.orm_model(**schema.dict()) for schema in value
                    ]

            else:
                if is_pydantic(value):
                    parsed_schema[key] = value.Meta.orm_model(**value.dict())

        except AttributeError:
            raise AttributeError(
                "Found nested Pydantic model but Meta.orm_model was not specified."
            )

    return parsed_schema
