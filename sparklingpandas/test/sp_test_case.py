#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""This module provides some common test case bases for
 SparklingPandasTestCases"""

from sparklingpandas.utils import add_pyspark_path
import pandas

add_pyspark_path()
from pyspark import SparkConf
from sparklingpandas.pcontext import PSparkContext
import unittest2
import sys
from pandas.util.testing import assert_frame_equal
import logging


class SparklingPandasTestCase(unittest2.TestCase):

    """Basic SparklingPandasTestCase, inherit from this class to get a
    PSparkContext as spark_ctx."""

    def setUp(self):
        """Setup the basic panda spark test case. This right now just creates a
        PSparkContext."""
        print "Setting up spark context"
        self._old_sys_path = list(sys.path)
        class_name = self.__class__.__name__
        conf = SparkConf()
        conf.set("spark.cores.max", "4")
        conf.set("spark.master", "local[4]")
        conf.set("spark.app-name", class_name)
        conf.set("spark.driver.allowMultipleContexts", "true")
        self.psc = PSparkContext.simple(conf=conf)
        # Add a common basic input and basicpframe we can reuse in testing
        self.basicinput = [
            ("tea", "happy"),
            ("water", "sad"),
            ("coffee", "happiest"),
            ("tea", "water")]
        self.basiccolumns = ['magic', 'thing']
        self.basicpframe = self.psc.DataFrame(
            self.basicinput, columns=self.basiccolumns)
        self.basicframe = pandas.DataFrame(
            self.basicinput, columns=self.basiccolumns)
        # Add a numeric frame
        self.numericinput = [
            (1, 2), (3, 4), (1, 3), (2, 6), (3, 100), (3, 20), (8, 9)]
        self.numericpframe = self.psc.DataFrame(
            self.numericinput, columns=['a', 'b'])
        self.numericframe = pandas.DataFrame(
            self.numericinput, columns=['a', 'b'])
        # A three column numeric frame
        self.numericthreeinput = [
            (1, 2, -100.5),
            (3, 4, 93),
            (1, 3, 100.2),
            (2, 6, 0.5),
            (3, 100, 1.5),
            (3, 20, 80),
            (8, 9, 20)]
        self.numericthreepframe = self.psc.DataFrame(
            self.numericthreeinput, columns=['a', 'b', 'c'])
        self.numericthreeframe = pandas.DataFrame(
            self.numericthreeinput, columns=['a', 'b', 'c'])
        self.mixedinput = [(1, 2, "coffee"), (4, 5, "cheese")]
        self.mixedpframe = self.psc.DataFrame(self.mixedinput,
                                              columns=['a', 'b', 'c'])
        self.mixedframe = pandas.DataFrame(self.mixedinput,
                                           columns=['a', 'b', 'c'])
        # Mixed NA frame
        self.mixednainput = [(1, 2, "coffee", None), (4, 5, "cheese", None)]
        self.mixednapframe = self.psc.DataFrame(self.mixednainput,
                                                columns=['a', 'b', 'c', 'd'])
        self.mixednaframe = pandas.DataFrame(self.mixednainput,
                                             columns=['a', 'b', 'c', 'd'])

    def tearDown(self):
        """
        Tear down the basic panda spark test case. This stops the running
        context and does a hack to prevent Akka rebinding on the same port.
        """
        print "tearing down spark context"
        self.psc.stop()
        sys.path = self._old_sys_path
        # To avoid Akka rebinding to the same port, since it doesn't unbind
        # immediately on shutdown
        self.psc.spark_ctx._jvm.System.clearProperty("spark.driver.port")

    @staticmethod
    def _compare_dfs(df1, df2):
        """
        Compare two DataFrames for equality
        """
        assert_frame_equal(df1, df2)

if __name__ == "__main__":
    unittest2.main()
