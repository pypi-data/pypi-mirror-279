import json

def generate_schema(json_data, depth=None):

    if not json_data:
        return None
    # 解析JSON对象
    data = json.loads(json_data)

    # 递归生成JSON架构
    def generate_subschema(data, depth=None):
        if depth is not None and depth <=0:
            return {
                "type": type(data).__name__
            }
        subDepth = depth -1 if depth is not None else None
        subschema = {}
        if isinstance(data, dict):
            # for key, value in data.items():
            for key in sorted(data.keys()):
                value = data[key]
                if isinstance(value, (dict, list)):
                    subschema[key] = generate_subschema(value, depth=subDepth)
                else:
                    subschema[key] = {"type": type(value).__name__}

            return {
                "type": type(data).__name__,
                "properties": subschema,
                "required": sorted(data.keys())
            }
        elif isinstance(data, list):
            if data:
                d1 = data[0]
                subschema = generate_subschema(d1, depth=subDepth)
            else:
                subschema = None
            return {
                "type": type(data).__name__,
                "properties": subschema
                # "required": list(data.keys())
            }
        else:
            return {
                "type": type(data).__name__
            }

    # 生成最终的JSON架构
    schema = generate_subschema(data, depth=depth)

    return schema

if __name__ == '__main__':
    # 给定JSON对象
    json_data = """ [{
        "name": "John",
        "age": 30,
        "city": "New York",
        "a": [
            {
                "a1": 11,
                "a2": {
                    "a11": "eeee"
                }
            }
        ]
    } ]"""

    # 生成JSON对象的架构
    schema = generate_schema(json_data, depth=None)

    # 打印生成的JSON架构
    print(json.dumps(schema, indent=4))