"""Texts of the defence showcase (Vietnamese). Markers: {fig:CODE} {code:file:Symbol} {file:path} {test:name}."""

DIAGRAMS = [
    ("Chương 1 - Giới thiệu và yêu cầu", [
        ("STK01", "Bản đồ các bên liên quan: nội bộ, bên ngoài và mối quan tâm"),
        ("BP01", "Quy trình nghiệp vụ tổng thể (BPMN): khách, các làn của shop, đối tác"),
        ("PT01", "Cây vấn đề: nguyên nhân gốc, 6 vấn đề, vấn đề cốt lõi, hệ quả"),
        ("UC00", "Use case tổng quát: mọi actor, use case chính của từng phân hệ"),
        ("UCD1", "Use case chi tiết: tài khoản và danh mục"),
        ("UCD2", "Use case chi tiết: giỏ hàng, đặt hàng, thanh toán"),
        ("UCD3", "Use case chi tiết: quản trị"),
        ("UCD4", "Use case chi tiết: vận hành và báo cáo")]),
    ("Chương 2 - Phân tích", [
        ("CL01", "Class phân tích: 22 lớp, chỉ có tên thuộc tính; 4 loại sản phẩm kế thừa thẳng Product"),
        ("AD05", "Activity có làn: tìm kiếm sản phẩm (UC05)"),
        ("AD06", "Activity có làn: quản lý giỏ hàng (UC07, UC30)"),
        ("AD01", "Activity có làn: đặt hàng, thanh toán (UC08)"),
        ("AD07", "Activity có làn: theo dõi đơn (UC11)"),
        ("AD08", "Activity có làn: quản lý sản phẩm (UC14)"),
        ("AD03", "Activity: quản lý tồn kho (UC20)"),
        ("AD02", "Activity có làn: xử lý và giao đơn"),
        ("CTX01", "Sơ đồ ngữ cảnh: hệ thống và các thực thể bên ngoài"),
        ("DFD0", "DFD mức 0: 8 tiến trình, 7 kho dữ liệu"),
        ("DFD1", "DFD mức 1 của tiến trình 4.0 Đặt hàng và thanh toán"),
        ("SD01", "Sequence phân tích (BCE): đặt hàng"),
        ("SD02", "Sequence phân tích (BCE): theo dõi đơn"),
        ("ST01", "Máy trạng thái của đơn hàng")]),
    ("Chương 3 - AI trong thương mại điện tử", [
        ("UC_AI", "Use case có AI"),
        ("CMP01", "Ba lớp của phân hệ tìm kiếm AI"),
        ("SD03", "Tìm kiếm bằng giọng nói"),
        ("SD04", "Tìm kiếm bằng ảnh"),
        ("AD04", "Pipeline tóm tắt đánh giá")]),
    ("Chương 4 - Data Model", [
        ("DM01", "Data model class: CL01 + định danh, kiểu, bản số, tên quan hệ, «ORM Persistable»"),
        ("ERD01", "ERD do syncClassesToErd sinh từ DM01: 22 bảng, 24 khoá ngoại, cùng lưới với DM01")]),
    ("Chương 5 - Thiết kế", [
        ("DCL01", "Class thiết kế (model): DM01 + method của code, điều hướng"),
        ("DCL02", "Class thiết kế (dao): interface DAO, lớp SQLite, Database"),
        ("DCL03", "Class thiết kế (service): các service nghiệp vụ và gateway"),
        ("DCL04", "Class thiết kế (ai): tìm kiếm, phân tích đánh giá, gợi ý"),
        ("DCL05", "Class thiết kế (controller): router WebApp và các controller"),
        ("PKG01", "Các tầng (package) và phụ thuộc «use» đi xuống"),
        ("LAY01", "Layer của use case tìm kiếm: lớp theo tầng, operation và phụ thuộc"),
        ("LAY02", "Layer của giỏ hàng và thanh toán: lớp theo tầng, operation và phụ thuộc"),
        ("LAY03", "Layer của đăng ký, đăng nhập (UC01, UC02)"),
        ("LAY04", "Layer của thanh toán thẻ (UC09): PaymentGateway và SimulatedPaymentProvider"),
        ("LAY05", "Layer của gợi ý sản phẩm (UC33, UC34)"),
        ("SD05", "Sequence thiết kế: checkout qua các tầng"),
        ("SD06", "Sequence thiết kế: theo dõi đơn qua các tầng"),
        ("SD07", "Sequence thiết kế: đăng nhập (alt đúng/sai mật khẩu)"),
        ("SD08", "Sequence thiết kế: thanh toán thẻ (alt SUCCEEDED/DECLINED)"),
        ("SD09", "Sequence thiết kế: gợi ý sản phẩm (opt dựng mô hình, loop chấm điểm)"),
        ("CMP02", "Sơ đồ thành phần của hệ thống"),
        ("DEP01", "Sơ đồ triển khai")]),
]

# Kind of each diagram as Visual Paradigm stores it (DIAGRAM_TYPE in the .vpp), shown after the code in the gallery.
KINDS = {
    "BP01": "BPMN Business Process Diagram",
    "STK01": "Stakeholder Map, vẽ bằng Class Diagram",
    "PT01": "Problem Tree, vẽ bằng Flowchart",
    "CTX01": "Context Diagram, Data Flow Diagram mức ngữ cảnh",
    "DFD0": "Data Flow Diagram mức 0",
    "DFD1": "Data Flow Diagram mức 1",
    "UC00": "Use Case Diagram tổng quan",
    "UC_AI": "Use Case Diagram",
    "CL": "Analysis Class Diagram (có method)",
    "DM": "Class Diagram «ORM Persistable»",
    "LAY": "Class Diagram theo tầng (Layer)",
    "ST01": "State Machine Diagram",
    "ERD": "ERD sinh tự động bằng syncClassesToErd",
    "CMP": "Component Diagram",
    "DEP": "Deployment Diagram",
    "PKG": "Package Diagram",
    "DCL": "Design Class Diagram",
    "UCD": "Use Case Diagram chi tiết",
    "AD": "Activity Diagram",
}


def kind(code):
    """Exact code first, then the longest matching prefix."""
    if code in KINDS:
        return KINDS[code]
    if code.startswith("SD"):
        if code in ("SD01", "SD02"):
            return "Sequence Diagram (Analysis)"
        return "Sequence Diagram" if code in ("SD03", "SD04") else "Sequence Diagram (Design)"
    return next((KINDS[k] for k in sorted(KINDS, key=len, reverse=True) if code.startswith(k)), "")


PHASES = [
    ("Yêu cầu", "Khảo sát (A01): bên liên quan {fig:STK01}, quy trình {fig:BP01}, cây vấn đề {fig:PT01}; 24 FR, 12 NFR, 32 use case {fig:UC00}."),
    ("Phân tích", "Class phân tích có kế thừa, chỉ tên thuộc tính {fig:CL01}; 8 activity ({fig:AD05}, {fig:AD01} ...); ngữ cảnh {fig:CTX01}; DFD, sequence BCE, trạng thái."),
    ("Data Model", "CL01 + ID, kiểu, «ORM Persistable» = {fig:DM01} → syncClassesToErd sinh {fig:ERD01} (22 bảng, 24 khoá ngoại)."),
    ("Thiết kế", "Class thiết kế = data model class + method {fig:DCL01}; generateSql → {file:design/create_tables.sql}; tầng {fig:PKG01} {fig:LAY02} {fig:LAY04}; generateCode → {file:design/generated}."),
    ("Cài đặt và kiểm chứng", "Python, SQLite, 45 test; check_code.py 74/74 lớp khớp; build_db.py 22/22 bảng khớp; evaluate.py; ảnh chụp demo."),
]

