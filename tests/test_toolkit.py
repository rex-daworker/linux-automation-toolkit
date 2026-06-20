"""Unit tests for the Linux Automation Toolkit modules."""
import json, logging, os
from unittest.mock import patch, MagicMock
import pytest
import main
from modules.logger import get_logger
from modules.backup import create_backup
from modules.updater import run_update
from modules.scheduler import install_cron_job


@pytest.fixture(autouse=True)
def reset_logger():
    lg = logging.getLogger("linux_automation_toolkit")
    lg.handlers.clear()
    yield
    lg.handlers.clear()


def test_get_logger_returns_logger(tmp_path):
    log_file = str(tmp_path / "logs" / "toolkit.log")
    logger = get_logger(log_file, "INFO")
    assert isinstance(logger, logging.Logger)
    assert os.path.isdir(os.path.dirname(log_file))


def test_logger_writes_to_file(tmp_path):
    log_file = str(tmp_path / "t.log")
    logger = get_logger(log_file, "INFO")
    logger.info("hello test")
    for h in logger.handlers:
        h.flush()
    assert "hello test" in open(log_file).read()


def test_backup_creates_timestamped_folder(tmp_path):
    src = tmp_path / "src"; src.mkdir()
    (src / "file.txt").write_text("data")
    logger = get_logger(str(tmp_path / "t.log"))
    path = create_backup([str(src)], str(tmp_path / "backups"), logger)
    assert os.path.isdir(path)
    assert os.path.basename(path).startswith("backup_")
    assert os.path.exists(os.path.join(path, "src", "file.txt"))


def test_backup_skips_missing_directory(tmp_path):
    logger = get_logger(str(tmp_path / "t.log"))
    path = create_backup(["/nonexistent/dir/xyz"], str(tmp_path / "backups"), logger)
    assert os.path.isdir(path)


def test_update_success(tmp_path):
    logger = get_logger(str(tmp_path / "t.log"))
    ok = MagicMock(returncode=0, stdout="ok", stderr="")
    with patch("modules.updater.subprocess.run", return_value=ok):
        assert run_update(logger) is True


def test_update_failure_stops(tmp_path):
    logger = get_logger(str(tmp_path / "t.log"))
    fail = MagicMock(returncode=1, stdout="", stderr="error")
    with patch("modules.updater.subprocess.run", return_value=fail):
        assert run_update(logger) is False


def test_install_cron_job_new(tmp_path):
    logger = get_logger(str(tmp_path / "t.log"))
    empty = MagicMock(returncode=0, stdout="")
    put = MagicMock(returncode=0)
    with patch("modules.scheduler.subprocess.run", side_effect=[empty, put]):
        assert install_cron_job("0 2 * * *", "python3 main.py --auto", logger) is True


def test_install_cron_job_already_exists(tmp_path):
    logger = get_logger(str(tmp_path / "t.log"))
    cmd = "python3 main.py --auto"
    existing = MagicMock(returncode=0, stdout=f"0 2 * * * {cmd}\n")
    with patch("modules.scheduler.subprocess.run", side_effect=[existing]):
        assert install_cron_job("0 2 * * *", cmd, logger) is True


def test_load_config(tmp_path):
    cfg = {"backup_directories": ["/etc/apt"], "log_file": "logs/toolkit.log"}
    p = tmp_path / "settings.json"
    p.write_text(json.dumps(cfg))
    assert main.load_config(str(p))["backup_directories"] == ["/etc/apt"]
