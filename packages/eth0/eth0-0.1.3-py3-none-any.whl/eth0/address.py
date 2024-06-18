#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
#
# Copyright (c) Jarkko Sakkinen 2024

import secrets

from eth_keys import keys


def main_cli():
    private_key = secrets.token_bytes(32)
    public_key = keys.PrivateKey(private_key).public_key
    address = public_key.to_checksum_address()

    print(f"{private_key.hex()} {address}")


if __name__ == "__main__":
    main_cli()
