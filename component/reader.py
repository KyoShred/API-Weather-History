"""Reads a JSON file and returns a Python object.

  Args:
    file: The JSON file.

  Returns:
    A Python object representing the JSON data.
"""
file = open("../data/rdu-weather-history.json", "r")
async def read_json_file(file: File) -> dict:

  json_data = file.read()
  return json.loads(json_data)