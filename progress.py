# Progress module
# Copyright: Stavros Korokithakis, 2007
# License: GNU LGPL
#
import time
import unittest


class Progress:
    """Track the progress of an operation and calculate the projected time to
    its completion."""
    def __init__(self, totalitems, timeasstring = True):
        """Create a Progress instance. totalitems must be the total number of
        items we intend to process, so the class knows how far we've gone."""
        self.__totalitems = totalitems
        self.__starttime = time.time()
        self.__timeasstring = timeasstring

    def timetostr(self, duration):
        """Convert seconds to D:H:M:S format (whichever applicable)."""
        # The verbosity is because this class should be as light as possible,
        # since it will probably be used in loops (hopefully not called very
        # often, but still).
        duration = int(duration)
        timelist = [duration / 86400, (duration / 3600) % 24]
        timestring = ""
        printall = False
        for item in timelist:
            printall |= item
            if printall:
                timestring += str(item).zfill(2) + ":"
        timestring += str((duration / 60) % 60).zfill(2) + \
        ":" + str(duration % 60).zfill(2)
        return timestring

    def progress(self, itemnumber):
        """We have progressed itemnumber items, so return our completion
        percentage, items/total items, total time and projected total
        time."""
        elapsed = time.time() - self.__starttime
        # Multiply by 1.0 to force conversion to long.
        percentcomplete = (1.0 * itemnumber) / self.__totalitems
        try:
            total = int(elapsed / percentcomplete)
        except ZeroDivisionError:
            total = 0
        if self.__timeasstring:
            return (
                self.timetostr(elapsed),
                self.timetostr(total),
                int(percentcomplete * 100),
                itemnumber, self.__totalitems
                )
        else:
            return (
                int(elapsed),
                int(total),
                int(percentcomplete * 100),
                itemnumber,
                self.__totalitems
                )

    def progressstring(self, itemnumber):
        """Return a string detailing the current progress."""
        timings = self.progress(itemnumber)
        if itemnumber == self.__totalitems:
            return "Done in %s, processed %s items.        \n" % \
            (timings[0], timings[4])
        else:
            return "Progress: %s/%s, %s%%, %s/%s items.\r" % timings
        return progstr


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.progress = Progress(100)

    def testtimetostr(self):
        tests = [(10, "00:10"),
            (75, "01:15"),
            (4000, "01:06:40"),
            (87123, "01:00:12:03"),
            (187123, "02:03:58:43"),
                ]
        for test, result in tests:
            self.assertEqual(self.progress.timetostr(test), result)


if __name__ == "__main__":
    unittest.main()
