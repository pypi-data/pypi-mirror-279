# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Python module used for handling zone controller specifications"""
from ruamel.yaml import YAML
from pybuild.lib import logger
from pybuild.interface.base import BaseApplication

LOGGER = logger.create_logger("base")


class BadYamlFormat(Exception):
    """Exception to raise when in/out signal is not defined."""
    def __init__(self, message):
        self.message = message


class ZCAL(BaseApplication):
    """Zone controller abstraction layer"""

    def __repr__(self):
        """String representation of ZCAL"""
        return (
            f"<ZCAL {self.name}"
            f" app_side insignals: {len(self.signal_names['other']['insignals'])}"
            f" app_side outsignals: {len(self.signal_names['other']['outsignals'])}>"
        )

    def __init__(self, base_application):
        """Create the interface object

        Currently, there is no verification that the signal is used.

        TODO: Check if the signal is a set or a get somewhere. Maybe in here.

        Args:
            base_application (BaseApplication): Primary object of an interface
                                                Usually a raster, but can be an application or a model too.
        """
        self.name = ""
        self.zc_translations = {}
        self.composition_spec = {}
        self.signal_names = {}
        self.e2e_sts_signals = set()
        self.update_bit_signals = set()
        self.clear_signal_names()
        self.interface_enums = set()
        self.base_application = base_application
        self.translations_files = []
        self.device_domain = base_application.get_domain_mapping()
        self.signal_primitives_list = set()

    @staticmethod
    def read_translation_files(translation_files, keys=None):
        """ Searches translation files (yaml) for given keys at top level. Raises an
        error if conflicting configurations are found among the files. Return a dict
        containing the aggregated data found in the translation files for the keys
        provided in the function call.

        Args:
            translation_files (list): List of paths to files to search.
            keys (list): List of keys to search among translation files for (all present keys by default).

        Returns:
            specs (dict): Dictionary containing provided keys with the aggregated data
            stored under those keys in translation files.
        """

        specs = {}
        for translation_file in translation_files:
            with open(translation_file, encoding="utf-8") as translation:
                yaml = YAML(typ='safe', pure=True)
                raw = yaml.load(translation)
                used_keys = raw.keys() if keys is None else keys
                for key in used_keys:
                    new_elements = raw.get(key, None)
                    if isinstance(new_elements, list):
                        specs[key] = specs.get(key, []) + new_elements
                    elif isinstance(new_elements, dict):
                        specs[key] = specs.get(key, {})
                        if {**specs[key], **new_elements} != {**new_elements, **specs[key]}:
                            LOGGER.error(
                                "Conflicting configuration found for key '%s' among translation files: %s",
                                key,
                                translation_files,
                            )
                        specs[key].update(new_elements)
        return specs

    def add_signals(self, signals, signal_type="insignal", *args):
        """Add signal names and properties

        Args:
            signals (list(Signals)): Signals to use
            signal_type (str): 'insignals' or 'outsignals'
        """

        type_in_zc = "insignals" if signal_type == "outsignals" else "outsignals"
        for signal in signals:
            if signal.name not in self.zc_translations:
                continue
            LOGGER.debug("Adding signal: %s", signal)
            for translation in self.zc_translations[signal.name]:
                signal_property = translation["property"]
                struct_name = translation["struct_name"]
                self.check_signal_property(struct_name, signal_property, type_in_zc)
                self.signal_names["zc"][type_in_zc].add(signal_property)
                self.signal_names["other"][signal_type].add(signal.name)
        for e2e_sts_signal_name in self.e2e_sts_signals:
            if e2e_sts_signal_name not in self.signal_names["other"]["insignals"]:
                LOGGER.warning("E2E check signal %s not used in any model.", e2e_sts_signal_name)
            else:
                self.signal_names["other"][signal_type].add(e2e_sts_signal_name)
        for update_bit_signal_name in self.update_bit_signals:
            if update_bit_signal_name not in self.signal_names["other"]["insignals"]:
                LOGGER.warning("Update bit signal %s not used in any model.", update_bit_signal_name)
            else:
                self.signal_names["other"][signal_type].add(update_bit_signal_name)
        LOGGER.debug("Registered signal names: %s", self.signal_names)

    def check_signal_property(self, struct_name, property_name, signal_type):
        """Check if we have only one signal written for the same property.

        Args:
            struct_name (str): signal struct name
            property_name (str): signal property
            signal_type (str): insignal or outsignal
        """
        signal_primitive_spec = ".".join([struct_name, property_name, signal_type])
        if signal_primitive_spec in self.signal_primitives_list:
            error_msg = (f"You can't write {property_name} in {struct_name} as"
                         f" {signal_type} since this primitive has been used."
                         " Run model_yaml_verification to identify exact models.")
            raise Exception(error_msg)
        self.signal_primitives_list.add(signal_primitive_spec)

    def parse_definition(self, definition):
        """Parses all translation files and populates class interface data.

        Args:
            definition (list(Path)): Definition files
        """

        raw = self.read_translation_files(definition)
        self.composition_spec = {
            key: raw[key] for key in ("port_interfaces", "data_types", "calls") if key in raw
        }
        ports_info = {}
        for port_name, port in raw.get("ports", {}).items():
            signal_struct = port.get("element", {})
            if signal_struct:
                self.populate_signal_translations(signal_struct)
                ports_info[port_name] = {
                    **self.get_port_info(signal_struct),
                    "interface": port.get("interface")
                }
            else:
                raise Exception(f"Port {port_name} has no element.")
        self.composition_spec["ports"] = ports_info

    @staticmethod
    def get_port_info(signal_struct):
        """Extract port information from signal elements in port. Raises exception
        if signal elements are not exclusively sent in one direction.

        Args:
            signal_struct (dict): Signal dict containing list of signal elements
        Returns:
            port_info (dict): Dict containing port direction and if any elements
            should have an update bit associated with them.
        """
        struct_name = list(signal_struct.keys())[0]
        signal_elements = signal_struct[struct_name]
        update_elements = set()
        direction = None
        for element in signal_elements:
            if "insignal" in element:
                temp_dir = "IN"
            elif "outsignal" in element:
                temp_dir = "OUT"
            else:
                raise BadYamlFormat(f"in/out signal for element in { struct_name } is missing.")
            if direction is not None and direction != temp_dir:
                raise BadYamlFormat(f"Signal { struct_name } has both in and out elements.")
            direction = temp_dir
            if element.get("updateBit", False):
                update_elements.add(struct_name)
        port_info = {"direction": direction}
        if update_elements:
            port_info["enable_update"] = list(update_elements)
        return port_info

    def populate_signal_translations(self, struct_specifications):
        """Populate class translations data.

        Args:
            struct_specifications (dict): Dict with signal structs to/from a port.
        """
        enumerations = self.base_application.enumerations

        struct_name = list(struct_specifications.keys())[0]
        signal_definitions = struct_specifications[struct_name]
        for signal_definition in signal_definitions:
            if "insignal" in signal_definition:
                signal_name = signal_definition["insignal"]
                base_signals = self.base_application.insignals
            elif "outsignal" in signal_definition:
                signal_name = signal_definition["outsignal"]
                base_signals = self.base_application.outsignals
            else:
                raise BadYamlFormat(f"in/out signal for { signal_name } is missing.")
            base_properties = None
            for base_signal in base_signals:
                if signal_name == base_signal.name:
                    matching_base_signal = base_signal
                    base_properties = self.base_application.get_signal_properties(
                        matching_base_signal
                    )
            if base_properties is None:
                raise BadYamlFormat(f"in/out signal for { signal_name } is missing.")

            if base_properties["type"] in enumerations:
                if 'init' in signal_definition:
                    init_value = signal_definition["init"]
                else:
                    if enumerations[base_properties['type']]['default_value'] is not None:
                        init_value = enumerations[base_properties['type']]['default_value']
                    else:
                        LOGGER.warning('Initializing enumeration %s to "zero".', base_properties['type'])
                        init_value = [
                            k for k, v in enumerations[base_properties['type']]['members'].items() if v == 0
                        ][0]
            else:
                init_value = signal_definition.get("init", 0)

            update_bit = signal_definition.get("updateBit", False)
            e2e_status = signal_definition.get("e2eStatus", False)
            group = signal_definition.get("group", struct_name)

            translation = {
                "range": {
                    "min": base_properties.get("min", "-"),
                    "max": base_properties.get("max", "-")
                },
                "offset": base_properties.get("offset", "-"),
                "factor": base_properties.get("factor", "-"),
                "property": signal_definition["property"],
                "init": init_value,
                "struct_name": struct_name,
                "variable_type": base_properties.get("type"),
                "description": base_properties.get("description"),
                "unit": base_properties.get("unit"),
                "debug": base_properties.get("debug", False),
                "dependability": e2e_status,
                "update_bit": update_bit
            }

            if signal_name not in self.zc_translations:
                self.zc_translations[signal_name] = []
            self.zc_translations[signal_name].append(translation)
            if update_bit:
                update_bit_property = f"{struct_name}UpdateBit"
                update_signal_name = f"yVc{group}_B_{update_bit_property}"
                if signal_name == update_signal_name:
                    error_msg = f"Don't put updateBit status signals ({update_signal_name}) in yaml interface files."
                    raise BadYamlFormat(error_msg)
                self.zc_translations[update_signal_name] = [
                    {
                        "property": update_bit_property,
                        "variable_type": "Bool",
                        "property_interface_type": "Bool",
                        "offset": "-",
                        "factor": "-",
                        "range": {
                            "min": "-",
                            "max": "-",
                        },
                        "init": 1,
                        "struct_name": struct_name,
                        "description": f"Update bit signal for signal {struct_name}.",
                        "unit": None,
                        "dependability": False,
                        "update_bit": True
                    }
                ]
                self.update_bit_signals.add(update_signal_name)

            if e2e_status:
                if "outsignal" in signal_definition:
                    error_msg = "E2e status not expected for outsignals"
                    raise BadYamlFormat(error_msg)

                e2e_sts_property = f"{struct_name}E2eSts"
                e2e_sts_signal_name = f"sVc{group}_D_{e2e_sts_property}"

                if signal_name == e2e_sts_signal_name:
                    error_msg = f"Don't put E2E status signals ({e2e_sts_signal_name}) in yaml interface files."
                    raise BadYamlFormat(error_msg)
                if e2e_sts_signal_name not in self.zc_translations:
                    self.zc_translations[e2e_sts_signal_name] = [
                        {
                            "property": e2e_sts_property,
                            "variable_type": "UInt8",
                            "property_interface_type": "UInt8",
                            "offset": 0,
                            "factor": 1,
                            "range": {
                                "min": 0,
                                "max": 255
                            },
                            "init": 255,
                            "struct_name": struct_name,
                            "description": f"E2E status code for E2E protected signal(s) {signal_name}.",
                            "unit": None,
                            "debug": False,
                            "dependability": True,
                            "update_bit": False
                        }
                    ]
                    self.e2e_sts_signals.add(e2e_sts_signal_name)
                else:
                    translation = self.zc_translations[e2e_sts_signal_name][0]
                    translation["description"] = translation["description"][:-1] + f", {signal_name}."

    def clear_signal_names(self):
        """Clear signal names

        Clears defined signal names (but not signal properties).
        """
        self.signal_names = {
            "zc": {"insignals": set(), "outsignals": set()},
            "other": {"insignals": set(), "outsignals": set()}
        }

    def to_dict(self):
        """Method to generate dict to be saved as yaml

        Returns:
            spec (dict): Signalling specification
        """
        spec = {"consumer": [], "producer": []}

        signal_roles = ["consumer", "producer"]
        signal_types = ["insignals", "outsignals"]
        for signal_role, signal_type in zip(signal_roles, signal_types):
            for signal_name in self.signal_names["other"][signal_type]:
                for signal_spec in self.zc_translations[signal_name]:
                    spec[signal_role].append({**signal_spec, "variable": signal_name})

        return spec
