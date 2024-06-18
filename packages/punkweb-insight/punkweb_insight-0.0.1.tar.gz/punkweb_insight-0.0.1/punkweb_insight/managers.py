from django.db import models


class PageViewManager(models.Manager):
    def data_chartjs(self, start, end, exclude_staff=False):
        page_views = self.filter(
            created_at__date__gte=start,
            created_at__date__lte=end,
        ).select_related("visitor")

        if exclude_staff:
            page_views = page_views.exclude(visitor__user__is_staff=True)

        data = {
            "labels": [],
            "datasets": [
                {
                    "label": "Page Views",
                    "data": [],
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 1,
                },
            ],
        }

        # Group by date, each day is a label and a data point

        for page_view in page_views.order_by("created_at"):
            date = page_view.created_at.date().isoformat()
            if date not in data["labels"]:
                data["labels"].append(date)
                data["datasets"][0]["data"].append(0)

            index = data["labels"].index(date)
            data["datasets"][0]["data"][index] += 1

        return data
