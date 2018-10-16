"""Tests for utility functions and decorators."""

import asyncio
import pytest

from pathshare_api.utilities import encrypt_password, decrypt_password


@pytest.mark.asyncio
async def test_encryption_decryption() -> None:
    """Test that a password is encrypted and decrypted correctly.
    
    Notes
    -----
    There is currently a bug with pytest-asyncio.
    """
    password = "password123123"
    password_data = await encrypt_password(password)
    decrypted_password = await decrypt_password(password_data)
    assert password == decrypted_password
    