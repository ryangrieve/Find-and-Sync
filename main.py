import json
import os
import subprocess

CONFIG_FILE = "sync_settings.json"


def get_directory(prompt):
    while True:
        directory_name = input(f"\nEnter {prompt} directory name: ")
        try:
            find_command = f"find /home -type d -iname '*{directory_name}*'"
            directories = (
                subprocess.check_output(find_command, shell=True, text=True)
                .strip()
                .split("\n")
            )

            if not directories:
                print(f"No matching {prompt} directories found. Please try again.")
                continue
            elif len(directories) == 1:
                selected_directory = directories[0]
                print(f"\nSelected {prompt} directory: {selected_directory}")
            else:
                print(f"\nMatching {prompt} directories:")
                for i, directory in enumerate(directories):
                    print(f"{i+1}. {directory}")
                selection_index = (
                    int(input(f"\nSelect a {prompt} directory (1-{len(directories)}) "))
                    - 1
                )
                selected_directory = directories[selection_index]
                print(f"\nSelected {prompt} directory: {selected_directory}")

            if not os.path.exists(selected_directory):
                print(f"\nThe {prompt} directory does not exist. Please try again.")
                continue

            return selected_directory
        except subprocess.CalledProcessError:
            print(
                f"Error occurred while searching for {prompt} directories. Please try again."
            )
            continue
        except ValueError as e:
            print(f"Error: {e}. Please try again.")
            continue


def save_sync_path(source_dir, dest_dir, sync_paths):
    sync_name = input("\nEnter a name for the sync: ")
    sync_paths[sync_name] = {"source_dir": source_dir, "dest_dir": dest_dir}
    with open(CONFIG_FILE, "w") as f:
        json.dump(sync_paths, f)
    print(f"\nsync path saved to {CONFIG_FILE}\n")


def run_sync(source_dir, dest_dir):
    print("\nStarting Sync...\n\n" + "-" * 50 + "\n")
    rsync_command = f"rsync -av --progress {source_dir}/ {dest_dir}/"
    subprocess.call(rsync_command, shell=True)
    print("\n" + "-" * 50 + "\n\nSync completed successfully!\n")


def load_sync_paths():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({}, f)

    with open(CONFIG_FILE, "r") as f:
        sync_paths = json.load(f)
    return sync_paths


def choose_sync(sync_paths):
    sync_list = list(sync_paths.keys())
    print("\nSaved options:")
    for i, sync_name in enumerate(sync_list):
        print(f"{i+1}. {sync_name}")
    print(f"{len(sync_list)+1}. Start a new sync")

    while True:
        try:
            selection_index = (
                int(input(f"\nSelect a sync by number (1-{len(sync_list)+1}): ")) - 1
            )
            if selection_index == len(sync_list):
                return None
            selected_sync_name = sync_list[selection_index]
            return selected_sync_name
        except (ValueError, IndexError):
            print("Invalid selection. Please enter a valid number.")


def confirm_sync_settings(source_dir, dest_dir):
    print("\nPlease confirm that the following settings are correct:\n")
    print(f"Source directory: {source_dir}")
    print(f"Destination directory: {dest_dir}")
    confirm = input("\nAre these settings correct? (y/n): ").lower()
    if confirm == "n":
        print("\nExiting sync script...")
        return False
    return True


def get_sync_settings(sync_paths):
    if not sync_paths:
        print("\nStarting a new sync...")
    else:
        selected_sync_name = choose_sync(sync_paths)
        if selected_sync_name is not None:
            selected_sync = sync_paths[selected_sync_name]
            sync_settings = [
                selected_sync["source_dir"],
                selected_sync["dest_dir"],
            ]
            return sync_settings

    source_dir = get_directory("source")
    dest_dir = get_directory("destination")
    if not confirm_sync_settings(source_dir, dest_dir):
        return None

    sync_settings = [source_dir, dest_dir]
    save_settings = (
        input("\nDo you want to save these sync settings? (y/n): ").lower() == "y"
    )
    if save_settings:
        save_sync_path(source_dir, dest_dir, sync_paths)

    return sync_settings


def config_sync():
    print(
        """
Find-and-Sync

Find-and-Sync is a tool that simplifies the synchronization of directories.
It searches for source and destination directories that match input and
syncs them using the find command and rsync. When saved settings exist, the
script offers to load previous sync options or create a new sync."""
    )

    sync_paths = load_sync_paths()
    sync_settings = get_sync_settings(sync_paths)

    if not sync_settings:
        return

    source_dir, dest_dir = sync_settings

    run_sync(source_dir, dest_dir)


config_sync()
