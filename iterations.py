from __future__ import division
from __future__ import print_function

from collections import defaultdict

import sys

class Iterations(object):
    """
    The Iterations object contains the data needed to run an iteration and
        display the results.
    """

    def __init__(self, name, iterations, *args, **kwargs):
        """
        name:       name of the test being run, which is the display text
        iterations: the number of iterations to run
        total:      (optional) the total number of iterations being considered
                    which is useful if the the process has multiple stages
                    that would otherwise skew the end percentage.  (set to
                    iterations by default)
        """

        self.iterations = iterations
        self.total_iterations = kwargs.get('total', iterations)
        self.name = name
        self.results = defaultdict(int)

    def run(self, func, *args, **kwargs):
        """
        Run the designated test.

        func:       The function to be tested.
        *args:      Arguments to pass to the function
        **kwargs:   Arguments passed to the function

        display:    (optional), if display is set to False, run will not
                    print information on its current status.
        """

        self.results = defaultdict(int) # clear any previous data

        display = kwargs.get('display', True)
        for iteration in range(self.iterations):
            if self.iterations > 1000 and iteration % 100 == 0:
                msg = "Running {} iterations for {}: ".format(self.iterations,
                                                              self.name)
                if display:
                    sys.stdout.write('{0}{1:.2f}%\r'.format(msg,
                                                            (iteration
                                                             / self.iterations) * 100))
                    sys.stdout.flush()

            result = func(*args, **kwargs)
            self.results[result] += 1

        if display:
            print("")
        return self.results

    def display_results(self):
        """
        Display the results of the completed test.

        """
        print("")
        print(self.name)
        print(20 * '-')
        for result in sorted(self.results):
            print("{}: {}%".format(result,
                                   (self.results[result]
                                    / float(self.total_iterations) * 100)))

        return self.results

    def return_results(self):
        """
        Instead of displaying the results, return the results as a dictionary

        """

        return self.results
