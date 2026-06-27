# 📝 Changelog

All notable changes to the Crypto-Journey project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-06-28

### 🎉 Major Release: Cuckoo Filter Integration

#### Added
- **Cuckoo Filter Implementation** (try_25, try_26)
  - Low false positive rate (~0.01%)
  - Configurable parameters (segments, buckets, fingerprint bits)
  - Auto-rotation of segments
  - Statistics tracking (total_checks, detected)
- **Blake2b Keystream** (try_26)
  - Better performance than Blake2s
  - Larger digest size (64 bytes vs 32 bytes)
- **Enhanced Nonce Processing**
  - HMAC-based nonce transformation
  - Better diffusion in keystream
- **Configuration Options**
  - Customizable salt/nonce/hmac sizes
  - Configurable block sizes
  - Flexible cuckoo filter parameters

#### Changed
- Updated header format for better compatibility
- Improved error handling in decrypt
- Better code documentation with type hints

#### Deprecated
- None

#### Removed
- None

#### Fixed
- Fixed random import in try_25 (now uses secrets)
- Fixed keystream index overflow in try_24
- Improved HMAC comparison timing safety
- Fixed Blake2s key length issue in try_20 and try_21

#### Security
- Added constant-time HMAC comparison
- Better key derivation with HMAC-based nonce processing

## [1.5.0] - 2024-06-20

### 🔧 Enhancement Release

#### Added
- Auto-reset bitmap (try_23)
- Enhanced keystream with nonce processing (try_24)
- Statistics tracking for bitmap usage
- Configuration options for bitmap reset

#### Changed
- Improved performance of bitmap operations
- Better memory management

#### Fixed
- Fixed bitmap index calculation
- Fixed tag ordering for reset

## [1.0.0] - 2024-06-15

### 🎉 Initial Release: The Complete Journey

#### Added
- All 26 versions from try_1 to try_26
- Complete documentation for each version
- Evolution timeline and comparison matrix
- Examples and test suite
- Apache 2.0 License

#### Features
- **try_1-try_6**: Basic encryption concepts
- **try_7-try_10**: Key derivation + Authentication
- **try_11-try_18**: Advanced KDF + Class-based architecture
- **try_19-try_21**: Replay protection (set/bitmap)
- **try_22-try_24**: Enhanced keystream + Auto-reset
- **try_25-try_26**: Cuckoo Filter + Blake2b

#### Known Issues
- try_18 has a known bug (using dict instead of set)
- try_20 limited set may miss replays after 100 messages

## [0.5.0] - 2024-06-01

### 🚧 Beta Release

#### Added
- First 20 versions
- Basic documentation
- Example usage
- Test coverage for try_19-try_21

#### Changed
- Improved code structure
- Better error messages

#### Fixed
- Fixed set bug in try_18
- Fixed header comparison in try_19

## [0.1.0] - 2024-05-15

### 🎬 Initial Development

#### Added
- First version (try_1) - Basic sum encryption
- Project structure
- README draft