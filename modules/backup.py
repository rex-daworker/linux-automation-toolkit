"""backup.py - create timestamped backups of important directories before updates."""
import os
import shutil
from datetime import datetime


def create_backup(directories, destination, logger):
    """Copy the given directories into a timestamped backup folder."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = os.path.join(destination, f"backup_{timestamp}")
    os.makedirs(backup_path, exist_ok=True)
    logger.info(f"Starting backup into {backup_path}")

    for directory in directories:
        if not os.path.exists(directory):
            logger.warning(f"Skipping missing directory: {directory}")
            continue
        target = os.path.join(backup_path, os.path.basename(directory.rstrip("/")))
        try:
            shutil.copytree(directory, target, dirs_exist_ok=True)
            logger.info(f"Backed up {directory} -> {target}")
        except Exception as error:
            logger.error(f"Failed to back up {directory}: {error}")

    logger.info("Backup completed")
    return backup_path
