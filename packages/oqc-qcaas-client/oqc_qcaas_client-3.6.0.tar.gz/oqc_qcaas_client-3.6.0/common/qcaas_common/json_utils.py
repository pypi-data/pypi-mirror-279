from datetime import datetime, time
from json import JSONEncoder


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S%z")
        elif isinstance(obj, time):
            return obj.strftime("%H:%M:%S%z")

        return super().default(obj)

    @classmethod
    def _get_datetime_from_json_string(cls, s: str):
        time_format = "%Y-%m-%d %H:%M:%S"
        return datetime.strptime(s, time_format)
