# -*- coding: UTF-8 -*-
# Copyright 2017-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils.html import escape
from django.contrib.contenttypes.fields import GenericRelation

from lino.api import dd, rt, _
from lino.mixins import BabelNamed, Referrable
from lino.utils.html import E, join_elems
from lino.modlib.comments.mixins import Commentable, PrivateCommentsReader
from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.notify.mixins import ChangeNotifier
from lino.core.roles import SiteAdmin, SiteUser  # , UserRole
from lino.core import constants


class Group(BabelNamed, Referrable, ChangeNotifier, Commentable):

    class Meta:
        app_label = 'groups'
        abstract = dd.is_abstract_model(__name__, 'Group')
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    memo_command = "group"

    description = dd.RichTextField(_("Description"),
                                   blank=True,
                                   format='plain')

    private = models.BooleanField(_("Private"), default=False)

    comments = GenericRelation('comments.Comment',
                               content_type_field='owner_type',
                               object_id_field='owner_id',
                               related_query_name="group")
                               # needed by get_request_queryset()

    @classmethod
    def setup_parameters(cls, fields):
        """Adds the :attr:`user` filter parameter field."""
        fields.setdefault('user',
                          dd.ForeignKey('users.User', blank=True, null=True))
        super().setup_parameters(fields)

    def get_change_observers(self, ar=None):
        for x in super().get_change_observers(ar):
            yield x
        for mbr in self.members.all():
            yield (mbr.user, mbr.user.mail_mode)

    # @dd.displayfield(_("Recent comments"))
    # def recent_comments(self, ar):
    #     if ar is None:
    #         return ''
    #     cls = rt.models.comments.CommentsByRFC
    #     sar = cls.request(parent=ar, master_instance=self, limit=3)
    #     chunks = []
    #     for com in sar.sliced_data_iterator:
    #         chunks.append(ar.obj2html(com, str(com)))
    #     chunks.append("...")
    #     chunks = join_elems(chunks, ', ')
    #
    #     sar = cls.insert_action.request(parent=sar)
    #     if sar.get_permission():
    #         btn = sar.ar2button(None, _("Write comment"), icon_name=None)
    #         chunks.append(" ")
    #         chunks.append(btn)
    #
    #     return E.div(*chunks)

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = super().get_request_queryset(ar, **filter)
        user = ar.get_user()
        if user.user_type.has_required_roles([SiteAdmin]):
            return qs
        if user.is_anonymous:
            return qs.none()
        # either a public group, or I am the owner, or I am a member
        q1 = Q(private=False)
        # q2 = Q(**{prefix+'user': user})
        q2 = Q(members__user=user)
        qs = qs.filter(q1|q2).distinct()
        return qs

    @classmethod
    def add_comments_filter(cls, qs, ar):
        groups = cls.get_request_queryset(ar)
        return qs.filter(Q(group=None) | Q(group__in=groups))
        # if groups.exists():
        #     return qs.filter(Q(group=None) | Q(group__in=groups))
        # return qs.filter(group=None)

    # @classmethod
    # def get_comments_filter(cls, user):
    #     if user.user_type.has_required_roles([PrivateCommentsReader]):
    #         return None
    #     if user.is_anonymous:
    #         return super().get_comments_filter(user)
    #     flt = Q(group__members__user=user)
    #     flt |= Q(user=user) | Q(private=False)
    #     return flt


class Groups(dd.Table):
    model = 'groups.Group'
    column_names = 'ref detail_link *'
    order_by = ['ref']
    required_roles = dd.login_required(SiteAdmin)

    insert_layout = """
    name
    ref private
    description
    """

    detail_layout = """
    name
    ref:10 id private
    description MembershipsByGroup
    comments.CommentsByRFC
    """

    @classmethod
    def get_request_queryset(self, ar, **kwargs):
        qs = super().get_request_queryset(ar, **kwargs)
        if (pv := ar.param_values) is None: return qs
        if pv.user:
            qs = qs.filter(Q(members__user=pv.user))
        return qs


class MyGroups(My, Groups):
    # column_names = 'overview:10 recent_comments *'
    required_roles = dd.login_required(SiteUser)


class Membership(UserAuthored):

    class Meta:
        app_label = 'groups'
        abstract = dd.is_abstract_model(__name__, 'Membership')
        verbose_name = _("Group membership")
        verbose_name_plural = _("Group memberships")

    group = dd.ForeignKey('groups.Group', related_name="members")
    remark = models.CharField(_("Remark"), max_length=200, blank=True)

    allow_cascaded_delete = ['site', 'user', 'group']

    def __str__(self):
        return _('{} in {}').format(self.user, self.group)


dd.update_field(Membership, "user", verbose_name=_("User"))


class Memberships(dd.Table):
    model = 'groups.Membership'
    required_roles = dd.login_required(SiteAdmin)
    insert_layout = dd.InsertLayout("""
    user
    group
    remark
    """,
                                    window_size=(60, 'auto'))

    detail_layout = dd.DetailLayout("""
    user
    group
    remark
    """,
                                    window_size=(60, 'auto'))


class MembershipsByGroup(Memberships):
    label = _("Memberships")
    master_key = 'group'
    column_names = "user remark workflow_buttons *"
    stay_in_grid = True
    display_mode = ((None, constants.DISPLAY_MODE_SUMMARY), )

    # summary_sep = comma

    @classmethod
    def row_as_summary(cls, ar, obj, **kwargs):
        return obj.user.as_summary_item(ar, **kwargs)
        # if ar is None:
        #     return escape(str(obj.user))
        # return ar.obj2htmls(obj, str(obj.user), **kwargs)


class MembershipsByUser(Memberships):
    master_key = 'user'
    column_names = "group remark *"
    order_by = ['group__ref']
    display_mode = ((None, constants.DISPLAY_MODE_SUMMARY), )
    required_roles = dd.login_required(SiteUser)

    @classmethod
    def row_as_summary(cls, ar, obj, **kwargs):
        return obj.group.as_summary_item(ar, **kwargs)

class AllMemberships(Memberships):
    required_roles = dd.login_required(SiteAdmin)
