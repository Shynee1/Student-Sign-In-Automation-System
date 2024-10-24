from sign_in import unregistered_names, register
import sign_in

from datetime import datetime
import os.path
import shutil
import logging

TEST_LOGS_DIR = "test_logs/"


class TestLogDirectory:
    """Handle testing functions that modify the logs/ folder.
    NOTE: These tests modify the contents of TEST_LOGS_DIR.
          Each test is expected to start and end with an empty directory.
    """

    def setup_method(self, method):
        """Verify that the TEST_LOGS_DIR exists and is empty before each test."""
        assert os.path.exists(TEST_LOGS_DIR)
        assert len(os.listdir(TEST_LOGS_DIR)) == 0
        sign_in.LOG_FORMAT = f"{TEST_LOGS_DIR}/%Y-%m-%d.json"

    def teardown_method(self, method):
        """Remove any remaining files in TEST_LOGS_DIR after each test."""
        assert os.path.exists(TEST_LOGS_DIR)
        for filename in os.listdir(TEST_LOGS_DIR):
            os.remove(os.path.join(TEST_LOGS_DIR, filename))
        assert len(os.listdir(TEST_LOGS_DIR)) == 0

    def test_first_day(self):
        # Ask some basic questions about students with free period on the first day of school
        assert len(unregistered_names(
            datetime(2022, 9, 7), grades=["IV"])) == 0
        assert len(unregistered_names(datetime(2022, 9, 7))) == 30

        grade5 = ['Hengst, Austan ( Austan )',
                  'Jabateh, Musa ( Musa )',
                  'Laveran, Pierce ( Pierce )',
                  'Reavey, Kevin ( Kevin )',
                  'Ronon, Gerald ( Tripp )',
                  'Yoh, Russell ( Russell )']

        assert unregistered_names(datetime(2022, 9, 7), grades=["V"]) == grade5

        # Check that registration works as expected
        register('Jabateh, Musa ( Musa )', datetime(2022, 9, 7))
        assert len(unregistered_names(datetime(2022, 9, 7), grades=["V"])) == 5
        register('Reavey, Kevin ( Kevin )', datetime(2022, 9, 7))

        remaining = ['Hengst, Austan ( Austan )',
                  'Laveran, Pierce ( Pierce )',
                  'Ronon, Gerald ( Tripp )',
                  'Yoh, Russell ( Russell )']

        assert unregistered_names(datetime(2022, 9, 7), grades=["V"]) == remaining