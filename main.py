"""main.py - entry point. Flow: backup -> update -> log. Supports manual and scheduled runs."""
import argparse
import json

from modules.logger import get_logger
from modules.backup import create_backup
from modules.updater import run_update
from modules.scheduler import install_cron_job


def load_config(path="config/settings.json"):
    with open(path) as config_file:
        return json.load(config_file)


def main():
    parser = argparse.ArgumentParser(description="Linux Automation Toolkit")
    parser.add_argument("--auto", action="store_true",
                        help="Run without prompts (for Cron).")
    parser.add_argument("--schedule", action="store_true",
                        help="Install the Cron job and exit.")
    args = parser.parse_args()

    config = load_config()
    logger = get_logger(config.get("log_file", "logs/toolkit.log"),
                        config.get("log_level", "INFO"))

    if args.schedule:
        install_cron_job(config["cron_schedule"], config["cron_command"], logger)
        return

    logger.info("=== Linux Automation Toolkit started ===")

    if not args.auto:
        answer = input("This will back up directories and run system updates. Continue? [y/N] ")
        if answer.strip().lower() != "y":
            logger.info("Run cancelled by user")
            return

    create_backup(config["backup_directories"], config["backup_destination"], logger)
    run_update(logger)
    logger.info("=== Toolkit run finished ===")


if __name__ == "__main__":
    main()
