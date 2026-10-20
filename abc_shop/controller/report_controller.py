"""Presentation layer: UC25-UC28 management dashboard and reports (Manager)."""
from controller.http import Response
from view import templates


class ReportController:

    def __init__(self, shop):
        self.reports = shop.reports

    def dashboard(self, request):
        manager = request.user
        return Response(templates.reports(
            request, self.reports.dashboard(manager), self.reports.sales_report(manager),
            self.reports.inventory_report(manager), self.reports.exception_report(manager)))
