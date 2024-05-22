# Copyright 2024 Adam McKellar, Kanushka Gupta, Timo Ege

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from importlib import metadata

__version__ = metadata.version(__package__)

# This is terrible and I really hate it.
__description__ = metadata.metadata(__package__)["Summary"]
__repository__ = metadata.metadata(__package__)["Project-URL"]

__author__ = metadata.metadata(__package__)["Author"]
__author_email__ = metadata.metadata(__package__)["Author-email"]
__license__ = metadata.metadata(__package__)["License"]

del metadata

from installation_instruction.installation_instruction import InstallationInstruction
import installation_instruction.helpers
from installation_instruction.get_flags_and_options_from_schema import get_flags_and_options

