"""updater.py - run apt update and apt upgrade through subprocess."""
import subprocess


def run_update(logger):
    """Run 'apt update' then 'apt upgrade -y', logging the outcome of each."""
    commands = [
        ["sudo", "apt", "update"],
        ["sudo", "apt", "upgrade", "-y"],
    ]
    for command in commands:
        logger.info(f"Running: {' '.join(command)}")
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"Success: {' '.join(command)}")
            else:
                logger.error(
                    f"Command failed (exit {result.returncode}): {' '.join(command)}"
                )
                logger.error(result.stderr.strip())
                return False
        except Exception as error:
            logger.error(f"Error running {' '.join(command)}: {error}")
            return False

    logger.info("System update completed")
    return True
