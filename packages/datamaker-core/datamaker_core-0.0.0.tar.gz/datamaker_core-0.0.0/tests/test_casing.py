from datamaker.utils.casing import snake_to_camel_case, snake_to_pascal_case


def test_snake_to_camel_case():
    assert snake_to_camel_case("hello_world") == "helloWorld"
    assert snake_to_camel_case("snake_case_string") == "snakeCaseString"
    assert snake_to_camel_case("camel_case") == "camelCase"
    assert snake_to_camel_case("single") == "single"
    assert snake_to_camel_case("") == ""


def test_snake_to_pascal_case():
    assert snake_to_pascal_case("hello_world") == "HelloWorld"
    assert snake_to_pascal_case("snake_case_string") == "SnakeCaseString"
    assert snake_to_pascal_case("camel_case") == "CamelCase"
    assert snake_to_pascal_case("single") == "Single"
    assert snake_to_pascal_case("") == ""
