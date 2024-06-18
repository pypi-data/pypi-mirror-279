# -*- coding: UTF-8 -*-
# Copyright 2011-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings

from lino.core.utils import resolve_model
from lino.utils.instantiator import Instantiator, i2d
from lino.utils.cycler import Cycler
from lino.api import rt

TEXTS = [
    ln.strip() for ln in """
Bar cannot baz
Bars have no foo
How to get bar from foo
Foo never bars
No more foo when bar is gone
Cannot delete foo
Why is foo so bar
Irritating message when bar
How can I see where bar?
Misc optimizations in Baz
Default account in invoices per partner
'NoneType' object has no attribute 'isocode'
""".splitlines() if ln.strip()
]


def objects():
    CTEXTS = Cycler(TEXTS)
    User = resolve_model(settings.SITE.user_model)
    Site = rt.models.tickets.Site
    Ticket = rt.models.tickets.Ticket
    u = User.objects.all()[0]

    project = Instantiator(Site, "name").build
    yield project("Spring")
    yield project("Summer")
    yield project("Autumn")
    yield project("Winter")
    PROJECTS = Cycler(Site.objects.all())

    ticket = Instantiator(Ticket, "summary", user=u).build

    for i in range(10):
        t = ticket(summary=CTEXTS.pop(), site=PROJECTS.pop())
        yield t
