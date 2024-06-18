# Changelog
All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-06-06
- Fix bug in `stos` instructions to pull address from `rdi` instead of `edi` (@ddash-ct)
- Dropped support for Python 3.8
- Fixed issue with finding code paths for recursive functions. (#10)
- `Emulator.context_at()` will now raise a `ValueError` (instead of returning None) if no contexts could be made.
- Fixed handling of function calls to import prefixed functions.
- Added new interactive command line shell. (see [documentation](./docs/Shell.md))
- Added ability to provide a callable or opcode to the `end` keyword in `ProcessorContext.execute()`
- Added and updated helpers for context memory:
  - `read_string_bytes()`  - Like `read_string()` but doesn't decode to a string.
  - `read_int()` - Reads bytes as integer of given size.
  - `write_string()` - Can now accept bytes or string value.
  - `write_int()` - Writes an integer of given size.
- Added ability to provided fixed number of arguments for registered builtin call hooks.


## [0.10.0] - 2023-11-29
- Tested on Ghidra 10.4
- Added `create_function()` utility function in `rugosa.func_utils`. This attempts to define a function containing the given address by looking for common start bounds.


## [0.9.0] - 2023-09-06
- Tested on Ghidra 10.3.2
- Added support for YARA version 4.3 in `rugosa.yara` utility.
  - Both the newer `StringMatch` objects and older tuple results for `.strings` are supported based on the `legacy_strings` flag set during a call to `.match()`. (defaults to older for backwards compatibility)


## [0.8.0] - 2023-07-17
- Added support for ymm* and zmm* registers.
- Added support vector bitwise instructions:
  - `vmovaps`
  - `vmovdqa`
  - `vmovdqu`
  - `vmovupd`
  - `vmovups`
  - `vpxor`
  - `xorps`
  - `vxorps`
  - `vzeroupper`

## [0.7.2] - 2023-04-19
- Fixed implementation of `div` opcode.


## [0.7.1] - 2023-02-21
- Fixed emulation of floating point opcodes.
- Fixed bug in Ghidra plugin setup handling.


## [0.7.0] - 2023-01-26
- Add `movsq` opcode support (@ddash-ct)
- Added utility functions for analyzing strings:
  - `find_user_strings()`
  - `find_api_resolve_strings()`
  - `is_code_string()`
  - `is_library_string()`
  - `detect_encoding()`
  - `force_to_string()`
- Added better support for operands with segment registers (fs/gs)
- Fixed default data type to be an 8 byte qword when forcing extra arguments on a 64bit sample.
- Added `default_data_type` argument on `get_function_args()`/`get_function_arg_values()`/`get_function_signatures()` to change the data type used when forcing extra arguments. (Data type given should be valid for the underlying disassembler.)
- Add support for `wsprintfW` call hook.
- Added `FunctionArgument.location` property, which provides the location of the argument. (stack offset, register, etc.)
- Added `disable_all()` and `enable()` to emulator instances which simulates a whitelist for opcode/function hooks.
- Fixed bug in `idiv` opcode emulation.


## [0.6.1] - 2022-12-20
- Fix EOFError that can occur when running consecutive Emulator instances due to stale caching.
- Fix IndexError bug in IMUL emulation.


## [0.6.0] - 2022-12-02
- Support all instruction operands, both implied and explicit.
- Fix bug in ROL opcode implementation.
- Added `.function_arg_values` property to ProcessorContext.
- Added `.get_function_arg_values()` convenience function to Emulator.
- Updated `ProcessorContext.call_history` to also include the argument names.
- Added IDA and Ghidra plugin to provide a GUI for using the emulation utility. (See [documentation](./docs/EmulatorPlugin.md))
  - Please note: These plugins are currently in beta.


## [0.5.1] - 2022-10-05
- Fixed performance issue during emulation.
- Fixed missing `_heap_base` error when allocating memory.


## [0.5.0] - 2022-09-15
- Added ability to emulate functions calls. (See [documentation](./docs/CPUEmulation.md#emulating-function-calls))
- Added ability to execute full functions with `Emulator.execute_function()`.
- Added tracking of stdout in `ProcessorContext`.
- Added `printf` call hook.
- Changed `ProcessorContext.func_calls` to `ProcessorContext.call_history`. `func_calls` is now deprecated.
- Added ability to stream emulated memory using `context.memory.open()`. (See [documentation](./docs/CPUEmulation.md#memory-streaming))


## [0.4.0] - 2022-08-10

- `rugosa.emulation.memory.clear_cache()` has been moved to `rugosa.emulation.emulator.Emulator.clear_cache()` in
  order to fix a bug with `cache_clear()` not working when teleported.
- Improved `rugosa.iter_imports()` function to dedup results.
- Fixed bug in `rugosa.re.find_functions()`.
- Added ability to get and set `.calling_convention` and `.return_type` in emulated `FunctionSignature`.


## [0.3.0] - 2022-06-28

### Added
- Added `iter_import_calls()` and `iter_import_callers()` functions to better handle pivoting off import functions.
- Added support for tracking decrypted string with `rugosa.DecodedString`.
- Bugfixes to better support Ghidra backend.


## [0.2.0] - 2022-06-01

### Changed
- IDA: Greatly improved emulation performance by "teleporting" the `Emulator` instance into the IDA interpreter.

### Fixed
- *Emulation*
  - Fixed issues with windows constants in call hooks.
  - Fixed bugs in opcode calls.


## [0.1.1] - 2022-03-23

### Added
- *Emulation*
    - Added `PathAddBackslash` SHLWAPI hook

### Fixed
- *Emulation*
  - Mask off any CSIDL flags before resolving folder in `SHGetFolderPath`
- Fixed failure of tests due to ordering.


## 0.1.0 - 2022-02-04
- Initial release.
- Migrated the majority of Kordesii functionality to work with Dragodis.


[Unreleased]: https://github.com/dod-cyber-crime-center/rugosa/compare/1.0.0...HEAD
[1.0.0]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.10.0...1.0.0
[0.10.0]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.9.0...0.10.0
[0.9.0]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.8.0...0.9.0
[0.8.0]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.7.2...0.8.0
[0.7.2]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.7.1...0.7.2
[0.7.1]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.7.0...0.7.1
[0.7.0]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.6.1...0.7.0
[0.6.1]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.6.0...0.6.1
[0.6.0]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.5.1...0.6.0
[0.5.1]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.5.0...0.5.1
[0.5.0]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.1.1...0.2.0
[0.1.1]: https://github.com/dod-cyber-crime-center/rugosa/compare/0.1.0...0.1.1
