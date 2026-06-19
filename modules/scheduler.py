"""scheduler.py - install a Cron job so the toolkit runs automatically."""
import subprocess


def install_cron_job(schedule, command, logger):
    """Add a Cron entry that runs the toolkit on the given schedule."""
    cron_line = f"{schedule} {command}"
    try:
        existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        current = existing.stdout if existing.returncode == 0 else ""
        if command in current:
            logger.info("Cron job already installed; nothing to do")
            return True
        new_cron = current + cron_line + "\n"
        result = subprocess.run(["crontab", "-"], input=new_cron, text=True)
        if result.returncode == 0:
            logger.info(f"Installed cron job: {cron_line}")
            return True
        logger.error("Failed to install cron job")
        return False
    except Exception as error:
        logger.error(f"Error installing cron job: {error}")
        return False
