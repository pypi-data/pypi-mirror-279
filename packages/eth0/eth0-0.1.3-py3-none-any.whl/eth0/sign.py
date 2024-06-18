#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
#
# Copyright (c) Jarkko Sakkinen 2024

import os
import sys

from eth_account.messages import defunct_hash_message
from eth_keys import keys


def main_cli():
    private_key_hex = os.getenv("ETHEREUM_PRIVATE_KEY")
    if not private_key_hex:
        sys.exit(1)

    payload = sys.stdin.buffer.read()
    key = keys.PrivateKey(bytes.fromhex(private_key_hex))
    signature = key.sign_msg_hash(defunct_hash_message(payload))

    print(f"{signature.to_hex()}")


if __name__ == "__main__":
    main_cli()