# Section C: three chains read left to right; under each, what changed, why, and what it brought.
# A step shows a diagram (fig), a real excerpt of the code (code / sql) or a screenshot of the running shop (shot).
EVOLUTION = [
    dict(title="1. Lớp phân tích → lớp thiết kế → code",
         note="Product và bốn loại sản phẩm kế thừa thẳng, phần thầy góp ý",
         steps=[
             dict(label="Phân tích", fig="CL01",
                  cap="Footwear, Apparel, Bag, Watch kế thừa thẳng Product; thuộc tính chưa có kiểu, trách nhiệm đã là method."),
             dict(label="Thiết kế", fig="DCL01",
                  cap="Class phân tích + method: kiểu của data model, tham số có kiểu, kiểu trả về, đầu quan hệ điều hướng."),
             dict(label="Code", code=("model/product.py", ["Product", "Bag"]),
                  cap="Cùng tên lớp, thuộc tính và method với DCL01; {file:design/check_code_output.txt}: 74/74 lớp khớp."),
         ],
         what=["kế thừa được giữ từ phân tích đến code: <code>class Bag(Product)</code>, không có lớp trung gian chi tiết",
               "thuộc tính thành trường có kiểu: <code>capacity_l: float</code>, <code>battery_days: Optional[int]</code>",
               "trách nhiệm thành method có kiểu: <code>spec_rows() -> List&lt;String&gt;</code>, <code>update_price(new_price: Float)</code>",
               "liên kết sang aggregate khác thành khoá: <code>Cart.customer_id</code>, <code>Product.category_id</code>"],
         why=["túi <i>là một</i> sản phẩm: có mọi thuộc tính của Product và thêm thuộc tính riêng, không cột rỗng",
              "quy tắc BR-CAT-01 (loại sản phẩm đúng loại của danh mục) nằm cạnh dữ liệu nó kiểm tra: {code:service/catalog_service.py:CatalogService.save_product}",
              "đối tượng ở aggregate khác được DAO khác nạp, nên chỉ giữ khoá"],
         gain=["trang sản phẩm hiện bảng thông số đúng loại mà view không cần if theo loại ({code:model/product.py:Product.spec_rows})",
               "tìm kiếm AI tìm được theo chất liệu, dung tích… nhờ {code:model/product.py:Product.search_text}",
               "thêm loại hàng mới là thêm một lớp con và một bảng: {test:test_each_product_is_of_the_kind_of_its_category}"]),
    dict(title="2. Sequence phân tích → sequence thiết kế → lúc chạy",
         note="UC08 Place Order / Checkout",
         steps=[
             dict(label="Phân tích", fig="SD01",
                  cap="CheckoutForm (boundary), CheckoutController (control), Cart, Order, StockLevel (entity)."),
             dict(label="Thiết kế", fig="SD05",
                  cap="OrderController → CheckoutService → OrderDAO, InventoryService, PaymentService với tên hàm thật."),
             dict(label="Code", code=("service/checkout_service.py", ["CheckoutService.place_order"]),
                  pick=r"def |idempotency_key = |existing|transaction|create_from_cart|save_order|reserve_order|request_payment|cart\.clear",
                  cap="Một bước của use case trong một hàm; transaction bao quanh tạo đơn và giữ hàng."),
             dict(label="Lúc chạy", shot="demo_results/web_04_checkout.png",
                  cap="Trang thanh toán đang chạy: mã WELCOME10, phí giao hàng, tổng tiền tính ở một chỗ."),
         ],
         what=["control của phân tích tách thành {code:controller/order_controller.py:OrderController.checkout} (HTTP, session, form) và CheckoutService (quy tắc nghiệp vụ)",
               "entity được truy cập qua DAO; tầng lưu trữ hiện rõ trên sơ đồ",
               "thông điệp 3–4 của SD05: tra idempotency key trước khi tạo đơn (luồng A7, gửi lại form)",
               "thông điệp 8–10 nằm trong {code:dao/database.py:Database.transaction}"],
         why=["tầng phân tích không biết HTTP hay SQL; tầng thiết kế thì phải biết",
              "tạo đơn và giữ hàng phải cùng thành công hoặc cùng không",
              "khách bấm hai lần không được tạo hai đơn; đối tác thanh toán chỉ được gọi sau khi transaction commit"],
         gain=["gửi lại form trả về đúng đơn cũ: {test:test_repeated_submission_returns_the_same_order}",
               "thanh toán bị từ chối thì trả hàng giữ chỗ và giữ nguyên giỏ: {test:test_declined_payment_releases_reservation_and_keeps_cart}",
               "đối tác không bao giờ nhận yêu cầu cho một đơn không tồn tại"]),
    dict(title="3. Class ORM → ERD sinh → SQL sinh → database",
         note="Data Model ⇒ DB bằng tool của plugin MCP, không vẽ tay",
         steps=[
             dict(label="Class ORM", fig="DM01",
                  cap="22 lớp phân tích thêm kiểu, định danh và «ORM Persistable»; mọi quan hệ có tên và bản số hai đầu."),
             dict(label="ERD (sinh)", fig="ERD01",
                  cap="syncClassesToErd sinh 22 bảng, 24 khoá ngoại; quyết định khoá áp lại bằng tool ({file:design/v5_tool_log.txt})."),
             dict(label="SQL (sinh)", sql=("design/create_tables.sql", "Bag"),
                  cap="generateSql (SQLite) viết {file:design/create_tables.sql}: khoá chính, khoá ngoại có tên."),
             dict(label="Database", shot="demo_results/web_03b_product_bag.png",
                  cap="Ứng dụng chạy trên đúng 22 bảng đó: trang một chiếc túi đọc Product + bảng Bag ({file:design/build_db_output.txt})."),
         ],
         what=["kế thừa thành bảng con dùng chung khoá (table per subclass): Bag, Watch… có <code>product_id</code> vừa là PK vừa là FK",
               "composition thành khoá ghép: CartItem (cart_id, product_id), OrderItem, Milestone",
               "Order đổi tên Orders (ORDER là từ khoá SQL); promo_code là FK được rỗng từ bản số 0..1"],
         why=["ERD không vẽ lại bằng tay, nên không lệch với class diagram",
              "chỗ nào bộ sinh không tự quyết (bảng không có định danh) thì quyết bằng tool và ghi lại",
              "schema.sql chỉ thêm cái ERD không chứa: NOT NULL, CHECK, UNIQUE, DEFAULT, 4 trigger, 2 bảng kỹ thuật"],
         gain=["22/22 bảng của ứng dụng giống hệt SQL sinh ra (cột, khoá chính, khoá ngoại)",
               "ứng dụng nạp một tháng dữ liệu vào database sinh ra; 5/5 câu lệnh sai khoá bị chặn",
               "{test:test_database_trigger_rejects_a_kind_row_of_the_wrong_kind}"]),
    dict(title="4. Class thiết kế theo package → code sinh → code ứng dụng",
         note="Layer → sinh code (generateCode, Python)",
         steps=[
             dict(label="Thiết kế", fig="DCL02",
                  cap="Mỗi package một class diagram: model, dao, service, ai, controller; interface và lớp cài đặt."),
             dict(label="Code sinh", code=("design/generated/model/cart.py", ["Cart"]),
                  cap="generateCode viết {file:design/generated}: 74 lớp trong 5 package, mỗi lớp một module."),
             dict(label="Code ứng dụng", code=("model/cart.py", ["Cart"]),
                  cap="check_code.py so từng lớp: lớp cha, thuộc tính, method và tên tham số."),
         ],
         what=["mỗi operation của sơ đồ thành method stub có kiểu; đầu quan hệ điều hướng thành field (<code>_items</code>)",
               "interface DAO thành lớp trừu tượng, lớp SQLite kế thừa nó"],
         why=["code ứng dụng và sơ đồ phải nói cùng một điều; phép so tự động bắt được chỗ lệch",
              "thử thêm một method chỉ có trên sơ đồ: check_code.py báo ngay"],
         gain=["74/74 lớp khớp ({file:design/check_code_output.txt})", "sơ đồ thiết kế không trôi khỏi code khi code thay đổi"]),
]


