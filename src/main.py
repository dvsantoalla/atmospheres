import argparse
import logging

import sys
from tests.notes_test import *
from tests.sounds_test import *
import csound.output

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', help="Run the following tests or 'all'")
parser.add_argument('-o', '--output', help="Write output to a file instead of DAC")
parser.add_argument('-d', '--debug', action='store_true')

if not "pytest" in sys.modules:
    args = parser.parse_args(sys.argv[1:])
    pytesting = False
else:
    args = None
    pytesting = True

if pytesting or args and args.debug:
    log.basicConfig(level=log.DEBUG)
    log.warning("Debugging output enabled")
else: 
    log.basicConfig(level=log.INFO)

logging.getLogger("matplotlib").setLevel(logging.WARN)

if args and args.output:
    csound.output.DAC = False
    csound.output.FILENAME = args.output

if args and args.test:
    log.info("Testing %s" % args.test)
    tl = unittest.TestLoader()
    if args.test == "all":
        suites = tl.discover("tests", pattern="*.py")
        test_results = []
        for s in suites:
            log.info("Running test suite %s" % s)
            tr = unittest.TextTestRunner(verbosity=2).run(s)
            test_results.append(tr)
        for t in test_results:
            log.error("%s errors %s of %s" % (t, len(t.errors), t.testsRun))
            if len(t.errors) > 0:
                for err in t.errors:
                    for err2 in err:
                        log.error("**** %s" % err2)
    else:
        # suite = unittest.TestLoader().loadTestsFromTestCase(TestSounds)
        suite = tl.loadTestsFromName(args.test)
        unittest.TextTestRunner(verbosity=2).run(suite)
        # https://docs.python.org/2/library/unittest.html#loading-and-running-tests


