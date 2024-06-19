import yaml
import os
import argparse
from typing import Optional

class DotDict(dict):
    """A dictionary with dot notation access."""
    def __getattr__(self, item: str):
        value = self.get(item)
        if isinstance(value, dict):
            return DotDict(value)
        return value

    def __setattr__(self, key: str, value):
        self[key] = value

    def __delattr__(self, key: str):
        del self[key]

def find_config_file() -> Optional[str]:
    """Find the .config.yaml file in the current folder or parent folders."""
    current_dir = os.getcwd()

    while current_dir:
        config_path = os.path.join(current_dir, '.config.yaml')
        if os.path.exists(config_path):
            return config_path
        current_dir = os.path.dirname(current_dir)

    return None

def load_yaml(file_path: str) -> DotDict:
    """Load YAML file and return a DotDict."""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return DotDict(data)

def get_nested_attr(data: DotDict, attr_path: str):
    """Get nested attribute using dot notation."""
    attrs = attr_path.split('.')
    current = data
    for attr in attrs:
        current = getattr(current, attr)
    return current

class BaseCommand:
    def __init__(self, parser):
        self.parser = parser

    def add_arguments(self):
        pass

    def execute(self, args):
        pass

class ConfigCommand(BaseCommand):
    def __init__(self, parser):
        super().__init__(parser)

    def add_arguments(self):
        self.parser.add_argument('--read', action='store_true',
                                 help='Output all variables from the configuration file')

    def execute(self, args):
        config_path = find_config_file()

        if not config_path:
            print("Error: .config.yaml file not found.")
            return

        config = load_yaml(config_path)

        if args.read:
            print(config)
        else:
            self.parser.print_help()

def main():
    parser = argparse.ArgumentParser(prog='zulu', description="Zulu CLI.")

    subcommands = {
        'config': ConfigCommand,
        # Add more subcommands as needed
    }

    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    for command_name, command_class in subcommands.items():
        command_parser = subparsers.add_parser(command_name, help=f'Manage {command_name}')
        command_instance = command_class(command_parser)
        command_instance.add_arguments()

    args = parser.parse_args()

    if args.command:
        command_class = subcommands.get(args.command)
        if command_class:
            command_instance = command_class(parser)
            command_instance.execute(args)
        else:
            print(f"Error: Unknown command '{args.command}'")
            parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