TRACE = [
    ("UC08 Đặt hàng / Checkout", [
        ("Yêu cầu", "FR08–FR10, NFR07 (không trùng đơn), BR: giữ hàng khi tạo đơn"),
        ("Phân tích", "Đặc tả UC08 (luồng chính, A1–A7, E1), {fig:AD01}, {fig:SD01}, {fig:DFD1}, {fig:ST01}"),
        ("Thiết kế", "{fig:SD05}, {fig:DCL01}, {fig:PKG01}"),
        ("Database", "Orders (UNIQUE idempotency_key), OrderItem, StatusChange, payment, InventoryEvent"),
        ("Code", "{code:controller/order_controller.py:OrderController.checkout} → {code:service/checkout_service.py:CheckoutService.place_order} → "
                 "{code:model/order.py:Order.create_from_cart} → {code:dao/sqlite_dao.py:SqliteOrderDAO.save_order}, {code:service/inventory_service.py:InventoryService.reserve_order}, "
                 "{code:service/payment_service.py:PaymentService.request_payment}"),
        ("Test", "{test:test_successful_checkout_reserves_stock_pays_and_clears_cart}, {test:test_repeated_submission_returns_the_same_order}, "
                 "{test:test_insufficient_stock_stops_checkout_without_side_effects}, {test:test_payment_callbacks_are_verified_and_idempotent}")]),
    ("UC07 Quản lý giỏ hàng (thêm sản phẩm)", [
        ("Yêu cầu", "FR07; include UC30 Kiểm tra hàng còn"),
        ("Phân tích", "{fig:UCD2}, {fig:CL01} (Cart ◆ CartItem)"),
        ("Thiết kế", "{fig:LAY02} (các tầng controller → service → dao → model của giỏ hàng và thanh toán), {fig:DCL01}"),
        ("Database", "cart (UNIQUE customer_id), CartItem (khoá (cart_id, product_id))"),
        ("Code", "{code:controller/order_controller.py:OrderController.add_to_cart} → {code:service/cart_service.py:CartService.add_item} → "
                 "{code:model/cart.py:Cart.add_item} → {code:dao/sqlite_dao.py:SqliteCartDAO.update_cart}"),
        ("Test", "{test:test_cart_adds_to_an_existing_line_and_totals_the_lines}, {test:test_customer_buys_through_the_web}")]),
    ("UC06 Xem chi tiết sản phẩm (Category → bảng của loại sản phẩm)", [
        ("Yêu cầu", "FR06; góp ý của thầy về Product/Category; BR-CAT-01"),
        ("Phân tích", "{fig:CL01} (4 loại sản phẩm kế thừa thẳng Product), {fig:AD08}"),
        ("Thiết kế", "{fig:DM01} → {fig:ERD01} (bảng con dùng chung khoá), {fig:DCL01}, {fig:DCL02}"),
        ("Database", "Category.detail_kind, Product, Footwear / Apparel / Bag / Watch (PK = FK product_id), trigger *_kind"),
        ("Code", "{code:controller/shop_controller.py:ShopController.product} → {code:service/catalog_service.py:CatalogService.product_detail} → "
                 "{code:dao/sqlite_dao.py:SqliteProductDAO._to_product} → {code:model/product.py:Product.spec_rows}"),
        ("Test", "{test:test_product_page_shows_the_attributes_of_the_kind}, {test:test_service_rejects_a_product_of_the_wrong_kind}, "
                 "{test:test_database_trigger_rejects_a_kind_row_of_the_wrong_kind}")]),
    ("UC05 Tìm kiếm sản phẩm bằng AI", [
        ("Yêu cầu", "FR05, AI-R1 đến AI-R4, AI-N3 (luôn có phương án không AI)"),
        ("Phân tích", "{fig:UC_AI}, {fig:SD03}, {fig:SD04}"),
        ("Thiết kế", "{fig:CMP01}, {fig:PKG01} (package ai)"),
        ("Database", "product, bảng của loại sản phẩm (từ khoá), StockLevel (S_business); VectorIndex trong bộ nhớ"),
        ("Code", "{code:controller/shop_controller.py:ShopController.search} → {code:ai/search/query_service.py:QueryService.text_query} → "
                 "{code:ai/search/search_service.py:SearchService.search} → {code:ai/search/ranking_service.py:RankingService.rank}"),
        ("Test", "{test:test_text_voice_and_price_filter}, {test:test_image_and_multimodal_search}, {test:test_search_uses_the_attributes_of_the_kind}")]),
]

SCRIPT = [
    ("0:00–0:45", "Bài toán: thông tin rời rạc và chậm; 6 vấn đề và nguyên nhân gốc.", "Showcase mục A, {fig:PT01}"),
    ("0:45–1:45", "Quy trình và yêu cầu: BPMN, use case tổng quát, đặc tả UC08.", "{fig:BP01}, {fig:UC00}, PDF chương 1"),
    ("1:45–3:00", "Phân tích → thiết kế: CL01 (kế thừa, chỉ tên thuộc tính) → DM01 (+ID, kiểu, ORM) → DCL01 (+method) → code; SD01 → SD05.", "Mở VP: Model Explorer có 5 project con 1 Requirements → 5 Design; mở 2 Analysis/CL01, 4 Data Model/DM01, 5 Design/DCL01, SD05; showcase mục C"),
    ("3:00–4:00", "Data model: DM01 «ORM Persistable» → syncClassesToErd → ERD01 → generateSql → build_db; generateCode → check_code.", "Mở VP: DM01, ERD01; {file:design/v5_tool_log.txt}"),
    ("4:00–5:00", "Truy vết: từ UC08 đến place_order và test.", "IDE: checkout_service.py dòng place_order; showcase mục D"),
    ("5:00–6:30", "Demo: tìm kiếm AI, trang P16, checkout, đơn bị từ chối thanh toán, báo cáo.", "Trình duyệt localhost:8000"),
    ("6:30–7:00", "Kiểm chứng và hạn chế: 45 test, 74/74 lớp, 22/22 bảng; phần còn thiếu.", "Showcase mục G"),
]

DECISIONS = [
    ("Monolith phân lớp (MVC + service + DAO)", "Một ứng dụng triển khai, chia lớp để đổi từng phần độc lập (NFR09).",
     "Microservices: thêm lời gọi mạng và nhất quán phân tán cho checkout vốn cần một transaction.", "{fig:PKG01}, {test:test_dependencies_only_point_downwards}"),
    ("Lớp service giữa controller và DAO", "Quy tắc của use case ở một chỗ, test được không cần HTTP.",
     "Quy tắc trong controller: trộn HTTP với tồn kho và thanh toán.", "{code:service/checkout_service.py:CheckoutService}"),
    ("Loại sản phẩm là lớp con của Product (bảng con dùng chung khoá)", "Không cột rỗng, NOT NULL theo loại, thêm loại là thêm lớp con và bảng.",
     "Một bảng rộng; bảng EAV mất kiểu và ràng buộc.", "{fig:CL01}, {fig:ERD01}, {code:dao/sqlite_dao.py:SqliteProductDAO._to_product}"),
    ("Tồn kho là chuỗi sự kiện", "Mọi con số giải thích được; không bao giờ âm.",
     "Sửa trực tiếp một con số: không truy được vì sao lệch.", "{code:model/inventory.py:StockLevel.apply}"),
    ("Đơn hàng giữ bảng chuyển trạng thái", "Service quyết định khi nào, model quyết định có hợp lệ không.",
     "Kiểm tra trạng thái rải trong từng service.", "{code:model/order.py:Order.change_status}, {fig:ST01}"),
    ("Idempotency key cho checkout, mã tham chiếu cho thanh toán", "Gửi lại form hay callback lặp không tạo đơn hay kết quả thứ hai (NFR07).",
     "Dựa vào người dùng không bấm hai lần.", "{test:test_repeated_submission_returns_the_same_order}"),
    ("Quy tắc ở cả service và database", "Service báo lỗi dễ hiểu; database chặn mọi đường khác.",
     "Chỉ kiểm trong code: script sửa tay có thể phá dữ liệu.", "{file:design/build_db_output.txt}"),
]

G1, G2, G3, G4, G5 = ("1. Nền tảng HTTT và SDLC", "2. Kỹ nghệ yêu cầu", "3. Quy trình nghiệp vụ và use case",
                      "4. Phân rã hệ thống và package", "5. Kiến trúc ba lớp")
G6, G7, G8, G9, G10 = ("6. Controller, Service, DAO, Model", "7. Thiết kế CSDL và chuẩn hoá", "8. Mô hình class và tương tác",
                       "9. Toàn vẹn dữ liệu, kiểm thử, chất lượng", "10. Đánh giá và bảo vệ dự án")

