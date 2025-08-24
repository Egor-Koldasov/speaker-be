from pydantic import BaseModel


class TestModel1(BaseModel):
    field1: str


class TestModel2(BaseModel):
    field2: TestModel1
    field3: str


test_json_1 = """
{
  "field2": {
    "field1": "field1_value",
    "field5": "field5_value"
  },
  "field3": "field3_value",
  "field4": "field4_value"
}
"""


def test_model_validation():
    model_1 = TestModel2.model_validate_json(test_json_1)
    print(model_1)


if __name__ == "__main__":
    test_model_validation()
