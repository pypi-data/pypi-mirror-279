import random
from faker import Faker
from sqlalchemy import Integer, String, Date, Float, Boolean, Column
from .custom_providers import random_amount


def get_column_provider(column: Column, faker: Faker, custom_providers={}):
    type_mapping = {
        String: faker.word,
        Integer: faker.random_int,
        Float: random_amount,
        Boolean: faker.boolean,
        Date: faker.date,
    }
    # Check for a custom faker provider
    if hasattr(column, "info") and "provider" in column.info:
        try:
            provider = column.info["provider"]

            if provider.startswith("enum"):
                enum_values = provider.split(":")[1]
                return lambda: random.choice(enum_values.split(","))

            # Check if the provider is a custom function
            if provider in custom_providers.keys():
                return custom_providers[provider]

            # Otherwise, use the faker library
            return faker.__getattr__(provider)
        except AttributeError as e:
            print(e)
            return faker.word

    # If no info provided, use some sensible default types
    return type_mapping.get(type(column.type), faker.word)
