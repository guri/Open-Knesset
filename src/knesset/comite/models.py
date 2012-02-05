from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from djangoratings.fields import RatingField

from tagging.fields import TagField
from links.fields import LinksField
from events.fields import EventsField

ISSUE_PUBLISHED, ISSUE_FLAGGED, ISSUE_REJECTED,\
ISSUE_ACCEPTED, ISSUE_APPEAL, ISSUE_DELETED = range(6)
PUBLIC_ISSUE_STATUS = ( ISSUE_PUBLISHED, ISSUE_ACCEPTED)

class Issue(models.Model):
    ''' Issue is used to hold a issue to explore and invistigate '''

    creator = models.ForeignKey(User, related_name='concpets')
    editors = models.ManyToManyField(User, null=True, blank=True, related_name = 'editing_issues')
    title = models.CharField(max_length=256,
                             verbose_name = _('Title'))
    description = models.TextField(blank=True,
                                   verbose_name = _('Description'))
    status = models.IntegerField(choices = (
        (ISSUE_PUBLISHED, _('published')),
        (ISSUE_FLAGGED, _('flagged')),
        (ISSUE_REJECTED, _('rejected')),
        (ISSUE_ACCEPTED, _('accepted')),
        (ISSUE_APPEAL, _('appeal')),
        (ISSUE_DELETED, _('deleted')),
            ), default=ISSUE_PUBLISHED)
    rating = RatingField(range=7, can_change_vote=True, allow_delete=True)
    links = LinksField()
    events = EventsField()
    tags = TagField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    log = models.TextField(default="", blank=True)

    class Meta:
        verbose_name = _('Issue')
        verbose_name_plural = _('Issues')

    @models.permalink
    def get_absolute_url(self):
        return ('issue-detail', [str(self.id)])

    def __unicode__(self):
        return "%s" % self.title

class Comite(models.Model):
    ''' Comite - a simpler committee
    '''
    name = models.CharField(max_length=256)
    description = models.TextField(null=True,blank=True, verbose_name=_('Description'))

    issues = models.ManyToManyField(Issue, related_name='comites', verbose_name=_('Issue'))
    links = LinksField()
    events = EventsField()

    members = models.ManyToManyField(User, related_name='comites', verbose_name=_('Members'))
    chairs = models.ManyToManyField(User, related_name='comites_chairs', verbose_name=_('Chairmans'))

    class Meta:
        verbose_name = _('Committee')
        verbose_name_plural = _('Committees')

    @models.permalink
    def get_absolute_url(self):
        return ('comite-detail', [str(self.id)])

    def __unicode__(self):
        return "%s" % self.name

