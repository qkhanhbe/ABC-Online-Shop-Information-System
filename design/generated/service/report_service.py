from __future__ import annotations



class ReportService:

    def dashboard(self, manager: User) -> Map:
        raise NotImplementedError

    def sales_report(self, manager: User, start: str, end: str) -> Map:
        raise NotImplementedError

    def inventory_report(self, manager: User) -> Map:
        raise NotImplementedError

    def exception_report(self, manager: User) -> Map:
        raise NotImplementedError
