# -*- coding: UTF-8 -*-
# Copyright 2014-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.core.choicelists import PointingChoice, MissingRow
from lino_xl.lib.accounting.utils import ZERO, Decimal
from lino.api import dd, _

if dd.is_installed("products"):

    class ReportingType(PointingChoice):
        pointing_field_name = 'products.Product.reporting_type'
        sales_price = None

        def __init__(self, value, text, name, sales_price, **kwargs):
            super().__init__(value, text, name, **kwargs)
            self.sales_price = sales_price

        def create_object(self, **kwargs):
            kwargs.update(dd.str2kw('name', self.text))
            kwargs.update(delivery_unit="hour")
            kwargs.update(reporting_type=self)
            if Decimal(self.sales_price) != ZERO and dd.is_installed('storage'):
                kwargs.update(storage_management=True)
            if dd.is_installed('trading'):
                kwargs.update(sales_price=self.sales_price)
            return self.pointing_field.model(**kwargs)


    class ReportingTypes(dd.ChoiceList):
        item_class = ReportingType
        verbose_name = _("Reporting type")
        verbose_name_plural = _("Reporting types")
        max_length = 6
        column_names = 'value name text tariff *'

        @dd.virtualfield(
            dd.ForeignKey('products.Product', verbose_name=_("Tariff")))
        def tariff(cls, choice, ar):
            obj = choice.get_object()
            if obj is None or isinstance(obj, MissingRow):
                return None
            return obj


    add = ReportingTypes.add_item

    add('10', _("Regular"), 'regular', "60.00")
    add('20', _("Extra"), 'extra', "90.00")
    add('30', _("Free"), 'free', "0.00")
    # add('10', _("Worker"), 'worker')
    # add('20', _("Employer"), 'employer')
    # add('30', _("Customer"), 'customer')

else:

    class ReportingTypes(dd.ChoiceList):
        verbose_name = _("Reporting type")
        verbose_name_plural = _("Reporting types")
        column_names = 'value name text *'

    add = ReportingTypes.add_item

    add('10', _("Regular"), 'regular')
