import argparse
import sys
import traceback
import os
import logging
import gazpar
import pygazpar

from gazpar.entity_recorder import PyGazparOptions
from gazpar.entity_recorder import EntityRecorder


# --------------------------------------------------------------------------------------------
def main():
    """Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version",
                        action="version",
                        version=f"gazpar {gazpar.__version__}")
    parser.add_argument("-u", "--username",
                        required=True,
                        help="GRDF username (email)")
    parser.add_argument("-p", "--password",
                        required=True,
                        help="GRDF password")
    parser.add_argument("-w", "--webdriver",
                        required=True,
                        help="Firefox webdriver executable (geckodriver)")
    parser.add_argument("-s", "--wait_time",
                        required=False,
                        type=int,
                        default=30,
                        help="Wait time in seconds (see https://selenium-python.readthedocs.io/waits.html for details)")
    parser.add_argument("-t", "--tmpdir",
                        required=False,
                        default="/tmp",
                        help="tmp directory (default is /tmp)")
    parser.add_argument("-l", "--lastNRows",
                        required=False,
                        type=int,
                        default=0,
                        help="Get only the last N rows (default is 0: it means all rows are retrieved)")
    parser.add_argument("--headfull",
                        required=False,
                        action='store_true',
                        default=False,
                        help="Run Selenium in headfull mode (default is headless)")
    parser.add_argument("-f", "--frequency",
                        required=False,
                        type=lambda frequency: pygazpar.Frequency[frequency],
                        choices=list(pygazpar.Frequency),
                        default="DAILY",
                        help="Meter reading frequency (DAILY, WEEKLY, MONTHLY)")
    parser.add_argument("--testMode",
                        required=False,
                        action='store_true',
                        default=False,
                        help="Run PyGazpar in test mode (Get static sample data)")

    subparsers = parser.add_subparsers()

    import_parser = subparsers.add_parser("import")
    import_parser.add_argument("--connectionType",
                               required=True,
                               type=str,
                               choices=list(["Sql", "InfluxDB"]),
                               help="Choose the target storage where to import to"
                               )
    import_parser.add_argument("--connectionString",
                               required=True,
                               type=str,
                               help="Connection string of the target storage"
                               )

    args = parser.parse_args()

    # We create the tmp directory if not already exists.
    if not os.path.exists(args.tmpdir):
        os.mkdir(args.tmpdir)

    # We remove the pygazpar log file.
    gazparLogFile = f"{args.tmpdir}/gazpar.log"
    if os.path.isfile(gazparLogFile):
        os.remove(gazparLogFile)

    # We remove the geckodriver log file
    geckodriverLogFile = f"{args.tmpdir}/pygazpar_geckodriver.log"
    if os.path.isfile(geckodriverLogFile):
        os.remove(geckodriverLogFile)

    # Setup logging.
    logging.basicConfig(filename=f"{gazparLogFile}", level=logging.DEBUG, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")

    logging.info(f"gazpar {gazpar.__version__}")
    logging.info(f"--webdriver {args.webdriver}")
    logging.info(f"--wait_time {int(args.wait_time)}")
    logging.info(f"--tmpdir {args.tmpdir}")
    logging.info(f"--lastNRows {int(args.lastNRows)}")
    logging.info(f"--headfull {bool(args.headfull)}")
    logging.info(f"--frequency {args.frequency}")
    logging.info(f"--testMode {bool(args.testMode)}")

    pyGazparOptions = PyGazparOptions()
    pyGazparOptions.username = args.username
    pyGazparOptions.password = args.password
    pyGazparOptions.webdriver = args.webdriver
    pyGazparOptions.wait_time = int(args.wait_time)
    pyGazparOptions.tmpdir = args.tmpdir
    pyGazparOptions.headlessMode = not bool(args.headfull)
    pyGazparOptions.testMode = bool(args.testMode)

    entityRecorder = EntityRecorder("unit test context", pyGazparOptions, args.connectionString)

    try:
        entity = entityRecorder.load(args.frequency, int(args.lastNRows))

        entityRecorder.save(entity)
    except BaseException:
        print('An error occured while importing data from PyGazpar to the target storage : %s', traceback.format_exc())
        return 1

    print("PyGazpar data import has completed successfully.")


# --------------------------------------------------------------------------------------------
if __name__ == '__main__':
    sys.exit(main())
