"""Read public installed metadata; never import SDK/transports or authorize GO."""
import hashlib
import importlib.metadata
import json
import re
from canary_controls import GateError

PACKAGES=('openhands-sdk','openhands-tools','litellm','httpx','httpcore',
          'aiohttp','tenacity','pydantic','anyio')


def inventory(distribution=importlib.metadata.distribution):
    try:
        records=[]
        for name in PACKAGES:
            dist=distribution(name);version=dist.version;metadata=dist.read_text('METADATA')
            if (type(version) is not str or len(version)>64 or
                re.fullmatch(r'[0-9]+(?:\.[0-9]+){1,3}',version) is None or
                type(metadata) is not str or not 0<len(metadata.encode())<=1048576 or
                (name.startswith('openhands-') and version!='1.53.0')):
                raise GateError('invalid_metadata')
            records.append({'name':name,'version':version,
                            'metadata_sha256':hashlib.sha256(metadata.encode()).hexdigest()})
        return {'schema':'obs.sdk.dependencies.v1','operational_go':False,'packages':records}
    except Exception:
        raise GateError('dependency_inventory_invalid') from None


if __name__=='__main__':
    print(json.dumps(inventory(),sort_keys=True))
