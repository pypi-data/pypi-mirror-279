"""
Contains helpers for interacting with Skyramp service.
"""


class _Service:
    def __init__(self, name, addr, alias, secure, protocol, credentails) -> None:
        self.name = name
        self.addr = addr
        self.alias = alias
        self.secure = secure
        self.protocol = protocol
        self.credential = credentails

    def to_json(self):
        """
        Convert the service object to json data.
        """
        attributes = ["addr", "alias", "secure", "protocol", "credential"]
        json_data = {
            attr: getattr(self, attr)
            for attr in attributes
            if getattr(self, attr) is not None
        }
        return json_data
