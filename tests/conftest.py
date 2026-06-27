"""
Pytest configuration for Crypto-Journey tests.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        'plaintext': "Hello, World!",
        'key': b'test-key-123',
        'key_str': 'test-key',
        'long_text': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10,
        'unicode_text': "سلام دنیا! 🌍✨ こんにちは 你好",
        'special_chars': "!@#$%^&*()_+-=[]{}|;':,.<>?/~`"
    }


@pytest.fixture
def crypt_instance():
    """Create a default crypt instance for testing."""
    from src.try_26 import ASA_Crypt
    return ASA_Crypt(b'test-key-123')


@pytest.fixture
def crypt_configs():
    """Provide different crypt configurations."""
    return [
        {'cuckoo_num_segments': 2, 'cuckoo_bucket_count': 128},
        {'cuckoo_num_segments': 8, 'cuckoo_bucket_count': 512},
        {'cuckoo_fingerprint_bits': 8},
        {'cuckoo_fingerprint_bits': 16},
        {'cuckoo_bucket_size': 2},
        {'cuckoo_bucket_size': 8},
    ]


@pytest.fixture
def all_versions():
    """Import all versions for testing."""
    versions = {}
    try:
        from src.try_1 import encrypt as e1, decrypt as d1
        versions['try_1'] = {'encrypt': e1, 'decrypt': d1}
    except:
        pass
    
    try:
        from src.try_5 import encrypt as e5, decrypt as d5
        versions['try_5'] = {'encrypt': e5, 'decrypt': d5}
    except:
        pass
    
    try:
        from src.try_10 import encrypt as e10, decrypt as d10
        versions['try_10'] = {'encrypt': e10, 'decrypt': d10}
    except:
        pass
    
    try:
        from src.try_15 import ASA_Crypt as C15
        versions['try_15'] = {'class': C15}
    except:
        pass
    
    try:
        from src.try_19 import ASA_Crypt as C19
        versions['try_19'] = {'class': C19}
    except:
        pass
    
    try:
        from src.try_21 import ASA_Crypt as C21
        versions['try_21'] = {'class': C21}
    except:
        pass
    
    try:
        from src.try_23 import ASA_Crypt as C23
        versions['try_23'] = {'class': C23}
    except:
        pass
    
    try:
        from src.try_26 import ASA_Crypt as C26
        versions['try_26'] = {'class': C26}
    except:
        pass
    
    return versions