import re
import sys


class AADLToIntermediate:
    def __init__(self):
        self.IN_COMPONENT = 0
        self.IN_FEATURES = 1
        self.IN_MODES = 2
        self.IN_PROPERTIES = 3
        self.IN_SUBCOMPONENTS = 4
        self.IN_CONNECTIONS = 5
        self.AWAITING_COMPONENT = 6

        self.package_match = re.compile("package  *([^ ]*)")
        self.system_extends_match = re.compile("system  *([^ ]*)  *extends  *([^ ]*)")
        self.system_match = re.compile("system  *([^ ]*)")
        self.system_implementation_match = re.compile("system implementation *([^.]*)\.(.*)")
        self.system_implementation_extends_match = re.compile("system implementation *([^.]*)\.(.*)  *extends (.*)")
        self.device_match = re.compile("device  *([^ ]*)")
        self.device_implementation_match = re.compile("device implementation *([^.]*)\.(.*)")
        self.device_implementation_extends_match = re.compile("device implementation *([^.]*)\.(.*)  *extends (.*)")
        self.bus_match = re.compile("bus  *([^ ]*)")
        self.bus_implementation_match = re.compile("bus implementation *([^.]*)\.(.*)")
        self.bus_implementation_extends_match = re.compile("bus implementation *([^.]*)\.(.*)  *extends (.*)")
        self.data_match = re.compile("data  *([^ ]*)")
        self.data_implementation_match = re.compile("data implementation *([^.]*)\.(.*)")
        self.data_implementation_extends_match = re.compile("data implementation *([^.]*)\.(.*)  *extends (.*)")
        self.end_match = re.compile("end  *(.*);")

        self.property_match = re.compile("([^ ]*)  *=>  *(.*)")

        self.end_comment_match = re.compile("(.*) -- .*")
        pass

    @staticmethod
    def convert_name(name):
        if "." in name:
            parts = name.split(".", 1)
            name = AADLToIntermediate.convert_name(parts[0])+"_"+AADLToIntermediate.convert_name(parts[1])
        elif name == name.upper():
            name = name[0]+name[1:].lower()

        name = name.replace(".", "_")
        return name

    def convert_file(self, in_filename, out_filename):
        current_component = ""
        mode = self.AWAITING_COMPONENT

        in_file = open(in_filename, "r")
        out_file = open(out_filename, "w")

        created_properties_group = False
        model_name = {}

        for line in in_file:
            line = line.strip()

            if line.startswith("--"):
                continue

            m = self.end_comment_match.match(line)
            if m is not None:
                line = m.group(1)

            m = self.package_match.match(line)
            if m is not None:
                model_name = self.convert_name(m.group(1))
                out_file.write("model {} of Intermediate at \"Intermediate.4ml\"\n{}\n".format(model_name, "{"))
                continue

            m = self.system_implementation_extends_match.match(line)
            if m is not None:
                name = m.group(1)
                extension = m.group(2)
                parent = m.group(3)
                parent_component = self.convert_name(parent)
                current_component = self.convert_name(name)+"_"+extension
                created_properties_group = False
                out_file.write("  {} is Component(\"{}\").\n".format(current_component, current_component))
                out_file.write("  Inherit({}, {}).\n".format(parent_component, current_component))
                continue

            m = self.system_implementation_match.match(line)
            if m is not None:
                name = m.group(1)
                extension = m.group(2)
                parent_component = self.convert_name(name)
                current_component = parent_component+"_"+extension
                created_properties_group = False
                out_file.write("  {} is Component(\"{}\").\n".format(current_component, current_component))
                out_file.write("  Inherit({}, {}).\n".format(parent_component, current_component))
                continue

            m = self.system_extends_match.match(line)
            if m is not None:
                name = self.convert_name(m.group(1))
                current_component = name
                created_properties_group = False
                parent = self.convert_name(m.group(2))
                out_file.write("  {} is Component(\"{}\").\n  Inherit({},{}).\n".format(current_component, current_component, parent, current_component))
                continue

            m = self.system_match.match(line)
            if m is not None:
                name = self.convert_name(m.group(1))
                current_component = name
                created_properties_group = False
                out_file.write("  {} is Component(\"{}\").\n".format(name, name))
                continue

            m = self.device_implementation_extends_match.match(line)
            if m is not None:
                name = m.group(1)
                extension = m.group(2)
                parent = m.group(3)
                parent_component = self.convert_name(parent)
                current_component = self.convert_name(name)+"_"+extension
                created_properties_group = False
                out_file.write("  {} is Component(\"{}\").\n".format(current_component, current_component))
                out_file.write("  Inherit({}, {}).\n".format(parent_component, current_component))
                continue

            m = self.device_implementation_match.match(line)
            if m is not None:
                name = m.group(1)
                extension = m.group(2)
                parent_component = self.convert_name(name)
                current_component = parent_component+"_"+extension
                created_properties_group = False
                out_file.write("  {} is Component(\"{}\").\n".format(current_component, current_component))
                out_file.write("  Inherit({}, {}).\n".format(parent_component, current_component))
                continue

            m = self.device_match.match(line)
            if m is not None:
                name = self.convert_name(m.group(1))
                current_component = name
                created_properties_group = False
                out_file.write("  {} is Component(\"{}\").\n".format(name, name))
                continue

            m = self.bus_implementation_extends_match.match(line)
            if m is not None:
                name = m.group(1)
                extension = m.group(2)
                parent = m.group(3)
                parent_component = self.convert_name(parent)
                current_component = self.convert_name(name)+"_"+extension
                created_properties_group = False
                out_file.write("  {} is Component(\"{}\").\n".format(current_component, current_component))
                out_file.write("  Inherit({}, {}).\n".format(parent_component, current_component))
                continue

            m = self.bus_implementation_match.match(line)
            if m is not None:
                name = m.group(1)
                extension = m.group(2)
                parent_component = self.convert_name(name)
                current_component = parent_component+"_"+extension
                created_properties_group = False
                out_file.write("  {} is Component(\"{}\").\n".format(current_component, current_component))
                out_file.write("  Inherit({}, {}).\n".format(parent_component, current_component))
                continue

            m = self.bus_match.match(line)
            if m is not None:
                name = self.convert_name(m.group(1))
                current_component = name
                created_properties_group = False
                out_file.write("  {} is Component(\"{}\").\n".format(name, name))
                continue

            m = self.data_implementation_extends_match.match(line)
            if m is not None:
                name = m.group(1)
                extension = m.group(2)
                parent = m.group(3)
                parent_component = self.convert_name(parent)
                current_component = self.convert_name(name)+"_"+extension
                created_properties_group = False
                out_file.write("  {} is Component(\"{}\").\n".format(current_component, current_component))
                out_file.write("  Inherit({}, {}).\n".format(parent_component, current_component))
                continue

            m = self.data_implementation_match.match(line)
            if m is not None:
                name = m.group(1)
                extension = m.group(2)
                parent_component = self.convert_name(name)
                current_component = parent_component+"_"+extension
                created_properties_group = False
                out_file.write("  {} is Component(\"{}\").\n".format(current_component, current_component))
                out_file.write("  Inherit({}, {}).\n".format(parent_component, current_component))
                continue

            m = self.data_match.match(line)
            if m is not None:
                name = self.convert_name(m.group(1))
                current_component = name
                created_properties_group = False
                out_file.write("  {} is Component(\"{}\").\n".format(name, name))
                continue

            m = self.end_match.match(line)
            if m is not None:
                current_component = ""
                mode = self.AWAITING_COMPONENT
                name = self.convert_name(m.group(1))
                if name == model_name:
                    out_file.write("}")
                else:
                    out_file.write("\n")
                continue

            if line == "features":
                mode = self.IN_FEATURES
                continue

            if line == "modes":
                mode = self.IN_MODES
                continue

            if line == "properties":
                mode = self.IN_PROPERTIES
                continue

            if line == "subcomponents":
                mode = self.IN_SUBCOMPONENTS
                continue

            if line == "connections":
                mode = self.IN_CONNECTIONS
                continue

            if line.endswith(";"):
                line = line[:len(line) - 1]

            if mode == self.IN_FEATURES:
                if line.endswith(";"):
                    line = line[:len(line)-1]

                parts = line.split(":", 1)
                if len(parts) == 1:
                    print("Unexpected line: {}".format(line))
                    continue

                feature_name = parts[0].strip()
                full_feature_name = current_component+"_"+parts[0].strip()
                keywords = parts[1].strip().split(" ")
                t = "out"
                if "in" in keywords:
                    keywords.remove("in")
                    if "out" in keywords:
                        keywords.remove("out")
                        t = "inout"
                    else:
                        t = "in"
                elif "out" in keywords:
                    keywords.remove("out")

                is_event = False
                if "event" in keywords:
                    is_event = True
                    keywords.remove("event")

                is_data = False
                if "data" in keywords:
                    is_data = True
                    keywords.remove("data")

                has_bus_access = False
                if "bus" in keywords and "access" in keywords:
                    has_bus_access = True
                    keywords.remove("bus")
                    keywords.remove("access")

                if len(keywords) > 2:
                    print("Unaccounted-for keywords in "+line)
                    continue

                data_type = ""
                if len(keywords) == 2:
                    data_type = keywords[1]

                if "requires" in keywords:
                    out_file.write("  Requires({}, {}).\n".format(
                        current_component, self.convert_name(keywords[-1])
                    ))
                    out_file.write("  {} is Port({}, \"{}\").\n".format(
                        full_feature_name, current_component, feature_name))
                    out_file.write("  PortType({}, \"{}\", \"{}\").\n".format(
                        full_feature_name, t, data_type))
                elif "port" in keywords:
                    out_file.write("  {} is Port({}, \"{}\").\n".format(
                        full_feature_name, current_component, feature_name))
                    out_file.write("  PortType({}, \"{}\", \"{}\").\n".format(
                        full_feature_name, t, data_type))
                else:
                    print("Unrecognized keywords in {}".format(line))
            elif mode == self.IN_MODES:
                parts = line.strip().split(":", 1)
                if len(parts) == 1:
                    print("Unexpected line: {}".format(line))
                    continue

                keywords = parts[1].strip().split(" ")
                is_initial = False
                if "initial" in keywords:
                    is_initial = True
                    keywords.remove("initial")

                if len(keywords) > 1:
                    print("Unexpected mode keywords in "+line)
                    continue

                mode_name = current_component+"_"+parts[0].strip()+"_mode"
                out_file.write("  {} is Condition({}, \"{}\").\n".format(
                    mode_name, current_component, keywords[0]
                ))
                if is_initial:
                    out_file.write("  InitialCondition({},{}).\n".format(
                        current_component, mode_name
                    ))
            elif mode == self.IN_PROPERTIES:
                if not created_properties_group:
                    out_file.write("  {}_props is AttributeGroup({}, \"Properties\").\n".format(
                        current_component, current_component
                    ))
                    created_properties_group = True

                m = self.property_match.match(line)
                if m is None:
                    print("Unexpected property line: "+line)
                    continue

                prop_name = self.convert_name(m.group(1))
                prop_value = m.group(2)
                if prop_value.startswith("(reference"):
                    print("Skipping reference in: "+line)
                    continue

                out_file.write("  Attribute({}_props, \"{}\", {}).\n".format(
                    current_component, prop_name, prop_value
                ))

            elif mode == self.IN_SUBCOMPONENTS:
                parts = line.strip().split(":", 1)

                if len(parts) == 1:
                    print("Unexpected line: {}".format(line))
                    continue

                subcomponent_name = self.convert_name(parts[0].strip())

                keywords = parts[1].strip().split(" ")
                is_data = False
                if "data" in keywords:
                    is_data = True
                    keywords.remove("data")

                is_bus = False
                if "bus" in keywords:
                    is_bus = True
                    keywords.remove("bus")

                is_system = False
                if "system" in keywords:
                    is_system = True
                    keywords.remove("system")

                if len(keywords) != 1:
                    print("Unexpected keywords in: "+line)
                    continue

                if is_data:
                    out_file.write("  {} is Port({}, \"{}\").\n".format(
                        current_component+"_"+subcomponent_name, current_component, subcomponent_name))
                    out_file.write("  PortType({}, \"data\", \"{}\").\n".format(
                        current_component + "_" + subcomponent_name, keywords[0]))
                else:
                    out_file.write("  {} is Subcomponent({}, \"{}\", {}).\n".format(
                        current_component+"_"+subcomponent_name, current_component, subcomponent_name, self.convert_name(keywords[0])))

            elif mode == self.IN_CONNECTIONS:
                parts = line.strip().split(":", 1)

                if len(parts) == 1:
                    print("Unexpected line: {}".format(line))
                    continue

                connection_name = self.convert_name(parts[0].strip())

                keywords = parts[1].strip().split(" ")
                is_data = False
                if "data" in keywords:
                    is_data = True
                    keywords.remove("data")

                is_bus = False
                if "bus" in keywords and "access" in keywords:
                    is_bus = True
                    keywords.remove("bus")
                    keywords.remove("access")

                is_port = False
                if "port" in keywords:
                    is_port = True
                    keywords.remove("port")

                if "->" in keywords:
                    keywords.remove("->")

                if "<->" in keywords:
                    keywords.remove("<->")

                if len(keywords) != 2:
                    print("Unexpected keywords in: "+line)
                    continue

                if is_port:
                    from_parts = keywords[0].split(".", 1)
                    if len(from_parts) == 1:
                        from_parts = [current_component, keywords[0]]
                    to_parts = keywords[1].split(".", 1)
                    if len(to_parts) == 1:
                        to_parts = [current_component, keywords[1]]

                    out_file.write("  PortConnection({}, \"{}\", \"{}\", \"{}\", \"{}\", \"{}\").\n".format(
                        current_component, connection_name, from_parts[0], from_parts[1],
                        to_parts[0], to_parts[1]
                    ))
                elif is_bus:
                    from_parts = keywords[0].split(".", 1)
                    if len(from_parts) == 1:
                        from_parts = [current_component, keywords[0]]
                    if "." in keywords[1]:
                        to_parts = keywords[1].split(".", 1)
                        if len(to_parts) == 1:
                            to_parts = [current_component, keywords[1]]
                        out_file.write("  PortConnection({}, \"{}\", \"{}\", \"{}\", \"{}\", \"{}\").\n".format(
                            current_component, connection_name, from_parts[0], from_parts[1],
                            to_parts[0], to_parts[1]
                        ))
                    else:
                        to_name = current_component + "_" + self.convert_name(keywords[1])
                        out_file.write("  BusConnection({}, \"{}\", \"{}\", \"{}\", {}).\n".format(
                            current_component, connection_name, from_parts[0], from_parts[1],
                            to_name))
                else:
                    from_name = self.convert_name(keywords[0])
                    to_name = current_component + "_" + self.convert_name(keywords[1])
                    out_file.write("  Connection({}, {}, {}, {}).\n".format(
                        current_component, connection_name, from_name, to_name))





        in_file.close()
        out_file.close()


if len(sys.argv) < 3:
    print("format is: {} aadl-file output-4ml-file".format(sys.argv[0]))
else:
    aadl = AADLToIntermediate()
    aadl.convert_file(sys.argv[1], sys.argv[2])
