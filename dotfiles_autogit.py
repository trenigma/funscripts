## Automatically commit updates to dotfiles folder
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


class GitAutoCommitHandler(FileSystemEventHandler):
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def on_modified(self, event):
        if event.is_directory:
            return

        print(f"File modified: {event.src_path}")
        self.commit_changes()

    def commit_changes(self):
        if not self.repo_path:
            raise ValueError("No repository path is set.")

        try:
            # Change directory to the repo
            os.chdir(self.repo_path)

            # Stage all changes
            subprocess.run(["git", "add", "."], check=True)

            # Commit changes with a message
            subprocess.run(["git", "commit", "-m", "Auto-commit: Changes detected"], check=True)

            # Push to the remote repository
            subprocess.run(["git", "push"], check=True)

            print("Changes committed and pushed successfully.")

        except subprocess.CalledProcessError as e:
            print(f"Error during git operation: {e}")
        except FileNotFoundError as e:
            print(f"Error: Git executable not found in the system path. {e}")
        except OSError as e:
            print(f"Error: Unable to change directory to the repository path. {e}")


def monitor_folder(folder_path):
    """
    Monitors the specified folder for any changes and automatically commits
    and pushes those changes to a git repository.

    Args:
        folder_path (str): The path to the folder to be monitored.

    This function uses the watchdog library to monitor the folder for changes.
    When a change is detected, it triggers the GitAutoCommitHandler to 
    automatically commit and push the changes to a git repository.
    """
    event_handler = GitAutoCommitHandler(folder_path)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)

    print(f"Monitoring changes in folder: {folder_path}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    # Set the path to git folder
    trenigma_folder = "/Users/tree/trenigma/dotfiles"

    if not os.path.isdir(trenigma_folder):
        print("The specified folder does not exist.")
        exit(1)

    monitor_folder(trenigma_folder)

    