ANSWERS = [
    (G1, "Hệ thống thông tin là gì? Các thành phần và cách chúng phối hợp trong hệ thống của em?",
     "<p>Hệ thống thông tin là tập hợp con người, quy trình, dữ liệu, phần mềm và phần cứng/mạng cùng thu thập, xử lý, lưu và cung cấp "
     "thông tin để hỗ trợ hoạt động và quyết định. Trong ABC Online Shop: <b>con người</b> là khách hàng và 4 vai trò nhân viên "
     "({fig:STK01}); <b>quy trình</b> là chuỗi đặt hàng → thanh toán → giao hàng → báo cáo ({fig:BP01}); <b>dữ liệu</b> là 22 bảng "
     "({fig:ERD01}); <b>phần mềm</b> là ứng dụng ba lớp ({fig:PKG01}); <b>hạ tầng</b> là máy chủ ứng dụng và SQLite ({fig:DEP01}).</p>"
     "<p>Chúng phối hợp qua dữ liệu dùng chung: khi khách đặt hàng, service ghi đơn và sự kiện giữ hàng trong một transaction; "
     "nhân viên kho thấy ngay số lượng khả dụng mới; báo cáo của quản lý tính lại từ chính các bản ghi đó, không nhập tay.</p>"),
    (G1, "Khác nhau giữa phân tích hệ thống và thiết kế hệ thống? Ví dụ trong dự án.",
     "<p><b>Phân tích</b> trả lời hệ thống phải làm gì, độc lập công nghệ; <b>thiết kế</b> trả lời làm như thế nào. Ví dụ: {fig:CL01} có "
     "lớp Order với thuộc tính kiểu String, không có phương thức, không nói lưu ở đâu; {fig:DCL01} có <code>Order</code> với kiểu Python, "
     "phương thức <code>change_status()</code>, <code>create_from_cart(cart)</code>, trường khoá <code>customer_id</code>. Tương tự "
     "{fig:SD01} dùng đối tượng boundary/control/entity, còn {fig:SD05} dùng class thật OrderController, CheckoutService, OrderDAO. "
     "Database cũng tách mức: class phân tích {fig:CL01} chưa có kiểu và khoá, còn class ORM {fig:DM01} và ERD sinh tự động {fig:ERD01} thuộc data model.</p>"),
    (G1, "Các pha của SDLC và nhóm đã áp dụng thế nào trong học kỳ?",
     "<p>Lập kế hoạch/khảo sát → phân tích → thiết kế → cài đặt → kiểm thử → triển khai/bảo trì. Em áp dụng: A01 khảo sát và cây vấn đề "
     "({fig:PT01}); A02 yêu cầu, use case ({fig:UC00}); A03 và Test 01 mô hình phân tích, dữ liệu, thiết kế; A06 bản mẫu tìm kiếm ba lớp; "
     "tiểu luận nối tất cả thành ứng dụng chạy được, 45 test, demo. Quy trình lặp: khi viết code phát hiện sai lệch thì sửa mô hình "
     "(ví dụ bỏ trường Customer.orders, đổi các loại sản phẩm thành lớp con của Product sau góp ý của thầy) rồi sinh lại SQL và khung code.</p>"),
    (G1, "Các bên liên quan chính, trách nhiệm và ảnh hưởng của yêu cầu của họ tới thiết kế?",
     "<p>Nội bộ: Administrator (danh mục, khuyến mãi, duyệt đánh giá), Sales Staff (xử lý đơn), Warehouse Staff (tồn kho, đóng gói), Manager "
     "(báo cáo). Bên ngoài: Customer, Payment Provider, Shipping Provider, Supplier ({fig:STK01}). Ảnh hưởng: nhân viên kho cần "
     "\"tồn kho thật\" → tồn kho thành chuỗi sự kiện {code:model/inventory.py:StockLevel.apply}; quản lý cần báo cáo tái lập → báo cáo "
     "tính từ bản ghi, không lưu số tổng; đối tác thanh toán cần yêu cầu có mã duy nhất → cột <code>payment.attempt_ref UNIQUE</code> và "
     "callback có chữ ký HMAC; mỗi vai trò chỉ có quyền tối thiểu ({code:model/customer.py:User.can}).</p>"),
    (G1, "Yêu cầu chức năng và phi chức năng khác nhau thế nào? Ví dụ và ảnh hưởng tới thiết kế, cài đặt.",
     "<p>Chức năng nói hệ thống làm gì (FR08: kiểm tra giỏ và tính tổng chính thức trước khi đặt hàng); phi chức năng nói làm tốt đến mức nào "
     "(NFR07 toàn vẹn: một kết quả thanh toán chỉ đổi đơn một lần; NFR09 dễ bảo trì; NFR05 phân quyền). FR08 thành "
     "{code:service/cart_service.py:CartService.validate_cart}. NFR07 ảnh hưởng cả thiết kế lẫn database: idempotency key UNIQUE, "
     "attempt_ref UNIQUE, xử lý callback idempotent ({code:service/payment_service.py:PaymentService.handle_result}). NFR09 quyết định kiến "
     "trúc ba lớp và test kiến trúc {test:test_dependencies_only_point_downwards}.</p>"),
    (G2, "Nhóm thu thập yêu cầu bằng cách nào? Vì sao phù hợp?",
     "<p>Phân tích tài liệu tình huống của đề bài, phân tích bên liên quan, mô hình hoá quy trình đặt hàng–phản hồi và phân tích vấn đề–nguyên "
     "nhân–hệ quả (cây vấn đề). Không có shop thật để phỏng vấn, nên điều chưa rõ được ghi thành <b>câu hỏi khảo sát và giả định</b> "
     "(ví dụ: chỉ thanh toán trực tuyến, giữ hàng khi tạo đơn) thay vì tự bịa nguyên nhân. Các kỹ thuật này phù hợp vì nguồn duy nhất là "
     "tài liệu, và mỗi giả định được đánh dấu để kiểm chứng: nếu giả định sai (ví dụ có COD) thì biết chính xác trạng thái nào trong "
     "{fig:ST01} phải thêm.</p>"),
    (G2, "SRS là gì? Nội dung chính và vai trò với phân tích, thiết kế?",
     "<p>SRS (đặc tả yêu cầu phần mềm) mô tả đầy đủ, kiểm chứng được những gì hệ thống phải làm: phạm vi, actor, yêu cầu chức năng và phi chức "
     "năng, use case và đặc tả, quy tắc nghiệp vụ, ràng buộc, tiêu chí nghiệm thu. Trong tiểu luận, SRS là Chương 1: 24 FR, 12 NFR có "
     "MoSCoW, 32 use case, đặc tả UC08 với luồng A1–A7, E1, quy tắc nghiệp vụ, tiêu chí nghiệm thu và ma trận truy vết. SRS là đầu vào của "
     "phân tích (mỗi luồng trong đặc tả thành một nhánh trong {fig:AD01}, một thông điệp trong {fig:SD01}) và là thước đo của kiểm thử "
     "(tên test nhắc lại luồng, ví dụ {test:test_insufficient_stock_stops_checkout_without_side_effects} là A1).</p>"),
    (G2, "Chọn một yêu cầu chức năng quan trọng: nó thành use case, mô hình thiết kế và chức năng cài đặt như thế nào?",
     "<p>FR09: tạo một đơn hàng định danh duy nhất gắn khách, dòng hàng, địa chỉ, tổng tiền và lịch sử trạng thái. → Use case UC08 "
     "({fig:UCD2}), đặc tả có luồng A7 (gửi lại form). → Phân tích: {fig:AD01}, {fig:SD01}, Order ◆ OrderItem ◆ StatusChange trong {fig:CL01}. "
     "→ Thiết kế: {fig:SD05}, {code:model/order.py:Order.create_from_cart}. → Dữ liệu: <code>Orders.idempotency_key UNIQUE</code>. "
     "→ Code: {code:service/checkout_service.py:CheckoutService.place_order}. → Test: {test:test_repeated_submission_returns_the_same_order}.</p>"),
    (G2, "Xác định và đặc tả yêu cầu phi chức năng ra sao? Hiệu năng, bảo mật, khả dụng, tin cậy ảnh hưởng kiến trúc thế nào?",
     "<p>Mỗi NFR được viết đo được và gắn với bằng chứng thành công (ví dụ NFR01: trang danh mục dưới 2 giây). <b>Bảo mật</b> (NFR05, NFR10): "
     "kiểm quyền trong service ({code:service/auth_service.py:AuthService.require}), mật khẩu PBKDF2, không lưu số thẻ. <b>Tin cậy</b> "
     "(NFR07): transaction và khoá duy nhất. <b>Khả dụng/dễ dùng</b>: trang luôn chạy được khi AI thiếu dữ liệu (AI-N3), thông báo lỗi rõ. "
     "<b>Hiệu năng</b>: chỉ mục vector giữ trong bộ nhớ, chỉ dựng lại khi danh mục đổi. Thẳng thắn: NFR01–03 chưa được đo vì bản mẫu chạy "
     "một tiến trình trên SQLite.</p>"),
    (G2, "Khách đưa yêu cầu mới sau khi thiết kế xong: phân tích ảnh hưởng thế nào?",
     "<p>Lần theo ma trận truy vết. Ví dụ yêu cầu \"thanh toán khi nhận hàng (COD)\": yêu cầu → thêm FR, sửa giả định; use case → UC09 thêm "
     "luồng; sơ đồ → {fig:ST01} thêm trạng thái giữa Shipped và Paid, {fig:AD02} thêm hành động thu tiền; package/class → "
     "PaymentService và Order.TRANSITIONS; database → giá trị mới của <code>payment.status</code>; code và test → test mới cho luồng COD. "
     "Kiến trúc ba lớp giới hạn ảnh hưởng: controller và view hầu như không đổi. Sau khi sửa mô hình, chạy lại "
     "{file:tools/vp/v5_design_build.py} (generateCode) và {file:design/check_code.py} để biết code còn khớp thiết kế không.</p>"),
    (G3, "Mô tả quy trình mua hàng: actor, hoạt động, thông tin trao đổi.",
     "<p>{fig:BP01}: khách tìm và chọn hàng, cho vào giỏ, checkout (gửi <i>đơn hàng</i>). Hệ thống kiểm giỏ, giữ hàng, tạo đơn Payment "
     "Pending, gửi <i>yêu cầu thanh toán có mã tham chiếu</i> tới Payment Provider; nhận <i>kết quả có chữ ký</i>; nếu xác thực thì đơn "
     "Paid/Confirmed, nếu không thì trả hàng giữ. Sales Staff xử lý đơn, Warehouse Staff lấy hàng, đóng gói, giao <i>kiện hàng</i> cho "
     "Shipping Provider; hãng gửi <i>các mốc giao hàng</i>; khách nhận hàng và có thể đánh giá. Chi tiết trong làn: {fig:AD01}, {fig:AD02}.</p>"),
    (G3, "Trình bày sơ đồ ngữ cảnh và DFD mức 1. Tiến trình, kho dữ liệu, thực thể ngoài được biểu diễn thế nào?",
     "<p>{fig:CTX01}: một tiến trình là toàn bộ hệ thống, 8 thực thể ngoài (khách, admin, nhân viên bán hàng, kho, quản lý, hai đối tác, "
     "nhà cung cấp) với các luồng dữ liệu vào/ra. {fig:DFD0}: 8 tiến trình (1.0 Quản lý danh mục … 8.0 Báo cáo) và 7 kho dữ liệu D1–D8. "
     "{fig:DFD1} phân rã tiến trình 4.0 Đặt hàng và thanh toán thành 4.1–4.5 và cân bằng với mức trên (cùng luồng ra vào). Ký hiệu Gane–Sarson: "
     "tiến trình hình chữ nhật bo góc có số, kho dữ liệu hở một đầu có mã D, thực thể ngoài hình chữ nhật. Mỗi luồng phải đi qua một tiến trình.</p>"),
    (G3, "As-Is và To-Be khác nhau thế nào? Hệ thống cải tiến quy trình hiện tại ra sao?",
     "<p>As-Is: dữ liệu sản phẩm và tồn kho do nhiều người giữ, kết quả thanh toán và trạng thái giao hàng nhập tay, báo cáo làm bằng tay "
     "(các vấn đề BP01–BP06 trong {fig:PT01}). To-Be ({fig:BP01}): một nguồn dữ liệu sản phẩm; tồn kho cập nhật bằng sự kiện ngay khi giữ, "
     "trả, xuất hàng; kết quả thanh toán và mốc giao hàng đi vào hệ thống qua thông điệp có mã tham chiếu; trạng thái đơn theo máy trạng "
     "thái; báo cáo tính từ bản ghi. Mỗi cải tiến gắn một nguyên nhân gốc và một mục tiêu đo được (Chương 1, mục tiêu hệ thống).</p>"),
    (G3, "Trình bày sơ đồ use case: actor, use case chính, quan hệ.",
     "<p>{fig:UC00} cho cái nhìn tổng quát, bốn sơ đồ chi tiết {fig:UCD1}–{fig:UCD4} chứa đủ 32 use case. 10 actor; Customer kế thừa Visitor; "
     "Staff trừu tượng giữ use case Login chung. <b>Include</b>: UC08 luôn gồm UC29 kiểm giỏ, UC30 kiểm hàng còn, UC31 tính tổng, UC09 thanh toán. "
     "<b>Extend</b>: UC32 áp khuyến mãi mở rộng UC08 chỉ khi khách nhập mã; UC12 huỷ đơn, UC13 đánh giá mở rộng UC10; UC24 bổ sung hàng mở rộng UC20 "
     "khi tồn kho chạm ngưỡng. Use case AI ở {fig:UC_AI}.</p>"),
    (G3, "Use case \"Place Order\": tiền điều kiện, luồng chính, luồng thay thế, hậu điều kiện. Chuyển thành các class và method?",
     "<p>Tiền điều kiện: khách đã đăng nhập, giỏ có ít nhất một sản phẩm đang bán. Luồng chính: chọn checkout → kiểm giỏ và giá (UC29), kiểm hàng "
     "(UC30) → xác nhận địa chỉ, nhập mã → tính tổng (UC31, UC32) → xác nhận → giữ hàng và tạo đơn Payment Pending → yêu cầu thanh toán (UC09) → "
     "Paid/Confirmed, xoá giỏ. Thay thế: A1 hết hàng, A2 giá đổi, A3 thiếu địa chỉ, A5 thanh toán bị từ chối, A7 gửi lại form; E1 lỗi lưu → không có gì "
     "được lưu. Hậu điều kiện: một đơn có dòng hàng, tổng, lịch sử, mã thanh toán, hàng đã giữ. Thành class: {code:controller/order_controller.py:OrderController.checkout} "
     "→ {code:service/checkout_service.py:CheckoutService.place_order} → Order, CartService, InventoryService, PaymentService, OrderDAO ({fig:SD05}).</p>"),
    (G4, "Từ yêu cầu, hệ thống được phân rã thành phân hệ, package, class, method thế nào? Tiêu chí?",
     "<p>Bước 1 theo nghiệp vụ: 32 use case nhóm thành 4 phân hệ (tài khoản–danh mục, giỏ–đơn–thanh toán, quản trị, vận hành–báo cáo) cộng AI. "
     "Bước 2 theo trách nhiệm kỹ thuật: 6 package view, controller, service, ai, dao, model ({fig:PKG01}). Bước 3: trong service mỗi lĩnh vực một class "
     "(CartService, CheckoutService…); trong model package con theo vòng đời dữ liệu (cart, order, payment…). Bước 4: method từ bước của đặc tả use case. "
     "Tiêu chí: gắn kết cao (một package một trách nhiệm), phụ thuộc thấp và một chiều, mỗi class truy được về use case.</p>"),
    (G4, "Trình bày cấu trúc package và trách nhiệm của từng package.",
     "<p>{fig:PKG01}: <b>view</b> chỉ tạo HTML ({file:abc_shop/view/templates.py}); <b>controller</b> nhận request, kiểm phiên, gọi service, trả response; "
     "<b>service</b> quy tắc nghiệp vụ và transaction (Customer → AuthService, Product → CatalogService, Order → CheckoutService/OrderService, Payment → PaymentService); "
     "<b>ai</b> tìm kiếm, tóm tắt đánh giá, gợi ý; <b>dao</b> giao diện DAO và cài đặt SQLite, Database (kết nối, transaction); <b>model</b> lớp miền "
     "theo package con customer, product, order, payment… Package \"Database\" của đề tương ứng với dao.Database và schema.sql.</p>"),
    (G4, "Phân rã theo chức năng nghiệp vụ và theo lớp kỹ thuật khác nhau thế nào? Dự án dùng cách nào?",
     "<p>Theo chức năng: mỗi package là một nghiệp vụ (order, product…) chứa cả giao diện, logic và lưu trữ của nó. Theo lớp: mỗi package là một tầng "
     "(controller, service, dao). Dự án dùng <b>kết hợp</b>: tầng là cấp ngoài cùng (dễ kiểm quy tắc phụ thuộc, phù hợp MVC của môn học), còn bên "
     "trong mỗi tầng chia theo nghiệp vụ (OrderController, OrderService, OrderDAO; model.order). Lý do: ứng dụng nhỏ, một nhóm phát triển; khi lớn có thể "
     "tách thành dịch vụ theo đúng các đường chia nghiệp vụ này.</p>"),
    (G4, "Gắn kết cao và phụ thuộc thấp là gì? Áp dụng ra sao trong package?",
     "<p>Gắn kết cao: các phần tử trong một module cùng phục vụ một trách nhiệm. Phụ thuộc thấp: module biết càng ít về module khác càng tốt. Áp dụng: "
     "service chỉ phụ thuộc <i>giao diện</i> DAO, không phụ thuộc SQLite ({test:test_services_never_import_a_storage_implementation}); phụ thuộc chỉ đi "
     "xuống ({test:test_dependencies_only_point_downwards}); model không phụ thuộc gì; AI không import service. Ví dụ VectorIndex nhận hàm encode được "
     "truyền vào thay vì import ImageService để dao không phụ thuộc ai. Gắn kết: mọi quy tắc của checkout ở CheckoutService.</p>"),
    (G4, "Order Management cần truy cập Product Management: thiết kế phụ thuộc thế nào? Vấn đề của phụ thuộc vòng?",
     "<p>Order phụ thuộc Product theo một chiều qua giao diện: CheckoutService/CartService dùng <code>ProductDAO</code> và <code>InventoryService</code>, "
     "dòng đơn giữ <code>product_id</code> và giá đã chụp lại chứ không giữ đối tượng Product. Product không biết gì về Order. Phụ thuộc vòng làm không "
     "thể biên dịch/test riêng từng phần, sửa một bên kéo bên kia, khó tách dịch vụ, và trong Python dễ gây lỗi import vòng. Nếu Product cần biết về "
     "đơn (ví dụ \"bán chạy\"), dùng báo cáo đọc dữ liệu hoặc sự kiện, không gọi ngược.</p>"),
    (G5, "Trình bày kiến trúc: trách nhiệm của lớp trình bày, nghiệp vụ, truy cập dữ liệu.",
     "<p>{fig:CMP02} và {fig:PKG01}. <b>Trình bày</b>: view + controller (WebApp định tuyến, kiểm phiên; templates tạo HTML). <b>Nghiệp vụ</b>: service "
     "(quy tắc use case, quyền, transaction) và ai, cùng model (quy tắc của chính đối tượng: chuyển trạng thái, tồn kho không âm). <b>Truy cập dữ liệu</b>: "
     "DAO đổi bản ghi ↔ đối tượng, Database quản lý kết nối và transaction. Bên ngoài: SQLite, PaymentGateway, ShippingGateway ({fig:DEP01}).</p>"),
    (G5, "Xác định class thuộc lớp nào ra sao? Lấy class cụ thể và giải thích.",
     "<p>Câu hỏi: class đó biết về HTTP, về quy tắc nghiệp vụ hay về SQL? {code:controller/order_controller.py:OrderController} đọc tham số request và "
     "redirect → trình bày. {code:service/checkout_service.py:CheckoutService} quyết định khi nào giữ hàng, khi nào yêu cầu thanh toán → nghiệp vụ. "
     "{code:dao/sqlite_dao.py:SqliteOrderDAO} chỉ viết SQL và ánh xạ dòng → Order → truy cập dữ liệu. {code:model/order.py:Order} giữ quy tắc chuyển trạng "
     "thái của chính nó → model dùng chung.</p>"),
    (G5, "Luồng xử lý đầy đủ khi khách đặt hàng: từ giao diện qua Controller, nghiệp vụ, DAO, database và trở lại.",
     "<p>Form checkout POST /checkout → {code:controller/router.py:WebApp.dispatch} nạp người dùng của phiên → "
     "{code:controller/order_controller.py:OrderController.checkout} → {code:service/checkout_service.py:CheckoutService.place_order}: tra idempotency key "
     "(OrderDAO), quote (CartService.validate_cart, khuyến mãi, phí ship), mở {code:dao/database.py:Database.transaction}, Order.create_from_cart, "
     "{code:dao/sqlite_dao.py:SqliteOrderDAO.save_order} (INSERT Orders, OrderItem, StatusChange), InventoryService.reserve_order (InventoryEvent, "
     "StockLevel), commit; PaymentService.request_payment → đơn Paid/Confirmed, xoá giỏ. Controller redirect tới /orders/O0xx, view hiển thị trạng thái ({fig:SD05}).</p>"),
    (G5, "Vì sao Controller không được chạy SQL hay giữ kết nối CSDL?",
     "<p>Controller sẽ trộn ba trách nhiệm: HTTP, quy tắc nghiệp vụ và lưu trữ. Hậu quả: quy tắc checkout lặp lại ở mọi nơi tạo đơn (web, API, script); "
     "không test được quy tắc mà không dựng HTTP; không gom được nhiều thao tác vào một transaction đúng ranh giới use case; đổi CSDL phải sửa mọi "
     "controller; dễ quên kiểm quyền và dễ lỗi SQL injection. Trong dự án, test kiến trúc chặn controller import dao ({test:test_dependencies_only_point_downwards}).</p>"),
    (G5, "Đổi sang hệ quản trị CSDL khác: kiến trúc ba lớp giảm ảnh hưởng ra sao? Sửa class nào?",
     "<p>Chỉ lớp truy cập dữ liệu đổi: viết cài đặt mới của các giao diện trong {file:abc_shop/dao/interfaces.py} (ví dụ PostgresOrderDAO), sửa "
     "{code:dao/database.py:Database} (kết nối, transaction), chuyển schema (script DDL sinh lại từ mô hình vật lý với kiểu của CSDL mới), và sửa composition "
     "root {file:abc_shop/shop.py} để tạo DAO mới. Service, model, controller, view không đổi vì chỉ dùng giao diện DAO. Test giữ nguyên làm lưới an toàn.</p>"),
    (G6, "Trách nhiệm của Controller, Service, DAO, Model; mỗi loại một ví dụ.",
     "<p>Controller: {code:controller/order_controller.py:OrderController.add_to_cart} (đọc product_id, qty, gọi service, redirect). Service: "
     "{code:service/cart_service.py:CartService.add_item} (sản phẩm còn bán, kiểm hàng còn UC30, cập nhật giỏ). DAO: {code:dao/sqlite_dao.py:SqliteCartDAO.update_cart} "
     "(ghi CartItem). Model: {code:model/cart.py:Cart.add_item} (cộng vào dòng có sẵn hoặc tạo dòng mới với giá hiện tại). Cả bốn trên sơ đồ tầng {fig:LAY02}.</p>"),
    (G6, "Chọn một method của Controller: tham số, kiểm tra, gọi nghiệp vụ, phản hồi. Nó gọi class/method nào tiếp?",
     "<p>{code:controller/order_controller.py:OrderController.checkout}: đầu vào là request với promo, card, key (idempotency key của form). Kiểm tra: "
     "<code>_customer()</code> gọi AuthService.require(user, 'cart') – chưa đăng nhập thì chuyển tới /login. Gọi tiếp "
     "{code:service/checkout_service.py:CheckoutService.place_order}. Phản hồi: lỗi CheckoutError → quay lại giỏ với danh sách vấn đề; thành công → "
     "redirect tới trang đơn với thông báo trạng thái. Controller không tự tính tổng hay giữ hàng.</p>"),
    (G6, "Quan hệ Service–DAO: quy tắc nào ở Service, thao tác nào ở DAO? Ví dụ.",
     "<p>Service giữ quy tắc và thứ tự: \"chỉ tạo đơn khi giỏ hợp lệ\", \"giữ hàng và tạo đơn trong một transaction\", \"chỉ xoá giỏ khi đã thanh toán\" "
     "({code:service/checkout_service.py:CheckoutService.place_order}). DAO chỉ đọc/ghi: {code:dao/sqlite_dao.py:SqliteOrderDAO.find_by_idempotency_key}, "
     "save_order. DAO trả None khi không thấy, không quyết định điều đó nghĩa là gì; service quyết định. Service phụ thuộc giao diện OrderDAO, nên test có "
     "thể dùng CSDL trong bộ nhớ.</p>"),
    (G6, "Chọn một method DAO: nó chạy truy vấn và ánh xạ bản ghi thành Model ra sao?",
     "<p>{code:dao/sqlite_dao.py:SqliteOrderDAO.get_order}: <code>SELECT * FROM Orders WHERE order_id = ?</code> (tham số hoá, chống SQL injection), "
     "rồi {code:dao/sqlite_dao.py:SqliteOrderDAO._to_order} đọc thêm <code>OrderItem</code> và <code>StatusChange</code> theo order_id và dựng "
     "đối tượng Order có danh sách OrderItem và StatusChange. Ghi: {code:dao/sqlite_dao.py:SqliteOrderDAO.save_order} INSERT … ON CONFLICT cập nhật trạng thái, "
     "lịch sử chỉ được nối thêm, không ghi đè.</p>"),
    (G6, "Vai trò của Model. Lần theo một Order từ lúc tạo, điền dữ liệu, truyền qua các class tới khi lưu.",
     "<p>Model là đối tượng miền mang dữ liệu và quy tắc của chính nó. Order được tạo bởi {code:model/order.py:Order.create_from_cart} (dòng giỏ → dòng đơn với "
     "giá chính thức, trạng thái Payment Pending, mục lịch sử đầu tiên), truyền cho OrderDAO.save_order (thành 3 loại bản ghi), cho InventoryService.reserve_order "
     "(đọc dòng hàng), PaymentService đổi trạng thái qua {code:model/order.py:Order.change_status}. Phân biệt: đối tượng Order trong bộ nhớ có danh sách lồng; "
     "trong CSDL nó là 1 dòng Orders + n dòng OrderItem + m dòng StatusChange; bảng là cấu trúc, bản ghi là dữ liệu.</p>"),
    (G7, "Trình bày ERD: thực thể, thuộc tính, khoá, quan hệ; chuyển thành bảng thế nào?",
     "<p>ERD không vẽ tay: class phân tích được bổ sung kiểu, định danh và «ORM Persistable» thành {fig:DM01}, rồi tool "
     "syncClassesToErd của plugin MCP sinh {fig:ERD01} (22 bảng, 24 khoá ngoại). Ví dụ Orders (PK order_id, FK customer_id → Customer, "
     "FK promo_code → Promotion được rỗng) 1–n OrderItem (PK ghép order_id, product_id). Quy tắc chuyển mà bộ sinh áp dụng: mỗi lớp "
     "một bảng; quan hệ 1–n thành khoá ngoại ở phía n; hợp thành thì khoá con chứa khoá cha; kế thừa thành bảng con dùng chung khoá "
     "(Customer dùng user_id của User; Footwear, Apparel, Bag, Watch dùng product_id của Product). Những chỗ bộ sinh không tự quyết "
     "(lớp không có định danh) được quyết bằng tool setPrimaryKey, renameColumn và ghi ở {file:design/v5_tool_log.txt}. "
     "Script SQL sinh bằng generateSql: {file:design/create_tables.sql}.</p>"),
    (G7, "Chọn một bảng: khoá ứng viên, khoá chính, phụ thuộc hàm, ràng buộc toàn vẹn.",
     "<p>Bảng <code>payment</code>: khoá ứng viên payment_id và attempt_ref (mỗi lần thử có mã duy nhất); khoá chính payment_id; attempt_ref UNIQUE. "
     "Phụ thuộc hàm: payment_id → order_id, attempt_ref, amount, currency, status, provider_ref, created_at; attempt_ref → payment_id. Ràng buộc: FK order_id → "
     "Orders, CHECK amount &gt; 0, NOT NULL các cột bắt buộc. Không có phụ thuộc bắc cầu qua cột không khoá, nên ở 3NF (thực ra BCNF vì mọi định "
     "thuộc đều là khoá ứng viên).</p>"),
    (G7, "Chuẩn hoá từng bước một bảng đơn hàng thiết kế kém lên 1NF, 2NF, 3NF.",
     "<p>Bảng kém: Order(order_id, customer_id, customer_name, customer_email, products=\"P01x2, P09x1\", product_names, unit_prices, total). "
     "<b>1NF</b>: bỏ nhóm lặp → OrderLine(order_id, product_id, product_name, unit_price, quantity), Order(order_id, customer_id, customer_name, customer_email, total). "
     "<b>2NF</b>: trong OrderLine khoá (order_id, product_id); product_name phụ thuộc chỉ product_id → đưa sang Product(product_id, name, price); giữ "
     "unit_price trên dòng vì là giá tại thời điểm mua. <b>3NF</b>: trong Order, customer_name, email phụ thuộc customer_id (bắc cầu) → bảng User. "
     "Kết quả đúng là Orders, OrderItem, product, User của dự án; OrderItem.name/unit_price là giá trị lịch sử có chủ ý.</p>"),
    (G7, "Vì sao Order và OrderDetail nên là hai bảng? Bất thường khi chèn, sửa, xoá nếu gộp?",
     "<p>Một đơn có nhiều dòng. Gộp lại thì thông tin đơn (địa chỉ, tổng, trạng thái) lặp ở mỗi dòng. <b>Chèn</b>: không tạo được đơn khi chưa có dòng, hoặc phải "
     "lặp địa chỉ nhiều lần. <b>Sửa</b>: đổi trạng thái phải sửa mọi dòng; sửa thiếu một dòng là dữ liệu mâu thuẫn. <b>Xoá</b>: xoá dòng cuối cùng làm mất luôn "
     "thông tin đơn. Tách thành Orders và OrderItem (FK order_id, PK ghép) loại bỏ cả ba; CHECK quantity &gt; 0 và khoá ghép ngăn một sản phẩm lặp trong một đơn.</p>"),
    (G7, "Chuẩn hoá ảnh hưởng thế nào tới Model, DAO, SQL? DAO lấy Order cùng OrderDetail từ nhiều bảng ra sao?",
     "<p>Bảng chuẩn hoá thì model có cấu trúc lồng (Order chứa list OrderItem, StatusChange), còn DAO phải ghép lại: {code:dao/sqlite_dao.py:SqliteOrderDAO._to_order} "
     "chạy 1 truy vấn lấy đơn rồi 2 truy vấn lấy dòng hàng và lịch sử theo order_id (có thể thay bằng JOIN). Khi ghi, save_order chèn vào 3 bảng trong một "
     "transaction. Tương tự ProductDAO: JOIN product với category để biết detail_kind, rồi đọc đúng một bảng của loại sản phẩm ({code:dao/sqlite_dao.py:SqliteProductDAO._to_product}).</p>"),
    (G8, "Trình bày sơ đồ class; chọn một class và đối chiếu thuộc tính, thao tác với code.",
     "<p>{fig:DCL01}: Cart có cart_id, items (hợp thành), customer_id (khoá); thao tác find, add_item(product, quantity), update_quantity, remove_item, "
     "calc_total, is_empty, clear. Code {code:model/cart.py:Cart}: cùng tên, cùng tham số. Không cần tin lời: {file:design/check_code_output.txt} so tự động 28 class "
     "của mô hình với code, Cart 3/3 trường, 7/7 phương thức. Khung code sinh từ mô hình nằm ở {file:design/generated/model/cart.py}.</p>"),
    (G8, "Use case chuyển thành các class và method cộng tác thế nào? Dùng \"Place Order\" từ yêu cầu tới class và sequence.",
     "<p>Bước 1: danh từ trong đặc tả UC08 → lớp phân tích (Cart, Order, OrderItem, StockLevel, Payment) trong {fig:CL01}. Bước 2: mỗi bước luồng → thông điệp giữa "
     "boundary/control/entity trong {fig:SD01}. Bước 3: control tách thành controller + service, entity thành model + DAO, đặt tên hàm thật → {fig:SD05}. "
     "Bước 4: thông điệp nào gửi tới một lớp thì lớp đó có phương thức tương ứng trong {fig:DCL01} (Order.create_from_cart, Cart.calc_total). "
     "Bước 5: code {code:service/checkout_service.py:CheckoutService.place_order} làm đúng thứ tự thông điệp của SD05.</p>"),
    (G8, "Association, Aggregation, Composition, Inheritance khác nhau? Ví dụ và cài đặt trong code.",
     "<p><b>Association</b>: hai lớp biết nhau, vòng đời độc lập – Review → Product, cài đặt bằng trường khoá product_id. <b>Aggregation</b>: toàn thể–bộ phận "
     "yếu, bộ phận sống độc lập – Customer ◇ Address, code là trường address: Optional[Address]. <b>Composition</b>: bộ phận không sống ngoài toàn thể – Order ◆ "
     "OrderItem, code là list items tạo bên trong Order; trong CSDL khoá con chứa khoá cha, xoá giỏ thì CASCADE xoá dòng giỏ. <b>Inheritance</b>: Customer kế "
     "thừa User (<code>class Customer(User)</code>), Bag kế thừa Product. Xem {fig:CL01}, {fig:DCL01}.</p>"),
    (G8, "Customer, ShoppingCart, Order, OrderDetail, Product, Payment: trách nhiệm, quan hệ; thêm giảm giá sản phẩm thì sửa class, method nào?",
     "<p>Customer đặt đơn (1–0..*), sở hữu Cart (1–0..1); Cart ◆ CartItem → Product; Order ◆ OrderItem → Product; Order 1–0..* Payment. Trách nhiệm: Cart và "
     "Order tự tính tổng từ dòng, dòng tự tính sub_total; Payment kiểm kết quả khớp ({code:model/payment.py:Payment.matches}). Giảm giá theo sản phẩm: thêm "
     "thuộc tính giảm giá hoặc lớp ProductDiscount liên kết Product; giá hiện hành tính ở Product (một phương thức current_price), CartService dùng giá đó khi "
     "add_item, CheckoutService.quote kiểm lại giá (UC29 đã báo \"giá đổi\"); OrderItem.unit_price vẫn chụp giá sau giảm. Khuyến mãi theo mã (Promotion.discount_for) giữ nguyên.</p>"),
    (G8, "Sequence diagram đặt hàng: thông điệp giữa Controller, Service, DAO, Model, CSDL; khớp với lời gọi trong code thế nào?",
     "<p>{fig:SD05}: 1 POST /checkout → 2 place_order → 3–4 find_by_idempotency_key (None) → 5–6 validate_cart → 7 apply_promotion, calc_shipping → 8 "
     "create_from_cart → 9 save_order → 10 reserve_order → 11 request_payment → 12–13 authorize/kết quả có chữ ký → 14 change_status(Paid/Confirmed) → 15 "
     "save_order → trả về controller, 18 redirect. Mỗi thông điệp là một dòng trong {code:service/checkout_service.py:CheckoutService.place_order} và các hàm nó gọi; "
     "ghi chú trong sơ đồ đánh dấu bước 8–10 trong một transaction.</p>"),
    (G9, "Đơn hàng có 5 sản phẩm: CSDL biểu diễn ra sao? Khoá chính, ngoại, ràng buộc bảo vệ nhất quán thế nào?",
     "<p>1 dòng Orders + 5 dòng OrderItem (PK (order_id, product_id), FK tới Orders và product) + dòng StatusChange + 5 sự kiện RESERVE "
     "trong InventoryEvent, 1 dòng payment. Bảo vệ: FK chặn dòng của sản phẩm hay đơn không tồn tại; PK ghép chặn một sản phẩm hai lần; CHECK quantity &gt; 0; "
     "UNIQUE idempotency_key chặn đơn trùng; StockLevel CHECK reserved ≤ physical chặn giữ quá hàng có; UNIQUE (product, kind, reference) chặn sự kiện ghi hai lần. "
     "build_db.py thử các vi phạm này: {file:design/build_db_output.txt}.</p>"),
    (G9, "Transaction tạo Order và nhiều OrderDetail: lỗi một thao tác thì sao? Commit và rollback.",
     "<p>Trong {code:service/checkout_service.py:CheckoutService.place_order}, tạo đơn, ghi dòng hàng, lịch sử và giữ hàng nằm trong "
     "<code>with self.db.transaction()</code> ({code:dao/database.py:Database.transaction}): BEGIN, các DAO lồng bên trong dùng chung transaction, hết khối thì "
     "COMMIT, có ngoại lệ thì ROLLBACK – không có đơn nửa vời hay hàng bị giữ mà không có đơn (luồng E1). Test {test:test_insufficient_stock_stops_checkout_without_side_effects} "
     "kiểm tra không còn bản ghi nào sau khi giữ hàng thất bại. Thanh toán gọi sau commit; từ chối thì service trả hàng và đặt Payment Failed.</p>"),
    (G9, "Unit, Integration, System, Acceptance testing khác nhau? Ví dụ với Controller, Service, DAO, CSDL.",
     "<p><b>Unit</b>: một class đơn lẻ – {test:test_order_follows_only_the_allowed_transitions} (Order). <b>Integration</b>: service + DAO + SQLite thật trong bộ nhớ – "
     "{test:test_successful_checkout_reserves_stock_pays_and_clears_cart}; DAO + database: {test:test_database_trigger_rejects_a_kind_row_of_the_wrong_kind}. "
     "<b>System</b>: toàn hệ thống qua HTTP – {test:test_customer_buys_through_the_web} (controller, view, service, DAO). <b>Acceptance</b>: theo tiêu chí nghiệm thu "
     "của use case, chạy bởi người dùng/khách hàng – kịch bản demo ở mục F và bảng tiêu chí nghiệm thu trong Chương 1.</p>"),
    (G9, "Thiết kế kịch bản test checkout: hàng còn, tạo đơn, thanh toán lỗi, xác nhận. Kết quả mong đợi?",
     "<p>(1) Hàng còn: giỏ P12 x1 → đơn Paid/Confirmed, reserved của P12 tăng 1, giỏ rỗng, có payment Succeeded ({test:test_successful_checkout_reserves_stock_pays_and_clears_cart}). "
     "(2) Hết hàng: số lượng vượt khả dụng → CheckoutError, không có đơn, tồn kho không đổi ({test:test_insufficient_stock_stops_checkout_without_side_effects}). "
     "(3) Thẻ bị từ chối → đơn Payment Failed, hàng được trả, giỏ còn nguyên ({test:test_declined_payment_releases_reservation_and_keeps_cart}). (4) Hết thời gian chờ → đơn "
     "Payment Pending, hàng vẫn giữ ({test:test_timeout_keeps_order_pending_and_reserved}). (5) Gửi lại form → cùng một đơn. (6) Xác nhận: lịch sử có mục Paid/Confirmed, trang đơn hiển thị trạng thái.</p>"),
    (G9, "Đánh giá hệ thống theo dễ dùng, tin cậy, bảo trì, hiệu năng, bảo mật; hạn chế và cải tiến.",
     "<p>Dễ dùng: tìm bằng câu tự nhiên, thông số theo nhóm, thông báo lỗi cụ thể; hạn chế: chưa có trang quản lý danh mục/khách hàng. Tin cậy: transaction, "
     "idempotency, ràng buộc CSDL; hạn chế: SQLite một tiến trình. Bảo trì: ba lớp, 45 test, mô hình ↔ code kiểm tự động. Hiệu năng: chưa đo NFR01–03. Bảo mật: "
     "PBKDF2, kiểm quyền ở service, cookie HttpOnly; hạn chế: chưa có HTTPS, CSRF token. Cải tiến: PostgreSQL, đo tải, cổng thanh toán thật có đối soát, "
     "mô hình AI thật (Whisper, CLIP) sau cùng giao diện.</p>"),
    (G10, "Demo một chức năng quan trọng và lần theo từ giao diện tới Controller, Service, DAO, Model, CSDL.",
     "<p>Thêm P16 vào giỏ: nút \"Add to cart\" POST /cart/add → {code:controller/order_controller.py:OrderController.add_to_cart} → "
     "{code:service/cart_service.py:CartService.add_item} (ProductDAO.get_product, InventoryDAO.get_stock kiểm UC30) → {code:model/cart.py:Cart.add_item} → "
     "{code:dao/sqlite_dao.py:SqliteCartDAO.update_cart} (INSERT CartItem) → redirect /cart. Mở song song {fig:LAY02} để chỉ từng hộp trên sơ đồ.</p>"),
    (G10, "Yêu cầu mới: tính năng gợi ý sản phẩm. Phân rã thành package, class, method, thao tác CSDL? Lớp nào bị ảnh hưởng?",
     "<p>Dự án đã có: package <b>ai</b> với {code:ai/recommender.py:RecommenderService} (fit đọc đơn hàng qua OrderDAO, similar(product_id, k), for_customer(customer_id, k)); "
     "dữ liệu đọc từ product, bảng của loại sản phẩm, OrderItem, StockLevel; không bảng mới (mô hình tính lại khi có đơn). Trình bày: ShopController.product truyền danh sách "
     "gợi ý cho view, OrderController.history cho trang đơn. Lớp bị ảnh hưởng: ai (mới), controller và view (thêm khối hiển thị); dao và model không đổi. Test "
     "{test:test_recommender_never_suggests_out_of_stock_or_bought_items}.</p>"),
    (G10, "OrderController truy cập CSDL trực tiếp và chứa quy tắc nghiệp vụ: vấn đề và cách refactor.",
     "<p>Vấn đề: controller gắn chặt với SQL (đổi CSDL là sửa controller), quy tắc checkout không dùng lại và không test được ngoài HTTP, transaction không đúng "
     "ranh giới use case, gắn kết thấp (một class làm 3 việc), phụ thuộc cao. Refactor: (1) chuyển SQL vào OrderDAO/CartDAO sau giao diện; (2) chuyển quy tắc vào "
     "CheckoutService với transaction; (3) controller chỉ đọc request, gọi service, chọn response; (4) tạo đối tượng ở composition root {file:abc_shop/shop.py}; "
     "(5) thêm test kiến trúc để không tái phạm. Đó chính là cấu trúc hiện tại ({fig:PKG01}, {fig:LAY02}).</p>"),
    (G10, "Đánh giá phản biện: ba quyết định thiết kế mạnh và ba hạn chế; cải tiến package, UML, CSDL, kiến trúc.",
     "<p>Mạnh: (1) tồn kho là chuỗi sự kiện và trạng thái đơn theo bảng chuyển – mọi con số giải thích được; (2) idempotency/mã tham chiếu ở mọi trao đổi với đối tác; "
     "(3) mô hình VP sinh ra SQL và khung code, được đối chiếu tự động với ứng dụng. Hạn chế: (1) thanh toán, vận chuyển, giọng nói được mô phỏng; (2) SQLite một "
     "tiến trình, chưa đo hiệu năng; (3) hai UNIQUE ghép và trigger chưa có trong ERD, menu Generate Database của VP chưa cấu hình. Cải tiến: tách package theo "
     "nghiệp vụ khi hệ lớn lên, thêm sequence thiết kế cho thanh toán callback, chuyển PostgreSQL với chỉ mục, thêm hàng đợi sự kiện cho thông báo.</p>"),
    (G10, "Bảo vệ trọn vẹn một use case quan trọng: từ nghiệp vụ tới use case, phân rã, package, class, method, bảng, chuẩn hoá và toàn vẹn.",
     "<p>Chọn UC08 Đặt hàng. Nghiệp vụ: vấn đề BP02 bán vượt tồn kho và BP03 thanh toán không xác thực ({fig:PT01}) → FR08–FR10, NFR07. Use case: UC08 include "
     "UC29–31, UC09; extend UC32 ({fig:UCD2}). Phân rã: phân hệ giỏ–đơn–thanh toán → package controller/service/dao/model ({fig:PKG01}). Class: {fig:DCL01}; "
     "method: {code:service/checkout_service.py:CheckoutService.place_order}, {code:model/order.py:Order.create_from_cart}, {code:model/order.py:Order.change_status}. "
     "Model ↔ bảng: Order ↔ Orders + OrderItem + StatusChange (3NF, giá dòng là giá trị lịch sử). Toàn vẹn: transaction, UNIQUE idempotency_key, "
     "CHECK tồn kho. Vì sao thiết kế này: một điểm giữ quy tắc, transaction đúng ranh giới; cải tiến: sequence cho callback, đối soát đơn Payment Pending.</p>"),
]
assert len(ANSWERS) == 50, len(ANSWERS)
