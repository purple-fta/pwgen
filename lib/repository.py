# TODO Docs
import json
import os



class Repository:
    @staticmethod
    def save(path: str, service_name: str, n: int, s: bool, i: int):
        if os.path.isfile(path):
            with open(path, 'r') as f:
                data = json.load(f)
                data[service_name] = {
                    'n': n,
                    's': s,
                    'i': i
                }
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)
        else:
            data = { service_name:
                {
                    'n': n,
                    's': s,
                    'i': i
                }
            }

            with open(path, 'x') as f:
                json.dump(data, f, indent=4)

    @staticmethod
    def load(path: str):
        if os.path.isfile(path):
            with open(path, 'r') as f:
                data = json.load(f)
                
                return data
        else:
            return {}

