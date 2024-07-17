from rosidl_adapter.parser import parse_message_string, parse_service_string
from rosidl_runtime_py import get_interface_path


def stringify_field_msg_types(root_type):
    definition = ""
    seen_types = set()
    deps = [root_type]
    is_root = True
    while deps:
        ty = deps.pop()
        parts = ty.split("/")
        if not is_root:
            definition += "\n================================================================================\n"
            definition += f"MSG: {ty}\n"
        is_root = False

        msg_name = parts[2] if len(parts) == 3 else parts[1]
        interface_name = ty if len(parts) == 3 else f"{parts[0]}/msg/{parts[1]}"
        with open(get_interface_path(interface_name), encoding="utf-8") as msg_file:
            msg_definition = msg_file.read()
        definition += msg_definition

        spec = parse_message_string(parts[0], msg_name, msg_definition)

        for field in spec.fields:
            is_builtin = field.type.pkg_name is None
            if not is_builtin:
                field_ty = f"{field.type.pkg_name}/{field.type.type}"
                if field_ty not in seen_types:
                    deps.append(field_ty)
                    seen_types.add(field_ty)

    return definition

def stringify_field_srv_types(root_type):
    definition = ""
    seen_types = set()
    deps = [root_type]
    is_root = True

    while deps:

        ty = deps.pop()
        parts = ty.split("/")
        if not is_root:
            definition += "\n================================================================================\n"
            definition += f"MSG: {ty}\n"
        
        msg_name = parts[2] if len(parts) == 3 else parts[1]

        if is_root:
            interface_name = ty if len(parts) == 3 else f"{parts[0]}/srv/{parts[1]}"
        else:
            interface_name = ty if len(parts) == 3 else f"{parts[0]}/msg/{parts[1]}"

        with open(get_interface_path(interface_name), encoding="utf-8") as msg_file:
            msg_definition = msg_file.read()
        definition += msg_definition

        if is_root:
            spec = parse_service_string(parts[0], msg_name, msg_definition)
        else:
            spec = parse_message_string(parts[0], msg_name, msg_definition)

        if is_root:
            for field in spec.response.fields:
                is_builtin = field.type.pkg_name is None
                if not is_builtin:
                    field_ty = f"{field.type.pkg_name}/{field.type.type}"
                    if field_ty not in seen_types:
                        deps.append(field_ty)
                        seen_types.add(field_ty)

            for field in spec.request.fields:
                is_builtin = field.type.pkg_name is None
                if not is_builtin:
                    field_ty = f"{field.type.pkg_name}/{field.type.type}"
                    if field_ty not in seen_types:
                        deps.append(field_ty)
                        seen_types.add(field_ty)

        else:
            for field in spec.fields:
                is_builtin = field.type.pkg_name is None
                if not is_builtin:
                    field_ty = f"{field.type.pkg_name}/{field.type.type}"
                    if field_ty not in seen_types:
                        deps.append(field_ty)
                        seen_types.add(field_ty)

        is_root = False

    return definition