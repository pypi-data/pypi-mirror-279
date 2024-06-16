from aioftp import Client, errors
from .FtpSupporting import *


class FTPManager:

    def __init__(self, host, port=21, user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.client = None

    async def create_file(self, local_file: str, remote_path: str):
        """
        :param local_file: The path to the file on your system
        :param remote_path: Remote path on the FTP server
        """
        async with Client.context(self.host, self.port, self.user, self.password) as client:
            await client.upload(local_file, remote_path)

    async def read_file(self, remote_file: str):
        """
        :param remote_file: Remote file on the FTP server
        """
        try:
            async with Client.context(self.host, self.port, self.user, self.password) as client:
                async with client.download_stream(remote_file) as stream: 
                    existing_data_bytes = await stream.read()
                    existing_data = existing_data_bytes.decode('utf-8')
                    return await process_read_data(remote_file, existing_data)
        except errors.StatusCodeError as e:
            print(e.info)

    async def update_file(self, remote_file, updated_data):
        """
        :param remote_file: Remote file on the FTP server
        :param updated_data: Updated new data
        """
        await self.delete_file(remote_file)
        async with Client.context(self.host, self.port, self.user, self.password) as client:
            uploaded_data = await process_write_data(remote_file, updated_data)
            async with client.upload_stream(remote_file) as stream:
                await stream.write(uploaded_data.encode("utf-8"))

    async def delete_file(self, remote_file):
        """
        :param remote_file: Remote file on the FTP server
        """
        async with Client.context(self.host, self.port, self.user, self.password) as client:
            await client.remove(remote_file)
