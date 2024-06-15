from ccdexplorer_schema_parser import ccdexplorer_schema_parser
import json


class Schema:
    def __init__(self, source, version=None):
        """Construct a new schema by extracting it from a module source. The
        module source can be either provided as a serialized versioned module,
        or a pair of a Wasm module together with a version (which can be either
        0 or 1). If the optional `version` argument is supplied then this
        assumes that the `source` is only the Wasm module.

        """
        if version is not None:
            self.schema = ccdexplorer_schema_parser.extract_schema_pair_ffi(
                version, source
            )
        else:
            self.schema = ccdexplorer_schema_parser.extract_schema_ffi(source)

    def event_to_json(self, contractName, eventData):
        response = ccdexplorer_schema_parser.parse_event_ffi(
            self.schema, contractName, eventData
        )
        return json.loads(response)

    def parameter_to_json(self, contractName, functionName, parameterData):
        response = ccdexplorer_schema_parser.parse_parameter_ffi(
            self.schema, contractName, functionName, parameterData
        )
        return json.loads(response)

    def return_value_to_json(self, contractName, functionName, returnValueData):
        response = ccdexplorer_schema_parser.parse_return_value_ffi(
            self.schema, contractName, functionName, returnValueData
        )
        return json.loads(response)
