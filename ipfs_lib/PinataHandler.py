import requests
import os

import options.prime as opt


class PinataHandler:
    def __init__(self):
        self.PUBLIC_API_KEY = opt.pinata_public_key
        self.PRIVATE_API_KEY = opt.pinata_private_key
        self.headers = {"pinata_api_key": self.PUBLIC_API_KEY, "pinata_secret_api_key": self.PRIVATE_API_KEY}

    def pin_files(self):
        endpoint = "https://api.pinata.cloud/"
        api_suffix = "pinning/pinFileToIPFS"

        pinata_options = {'pinataOptions': '{"cidVersion":0,"wrapWithDirectory":false}'}

        ipfs_directory = opt.ipfs_directory_name

        files = []
        for file in os.listdir("Scratch/IMG"):
            t = ('file', (f'{ipfs_directory}/{file}', open(f'Scratch/IMG/{file}', "rb")))
            files.append(t)

        files = tuple(files)

        res = requests.post(endpoint + api_suffix, files=files, headers=self.headers, data=pinata_options)

        return res.json()['IpfsHash']

    def pin_json(self):
        endpoint = "https://api.pinata.cloud/"
        api_suffix = "pinning/pinFileToIPFS"

        pinata_options = {'pinataOptions': '{"cidVersion":0,"wrapWithDirectory":false}'}

        ipfs_directory = opt.ipfs_directory_name

        files = []
        for file in os.listdir("Scratch/JSON"):
            t = ('file', (f'{ipfs_directory}/{file}', open(f'Scratch/JSON/{file}', "rb")))
            files.append(t)

        files = tuple(files)

        res = requests.post(endpoint + api_suffix, files=files, headers=self.headers, data=pinata_options)

        return res.json()['IpfsHash']


