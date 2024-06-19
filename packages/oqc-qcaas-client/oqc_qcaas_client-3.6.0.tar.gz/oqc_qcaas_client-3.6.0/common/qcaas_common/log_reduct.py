import logging


class RedactingFilter(logging.Filter):
    def __init__(self, patterns):
        super(RedactingFilter, self).__init__()
        self._patterns = patterns

    def filter(self, record):
        record.msg = self.redact(record.msg)
        if isinstance(record.args, dict):
            for k in record.args.keys():
                record.args[k] = self.redact(record.args[k])
        else:
            record.args = tuple(self.redact(arg) for arg in record.args)
        return True

    def redact(self, msg):
        msg = isinstance(msg, str) and msg or str(msg)
        for pattern in self._patterns:
            if pattern in msg:
                msg = (
                    msg.split(pattern)[0]
                    + f"<<Reducted>> << Information:{pattern} >> <<ALERT>>"
                )
        return msg
