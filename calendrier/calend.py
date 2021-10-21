from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc
from django.utils.translation import gettext_lazy as _


class EventCalendar(HTMLCalendar):
    def __init__(self, pEvents):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(pEvents.order_by("date"))

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += " today"
            if day in self.events:
                cssclass += " filled"
                body = []
                for ev in self.events[day]:
                    body.append('<a href="/agenda/' + '%s"' % ev.id)
                    if ev.calendrier == "C":
                        body.append('style="color:#160083">'+esc(ev.nom))
                    elif ev.calendrier == "D":
                        body.append('style="color:#770083">'+esc(ev.nom))
                    else:
                        body.append('>'+esc(ev.nom))
                    body.append("</a><br/>")
                return self.day_cell(
                    cssclass,
                    '<div class="dayNumber">%d</div> %s' % (day, "".join(body)),
                )
            return self.day_cell(cssclass, '<div class="dayNumber">%d</div>' % day)
        return self.day_cell("noday", "&nbsp;")

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, pEvents):
        def field(ev):
            return ev.date.day

        return dict([(dat, list(items)) for dat, items in groupby(pEvents, field)])

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
