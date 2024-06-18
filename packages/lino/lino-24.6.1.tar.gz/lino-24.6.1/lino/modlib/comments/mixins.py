# -*- coding: UTF-8 -*-
# Copyright 2015-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.db.models import Q

from lino.api import dd, rt, _
from lino.modlib.memo.mixins import MemoReferrable

from .choicelists import Emotions
from .roles import PrivateCommentsReader


class MyEmotionField(dd.VirtualField):
    """
    An editable virtual field to get and set my emotion about that comment.

    My emotion is stored in the Emotion table.

    """

    editable = True
    empty_values = set([None])

    def __init__(self, *args, **kwargs):
        kwargs.update(blank=True)
        dd.VirtualField.__init__(self, Emotions.field(*args, **kwargs), None)
        self.choicelist = self.return_type.choicelist

    def set_value_in_object(self, ar, obj, value):
        if ar is None:
            raise Exception("20201215")
            # dd.logger.info("20201215 oops")
            # return
        mr, created = rt.models.comments.Reaction.objects.get_or_create(
            user=ar.get_user(), comment=obj
        )
        mr.emotion = value
        mr.full_clean()
        mr.save()

    def value_from_object(self, obj, ar=None):
        return obj.get_my_emotion(ar)


class CommentField(dd.VirtualField):
    """
    An editable virtual field to add a comment about that database object.

    """

    editable = True
    simple_elem = True

    def __init__(self, slave_table):
        t = models.TextField(_("My comment"), blank=True)
        super().__init__(t, None)
        self.slave_table = slave_table

    def set_value_in_object(self, ar, obj, value):
        actor = rt.models.resolve(self.slave_table)
        sar = actor.request(
            master_instance=obj, request=ar.request, renderer=ar.renderer
        )
        obj = sar.create_instance(body=value)
        obj.full_clean()
        obj.save_new_instance(sar)
        ### Following line below is NOT in need anymore,
        ### CommentsByRFC.live_panel_update does the update for delayed value already
        # ar.set_response(refresh_delayed_value=str(actor))
        # ar.set_response(refresh=True)

    def value_from_object(self, obj, ar=None):
        return None


class Commentable(MemoReferrable):
    class Meta(object):
        abstract = True

    create_comment_template = _("Created new {model} {obj}.")

    comment = CommentField("comments.CommentsByRFC")

    def on_commented(self, comment, ar, cw):
        pass

    def get_rfc_description(self, ar):
        return ""

    def get_comment_group(self):
        return None

    if dd.is_installed("comments"):

        def save_new_instance(self, ar):
            super().save_new_instance(ar)
            if rt.settings.SITE.loading_from_dump:
                return

            if self.create_comment_template is not None:
                txt = self.create_comment_template.format(
                    model=self.__class__._meta.verbose_name, obj=self
                )
                # txt = self.get_create_comment(ar)
                comment = rt.models.comments.Comment(body=txt, owner=self)
                comment.on_create(ar)
                comment.full_clean()
                comment.save_new_instance(ar)
                # print("20220916 save_new_instance() created", comment, txt)

    @classmethod
    def add_comments_filter(cls, qs, ar):
        return qs

    def is_comment_private(self, comment, ar):
        """Whether the given comment should be private."""
        return dd.plugins.comments.private_default
