# GPT-Ignore

`gpt-ignore` is a Python package designed to collect code from a specified project directory, ignoring files and directories as specified in a `.gpt-ignore` file (which defaults to the contents of `.gitignore` if `.gpt-ignore` does not exist). It extracts code from files with specific extensions and compiles it into a single output file.

## Features

- Copies `.gitignore` to `.gpt-ignore` if `.gpt-ignore` does not exist.
- Reads ignore patterns from `.gpt-ignore`.
- Traverses the project directory, collecting code from files with specified extensions.
- Writes the collected code to an output file.

## Installation

You can install the package from PyPI using pip:

```sh
pip install gpt-ignore
```

## Usage

After installation, you can use the gpt-ignore command:
    
```sh
gpt-ignore /path/to/project --output_file=output.txt
```

### Command Line Arguments
- `root_dir`: Path to the project directory (required).
- `--output_file`: Name of the output file (default: `all_code.txt`).

### Sample Output

```sh
File: /path/to/file.py
Type: .py

# Content of file.py

File: /path/to/another_file.js
Type: .js

// Content of another_file.js
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please submit a pull request or report issues on the GitHub repository.

## Acknowledgements

This project was inspired by [gitignore.io](https://www.gitignore.io/).

## Authors
 -Tayyip Canbay 