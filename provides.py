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
from charms.reactive import Endpoint


class BarbicanSecretsProvides(Endpoint):
    """This is the barbican-{type}secrets end of the relation."""

    def publish_plugin_info(self, name, data, reference=None):
        for relation in self.relations:
            relation.to_publish['name'] = name
            relation.to_publish['data'] = data
            relation.to_publish['reference'] = reference
