# -*- coding: UTF-8 -*-
# Copyright 2019-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _
from lino.utils import join_words

from lino_xl.lib.groups.models import *
# from lino.modlib.users.mixins import UserAuthored


# class Group(Group, UserAuthored):
class Group(Group):

    class Meta(Group.Meta):
        app_label = 'groups'
        abstract = dd.is_abstract_model(__name__, 'Group')
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    # @classmethod
    # def get_request_queryset(cls, ar, **filter):
    #     qs = super().get_request_queryset(ar, **filter)
    #     user = ar.get_user()
    #     if user.user_type.has_required_roles([SiteAdmin]):
    #         return qs
    #     if user.is_anonymous:
    #         return qs.none()
    #     # either a public group, or I am the owner, or I am a member
    #     q1 = Q(private=False)
    #     q2 = Q(user=user)
    #     q3 = Q(members__user=user)
    #     qs = qs.filter(q1|q2|q3).distinct()
    #     return qs


# dd.update_field(Group, 'user', verbose_name=_("Owner"))

Groups.column_names = 'detail_link private MembershipsByGroup *'
Groups.detail_layout = """
name
ref:10 id private
description MembershipsByGroup
# comments.CommentsByRFC tickets.SitesByGroup
tickets.TicketsByGroup
"""
MyGroups.column_names = 'detail_link tickets.TicketsByGroup *'
