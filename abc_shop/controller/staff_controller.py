"""Presentation layer: UC19 Process Orders, UC20 Manage Inventory, UC21-22 shipment,
UC24 Manage Replenishment, UC18 Manage Reviews (staff screens)."""
from controller.http import Response
from service.auth_service import AuthService
from view import templates


class StaffController:

    def __init__(self, shop):
        self.order_service = shop.orders
        self.shipping = shop.shipping
        self.inventory_service = shop.inventory
        self.review_service = shop.reviews
        self.catalog = shop.catalog

    def orders(self, request):
        user = request.user
        queue = self.order_service.processing_queue(user) if user and user.can("process_orders") else []
        picks = self.shipping.pick_list(user) if user and user.can("shipment") else []
        ready = self.shipping.ready_list(user) if user and user.can("shipment") else []
        if not (user and (user.can("process_orders") or user.can("shipment"))):
            AuthService.require(user, "process_orders")
        return Response(templates.staff_orders(request, queue, picks, ready))

    def order_action(self, request, order_id, action):
        user = request.user
        if action == "process":
            order = self.order_service.start_processing(user, order_id)
        elif action == "hold":
            order = self.order_service.hold(user, order_id, request.get("reason") or "manual check")
        elif action == "pack":
            shipment = self.shipping.mark_packed(user, order_id)
            return Response.redirect("/staff/orders", f"{order_id} packed as {shipment.shipment_id}: "
                                     "Ready for Shipment.", request)
        elif action == "ship":
            shipment = self.shipping.arrange_delivery(user, order_id)
            return Response.redirect("/staff/orders", f"{order_id} handed to carrier "
                                     f"{shipment.carrier_ref}.", request)
        else:
            return Response.redirect("/staff/orders", "Unknown action.", request)
        return Response.redirect("/staff/orders", f"{order_id}: {order.status}.", request)

    def inventory(self, request):
        AuthService.require(request.user, "inventory")
        rows = [(card["product"], self.inventory_service.stock_of(card["product"].product_id))
                for card in self.catalog.browse()]
        return Response(templates.inventory(request, rows, self.inventory_service.low_stock()))

    def inventory_event(self, request):
        user = request.user
        product_id = request.get("product_id")
        if request.get("kind") == "REPLENISH":
            rq = self.inventory_service.request_replenishment(user, product_id, int(request.get("qty")))
            return Response.redirect("/staff/inventory", f"Replenishment {rq} requested.", request)
        result = self.inventory_service.manual_event(user, product_id, request.get("kind"),
                                                     int(request.get("qty")), request.get("reference"),
                                                     request.get("reason"))
        note = f"{result['event'].event_id} recorded; available = {result['stock'].available}"
        if result["low"]:
            note += " - below threshold, consider replenishment (UC24)"
        return Response.redirect("/staff/inventory", note, request)

    def reviews(self, request):
        queue = self.review_service.moderation_queue(request.user)
        return Response(templates.moderation(request, queue))

    def moderate(self, request, review_id):
        review = self.review_service.moderate(request.user, review_id, request.get("decision") == "approve")
        return Response.redirect("/admin/reviews", f"{review_id} {review.status}.", request)
