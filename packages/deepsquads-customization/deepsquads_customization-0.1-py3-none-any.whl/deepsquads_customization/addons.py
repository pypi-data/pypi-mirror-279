# Copyright © KhulnaSoft Bot <info@khulnasoft.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Example pre commit script."""

from django.utils.translation import ugettext_lazy as _
from deepsquads.addons.events import EVENT_PRE_COMMIT
from deepsquads.addons.scripts import BaseScriptAddon


class ExamplePreAddon(BaseScriptAddon):
    """Pre commit script example addon."""

    # Event used to trigger the script
    events = (EVENT_PRE_COMMIT,)
    # Name of the addon, has to be unique
    name = "deepsquads.example.pre"
    # Verbose name and long descrption
    verbose = _("Execute script before commit")
    description = _("This addon executes a script.")

    # Script to execute
    script = "/bin/true"
    # File to add in commit (for pre commit event)
    # does not have to be set
    add_file = "po/{{ language_code }}.po"
