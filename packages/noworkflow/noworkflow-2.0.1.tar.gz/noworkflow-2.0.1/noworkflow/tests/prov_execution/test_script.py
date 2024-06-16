# Copyright (c) 2016 Universidade Federal Fluminense (UFF)
# Copyright (c) 2016 Polytechnic Institute of New York University.
# This file is part of noWorkflow.
# Please, consult the license terms in the LICENSE file.
"""Test Code Block collection"""
from __future__ import (absolute_import, print_function,
                        division, unicode_literals)


from ..collection_testcase import CollectionTestCase


class TestScript(CollectionTestCase):
    """Test Script activation"""

    def test_script(self):
        """Test script collection"""
        self.script("# script.py\n"
                    "# other")
        self.metascript.execution.collect_provenance()
        self.executed = True
        self.assertEqual(self.metascript.execution.msg,
                         "the execution of trial -1 finished successfully")

        script = self.find_code_component(name="script.py")
        script_evaluation = self.find_evaluation(code_component_id=script.id)
        script_activation = self.metascript.activations_store[
            script_evaluation.id
        ]
        var_module = self.get_evaluation(name=self.rtype('module'))
        var_type = self.get_evaluation(name=self.rtype('type'))

        self.assertEqual(script_evaluation.activation_id, 0)
        self.assertTrue(
            script_activation.start_checkpoint < script_evaluation.checkpoint)
        self.assertEqual(script_activation.code_block_id, script.id)
        self.assertEqual(script_activation.name, "__main__")
        self.assertEqual(len(self.metascript.exceptions_store.store), 0)
        self.assert_type(script_evaluation, var_module)
        self.assert_type(var_module, var_type)
        self.assert_type(var_type, var_type)

        self.assertEqual(script_evaluation.repr[:19], "<module '__main__' ")

    def test_script_with_error(self):
        """Test script collection with exception"""
        self.script("# script.py\n"
                    "1 / 0\n"
                    "# other")
        self.metascript.execution.collect_provenance()
        self.executed = True
        self.assertNotEqual(self.metascript.execution.msg,
                            "the execution of trial -1 finished successfully")

        script = self.find_code_component(name="script.py")
        script_evaluation = self.find_evaluation(code_component_id=script.id)
        script_activation = self.metascript.activations_store[
            script_evaluation.id
        ]
        var_module = self.get_evaluation(name=self.rtype('module'))
        var_type = self.get_evaluation(name=self.rtype('type'))

        self.assertEqual(script_evaluation.activation_id, 0)
        self.assertTrue(
            script_activation.start_checkpoint < script_evaluation.checkpoint)
        self.assertEqual(script_activation.code_block_id, script.id)
        self.assertEqual(script_activation.name, "__main__")

        self.assertEqual(len(self.metascript.exceptions_store.store), 1)
        # ToDo #77: check exception
        self.assert_type(script_evaluation, var_module)
        self.assert_type(var_module, var_type)
        self.assert_type(var_type, var_type)

        self.assertEqual(script_evaluation.repr[:19], "<module '__main__' ")
