# Copyright 2018 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import mock

import requires

import charms_openstack.test_utils as test_utils


_hook_args = {}


class TestRegisteredHooks(test_utils.TestRegisteredHooks):

    def test_hooks(self):
        defaults = []
        hook_set = {
            'when_any': {
                'new_plugin': ('endpoint.{endpoint_name}.changed.name',
                               'endpoint.{endpoint_name}.changed.reference',
                               'endpoint.{endpoint_name}.changed.data',),
            },
            'when_not': {
                'broken': ('endpoint.{endpoint_name}.joined',),
            },
        }
        # test that the hooks were registered via the
        # reactive.barbican_handlers
        self.registered_hooks_test_helper(requires, hook_set, defaults)


class TestBarbicanSecretRequires(test_utils.PatchHelper):

    def setUp(self):
        super().setUp()
        self.bsr = requires.BarbicanSecretsRequires('some-relation', [])
        self._patches = {}
        self._patches_start = {}

    def tearDown(self):
        self.bsr = None
        for k, v in self._patches.items():
            v.stop()
            setattr(self, k, None)
        self._patches = None
        self._patches_start = None

    def patch_bsr(self, attr, return_value=None):
        mocked = mock.patch.object(self.bsr, attr)
        self._patches[attr] = mocked
        started = mocked.start()
        started.return_value = return_value
        self._patches_start[attr] = started
        setattr(self, attr, started)

    def test_new_plugin(self):
        self.patch_object(requires, 'set_flag')
        self.patch_object(requires, 'clear_flag')
        self.bsr.new_plugin()
        self.set_flag.assert_called_with('some-relation.new-plugin')
        self.clear_flag.assert_has_calls([
            mock.call('some-relation.changed.name'),
            mock.call('some-relation.changed.reference'),
            mock.call('some-relation.changed.data'),
        ])

    def test_broken(self):
        self.patch_object(requires, 'clear_flag')
        self.bsr.broken()
        self.clear_flag.assert_called_with('some-relation.new-plugin')

    def test_plugins(self):
        self.patch_bsr('_relations')
        relation = mock.MagicMock()
        unit = mock.PropertyMock()
        type(relation).units = [unit]
        relation.relation_id = 'RELATION_ID'
        self._relations.__iter__.return_value = [relation]
        result = next(self.bsr.plugins)
        self.assertEqual(result['name'], unit.received['name'])
        self.assertEqual(result['reference'], unit.received['reference'])
        self.assertEqual(result['data'], unit.received['data'])
        self.assertEqual(result['relation_id'], relation.relation_id)
        self.assertEqual(result['remote_unit_name'], unit.unit_name)

    def test_plugins_string(self):
        self.patch_bsr('_relations')
        relation = mock.MagicMock()
        unit = mock.MagicMock()
        unit.received = {'name': 'NAME', 'reference': None, 'data': 'DATA'}
        relation.units = [unit]
        self._relations.__iter__.return_value = [relation]
        self.assertEqual(self.bsr.plugins_string, 'NAME_plugin')
        unit.received = {'name': 'NAME', 'reference': 'PLUGINREFERENCE',
                         'data': 'DATA'}
        self.assertEqual(self.bsr.plugins_string, 'PLUGINREFERENCE')
