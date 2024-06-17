# fast-opex
Simpler and faster implementation of the OPEX JSON file format for object detection predictions.

Uses [orjson](https://github.com/ijl/orjson) if present (no pretty-printing available) for further speed-ups, 
otherwise the standard json library.

This library is written in Python. For a Java port, please see 
[opex4j](https://github.com/waikato-datamining/opex4j).

## Installation

You can install the library via `pip` (or `pip3`):

```commandline
pip install fast-opex
```

## JSON

```json
{
  "timestamp": "%Y%m%d_%H%M%S.%f",
  "id": "str",
  "objects": [
    {
      "score": 1.0,
      "label": "person",
      "bbox": {
        "top": 100,
        "left": 100,
        "bottom": 150,
        "right": 120
      },
      "polygon": {
        "points": [
          [100, 100],
          [150, 100],
          [150, 120],
          [100, 120]
        ]
      }
    },
    {
      "score": 0.95,
      "label": "house",
      "bbox": {
        "top": 100,
        "left": 100,
        "bottom": 200,
        "right": 200
      },
      "polygon": {
        "points": [
          [100, 100],
          [200, 100],
          [200, 200],
          [100, 200]
        ]
      },
      "meta": {
        "price": "500k"
      }
    }
  ],
  "meta": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

**Notes:**

The following keys are optional: 

* timestamp
* meta
* score 


## Reading/Writing

To read a prediction:

```python
from opex import ObjectPredictions

# From a string
predictions = ObjectPredictions.from_json_string("{...}")

# From a named file
predictions = ObjectPredictions.load_json_from_file("predictions.json")

# From an open stream
with open("predictions.json", "r") as stream:
    predictions = ObjectPredictions.read_json_from_stream(stream)
```

To write a prediction:

```python
from opex import ObjectPredictions

predictions: ObjectPredictions = ...

# Serialise the object to a JSON-formatted string
print(predictions.to_json_string())
print(predictions.to_json_string(indent=2))

# Write the object to a file
predictions.save_json_to_file("predictions.json", indent=2)

# Write to an open stream
with open("predictions.json", "w") as stream:
    predictions.write_json_to_stream(stream, indent=2)
```
