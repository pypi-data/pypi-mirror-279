# filestates

`filestates` is a Python package that allows you to manage the state of files and directories using YAML configuration files.

## Features

- **Apply and Modify Permissions and Ownership**: Manage file and directory permissions and ownership individually or recursively.
- **Create, Modify, and Delete Directories**: Use patterns and regex to create, modify, and delete directories and subdirectories (e.g., ensure each `Entity/MyEntity.php` file has a corresponding `Repository/MyEntityRepository.php`).
- **Create Files Using Templates and Placeholders**: Generate files from templates with dynamic placeholders.

## Installation

Install `filestates` with pip:

pip install filestates

## Usage

### Configuration File Example

```yaml
# example.yaml
files:
  - path: /path/to/file
    owner: user
    group: group
    mode: '0644'
directories:
  - path: /path/to/directory
    recursive: true
    mode: '0755'
    create: true
templates:
  - path: /path/to/output/file
    template: /path/to/template/file
    placeholders:
      placeholder1: value1
      placeholder2: value2
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
