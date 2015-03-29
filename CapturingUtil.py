from cStringIO import StringIO
import sys

"""
Compliments of StackOverflow,
This will capture the print to command line output to either
print later or likely in our case just keep it
from bombarding the user like with plot.
"""
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout

if __name__=='__main__':
    print "before"
    with Capturing() as output:
        print "hello"
    print "after"
