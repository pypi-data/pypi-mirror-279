import os
import sys
import distro
import json
import subprocess
import argparse

CONFIG_FILE = "config.json"


def main():
    parser = argparse.ArgumentParser(
        description="Dashdot-dotfiles manager",
        usage="ds [command] {link delink edit}"
    )
    parser.add_argument("command", choices=[
                        "link", "delink", "edit", "bootstrap", "update"], help="Command to be run")
    parser.add_argument("config", nargs="?", help="Configuration to edit")

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"config.json not found")

    with open(CONFIG_FILE, "rb") as json_file:
        config = json.load(json_file)

    if args.command == "link":
        link_dotfiles(config)
    elif args.command == "delink":
        delink_dotfiles(config)
    elif args.command == "edit":
        edit_dotfiles(config, args.config)
    elif args.command == "bootstrap":
        bootstrap_system(config)
    elif args.command == "update":
        update_system(config)


def link_dotfiles(dotfiles_config):
    for section, settings in dotfiles_config.items():
        if section in ["editor", "bootstrap", "update"]:
            continue

        locations = settings.get("location", [])

        if not locations:
            print(f"Invalid configuration for '{section}'. Skipping.")
            continue

        dotfiles_path = os.path.join(os.path.abspath("."), section)
        if isinstance(locations, str):
            src_path = os.path.join(dotfiles_path)
            dst_path = os.path.expandvars(locations)

            try:
                os.symlink(src_path, dst_path)
                print(f"Symlink created: {dst_path}")
            except FileExistsError:
                print(f"Symlink already exists: {dst_path}")
        elif isinstance(locations, list):
            for location in locations:
                src_path = os.path.join(dotfiles_path, location["src"])
                dst_path = os.path.expandvars(location["dest"])

                try:
                    os.symlink(src_path, dst_path)
                    print(f"Symlink created: {dst_path}")
                except FileExistsError:
                    print(f"Symlink already exists: {dst_path}")


def delink_dotfiles(dotfiles_config):
    for section, settings in dotfiles_config.items():
        if section in ["editor", "bootstrap", "update"]:
            continue
        locations = settings.get("location", [])

        if not locations:
            print(f"Invalid configuration for '{section}'. Skipping.")
            continue

        if isinstance(locations, str):
            dst_path = os.path.expandvars(locations)

            try:
                os.unlink(dst_path)
                print(f"Symlink deleted: {dst_path}")
            except FileNotFoundError:
                print(f"Symlink not found: {dst_path}")
        elif isinstance(locations, list):
            for location in locations:
                dst_path = os.path.expandvars(location["dest"])
                try:
                    os.unlink(dst_path)
                    print(f"Symlink deleted: {dst_path}")
                except FileNotFoundError:
                    print(f"Symlink not found: {dst_path}")


def edit_dotfiles(dotfiles_config, config_to_edit):
    if config_to_edit and config_to_edit in dotfiles_config:
        editor = dotfiles_config.get("editor", "nano")
        main_file = dotfiles_config[config_to_edit].get("main", "")

        if main_file:
            dotfiles_path = os.path.join(os.path.abspath("."), config_to_edit)
            src_path = os.path.join(dotfiles_path, main_file)
            try:
                subprocess.run(editor.split() + [src_path])
            except subprocess.CalledProcessError as e:
                print(f"Error while editing file: {e}")
        else:
            print(f"Invalid configuration for '{config_to_edit}'.")
    else:
        for section in dotfiles_config.keys():
            if section not in ["editor", "update", "bootstrap"]:
                print(section)


def bootstrap_system(dotfiles_config):
    print("Bootstraping system\n")
    print("Linking your dotfiles")
    link_dotfiles(dotfiles_config)

    bootstrap = dotfiles_config.get("bootstrap")
    platform = sys.platform

    if platform == "linux":
        commands = bootstrap["linux"][distro.id()]
    else:
        commands = bootstrap[platform]

    for n, command in enumerate(commands):
        print(f"\nTask: {n + 1}")
        subprocess.run(command.split())


def update_system(dotfiles_config):
    print("Updating system")
    update = dotfiles_config.get("update")
    platform = sys.platform

    if platform == "linux":
        commands = update["linux"][distro.id()]
    else:
        commands = update[platform]

    for n, command in enumerate(commands):
        print(f"\nTask: {n + 1}")
        subprocess.run(command.split())


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
