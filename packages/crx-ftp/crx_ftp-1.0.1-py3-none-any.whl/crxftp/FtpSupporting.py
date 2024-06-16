from json import loads, dumps

async def read_json(file_content):
    file_data = loads(file_content)
    return file_data

async def write_json(data):
    return dumps(data, ensure_ascii=False, indent=2)

async def get_extension(file_name):
    return file_name.split(".")[-1]

async def process_read_data(remote_file, data):
    file_extension = await get_extension(remote_file)
    if file_extension == "json":
        return await read_json(data)
    elif file_extension == "txt":
        return data

async def process_write_data(remote_file, data):
    file_extension = await get_extension(remote_file)
    if file_extension == "json":
        return await write_json(data)
    elif file_extension == "txt":
        return data
