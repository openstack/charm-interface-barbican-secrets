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

# the reactive framework unfortunately does not grok `import as` in conjunction
# with decorators on class instance methods, so we have to revert to `from ...`
# imports
from charms.reactive import Endpoint, clear_flag, set_flag, when_any, when_not


class BarbicanSecretsRequires(Endpoint):
    """This is the Barbican 'end' of the relation."""

    @when_any('endpoint.{endpoint_name}.changed.name',
              'endpoint.{endpoint_name}.changed.reference',
              'endpoint.{endpoint_name}.changed.data')
    def new_plugin(self):
        set_flag(
            self.expand_name('{endpoint_name}.new-plugin'))
        clear_flag(
            self.expand_name('{endpoint_name}.changed.name'))
        clear_flag(
            self.expand_name('{endpoint_name}.changed.reference'))
        clear_flag(
            self.expand_name('{endpoint_name}.changed.data'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(
            self.expand_name('{endpoint_name}.new-plugin'))

    @property
    def plugins(self):
        for relation in self.relations:
            for unit in relation.units:
                name = unit.received['name']
                reference = unit.received['reference']
                data = unit.received['data']
                if not (name and data):
                    continue
                yield {
                    'name': name,
                    'reference': reference,
                    'data': data,
                    'relation_id': relation.relation_id,
                    'remote_unit_name': unit.unit_name,
                }

    @property
    def plugins_string(self):
        def plugin_name_or_reference():
            for relation in self.relations:
                for unit in relation.units:
                    name = unit.received['name']
                    reference = unit.received['reference']
                    data = unit.received['data']
                    if not (name and data):
                        continue
                    if reference:
                        yield reference
                    else:
                        yield name + '_plugin'
        return ','.join(plugin_name_or_reference())
