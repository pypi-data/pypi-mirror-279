ORJSON_INDENT_WARNING = False
try:
    import orjson
    import orjson as json
    ORJSON = True
except:
    import json
    ORJSON = False

from dataclasses import dataclass
from typing import Dict, List, Optional

from ._ObjectPrediction import ObjectPrediction, BBox, Polygon


@dataclass
class ObjectPredictions:
    """
    A collection of object predictions.
    """
    # The time at which the picture was taken
    timestamp: Optional[str] = None

    # The camera that took the picture
    id: str = None

    # The object predictions
    objects: List[ObjectPrediction] = None

    # Any meta-data
    meta: Optional[Dict[str, str]] = None

    def __str__(self):
        """
        Returns a short string representation of itself.

        :return: the string representation
        :rtype: str
        """
        return "timestamp=%s, id=%s, #objects=%d" % (str(self.timestamp), self.id, len(self.objects))

    def to_dict(self):
        """
        Returns its values as dictionary.

        :return: the generated dictionary
        :rtype: dict
        """
        objs = []
        for obj in self.objects:
            objs.append(obj.to_dict())
        return {
            "timestamp": self.timestamp,
            "id": self.id,
            "objects": objs,
            "meta": self.meta,
        }

    def to_json_string(self, indent: Optional[int] = None) -> str:
        """
        Returns itself as JSON string.

        :param indent: the indentation to use for pretty printing, None for space-saving output
        :type indent: int
        :return: the generated JSON string
        :rtype: str
        """
        global ORJSON_INDENT_WARNING

        if ORJSON:
            if indent is None:
                return json.dumps(self.to_dict()).decode("utf-8")
            else:
                if (indent != 2) and not ORJSON_INDENT_WARNING:
                    ORJSON_INDENT_WARNING = True
                    print("WARNING: Only indent=2 is supported!")
                return json.dumps(self.to_dict(), option=orjson.OPT_INDENT_2).decode("utf-8")
        else:
            return json.dumps(self.to_dict(), indent=indent)

    def save_json_to_file(self, path: str, indent: Optional[int] = None):
        """
        Saves the JSON representation to the specified file.

        :param path: the file to write to
        :type path: str
        :param indent: the indentation to use for pretty printing, None for space-saving output
        :type indent: int
        """
        with open(path, "w") as fp:
            fp.write(self.to_json_string(indent=indent))
            fp.write("\n")

    def write_json_to_stream(self, stream, indent: Optional[int] = None):
        """
        Saves the JSON representation to the specified stream.

        :param stream: the stream to write to (file-like object)
        :param indent: the indentation to use for pretty printing, None for space-saving output
        :type indent: int
        """
        global ORJSON_INDENT_WARNING

        if ORJSON:
            if indent is None:
                stream.write(json.dumps(self.to_dict()))
            else:
                if (indent != 2) and not ORJSON_INDENT_WARNING:
                    ORJSON_INDENT_WARNING = True
                    print("OPEX ORJSON WARNING: Only indent=2 is supported!")
                stream.write(json.dumps(self.to_dict(), option=orjson.OPT_INDENT_2))
        else:
            json.dump(self, stream, indent=indent)

    @classmethod
    def _bbox_from_dict(cls, index: int, d: Dict) -> BBox:
        """
        Instantiates the bbox from the dictionary.

        :param index: the index in the objects array
        :type index: int
        :param d: the dictionary to use
        :type d: dict
        :return: the bounding box
        :rtype: BBox
        """
        try:
            return BBox(
                top=int(d["top"]),
                left=int(d["left"]),
                bottom=int(d["bottom"]),
                right=int(d["right"])
            )
        except Exception as e:
            raise Exception("Failed to instantiate BBox #%d" % index) from e

    @classmethod
    def _polygon_from_dict(cls, index: int, d: Dict) -> Polygon:
        """
        Instantiates the polygon from the dictionary.

        :param index: the index in the objects array
        :type index: int
        :param d: the dictionary to use
        :type d: dict
        :return: the polygon object
        :rtype: Polygon
        """
        if "points" not in d:
            raise Exception("No 'points' present (Polygon #%d)!" % index)
        if not isinstance(d["points"], list):
            raise Exception("'points' not a list (Polygon #%d)!" % index)
        try:
            points = [[x, y] for x, y in d["points"]]
            return Polygon(points=points)
        except Exception as e:
            raise Exception("Failed to instantiate Polygon #%d" % index) from e

    @classmethod
    def _object_from_dict(cls, index: int, d: Dict) -> ObjectPrediction:
        """
        Instantiates the object from the dictionary.

        :param index: the index in the objects array
        :type index: int
        :param d: the dictionary to use
        :type d: dict
        :return: the prediction
        :rtype: ObjectPrediction
        """
        if d is None:
            raise Exception("Expected dictionary (object #%d), but got None!" % index)
        if not isinstance(d, dict):
            raise Exception("Expected dictionary (object #%d), but got: %s" % (index, str(type(d))))

        # score (optional)
        score = None
        if "score" in d:
            score = float(d["score"])

        # label
        if "label" not in d:
            raise Exception("No 'label' present (object #%d)!" % index)
        label = d["label"]

        # bbox
        if "bbox" not in d:
            raise Exception("No 'bbox' present (object #%d)!" % index)
        bbox = cls._bbox_from_dict(index, d["bbox"])

        # polygon
        if "polygon" not in d:
            raise Exception("No 'polygon' present (object #%d)!" % index)
        polygon = cls._polygon_from_dict(index, d["polygon"])

        # meta-data (optional)
        meta = None
        if "meta" in d:
            meta = d["meta"]

        return ObjectPrediction(score=score, label=label, bbox=bbox, polygon=polygon, meta=meta)

    @classmethod
    def _from_dict(cls, d: Dict) -> 'ObjectPredictions':
        """
        Turns the dictionary into predictions.

        :param d: the dictionary to process
        :type d: dict
        :return: the predictions
        :rtype: ObjectPredictions
        """
        # general
        if d is None:
            raise Exception("Expected dictionary, but got None!")
        if not isinstance(d, dict):
            raise Exception("Expected dictionary, but got: %s" % str(type(d)))

        # timestamp
        if "timestamp" not in d:
            raise Exception("No 'timestamp' present!")
        timestamp = d["timestamp"]

        # id
        if "id" not in d:
            raise Exception("No 'id' present!")
        id_ = d["id"]

        # objects
        if "objects" not in d:
            raise Exception("No 'objects' property!")
        objs = []
        for i, d_obj in enumerate(d["objects"]):
            objs.append(cls._object_from_dict(i, d_obj))

        # meta-data (optional)
        meta = None
        if "meta" in d:
            meta = d["meta"]

        return ObjectPredictions(id=id_, timestamp=timestamp, objects=objs, meta=meta)

    @classmethod
    def from_json_string(cls, s: str) -> 'ObjectPredictions':
        """
        Loads the object predictions from the provided string.

        :param s: the string to read from
        :type s: str
        :return: the predictions
        :rtype: ObjectPredictions
        """
        return cls._from_dict(json.loads(s))

    @classmethod
    def load_json_from_file(cls, path: str) -> 'ObjectPredictions':
        """
        Loads the object predictions from the file.

        :param path: the file to read from
        :type path: str
        :return: the predictions
        :rtype: ObjectPredictions
        """
        if ORJSON:
            with open(path, "rb") as fp:
                return cls._from_dict(json.loads(fp.read()))
        else:
            with open(path, "r") as fp:
                return cls._from_dict(json.load(fp))

    @classmethod
    def read_json_from_stream(cls, stream) -> 'ObjectPredictions':
        """
        Loads the object predictions from the stream.

        :param stream: the stream to read from (file-like object)
        :return: the predictions
        :rtype: ObjectPredictions
        """
        if ORJSON:
            return cls._from_dict(json.loads(stream.read()))
        else:
            return cls._from_dict(json.load(stream))
