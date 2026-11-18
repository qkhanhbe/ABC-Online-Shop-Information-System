# ABC Online Shop: from requirements to running code

Final essay (version 5) of **Information System Analysis and Design** (PTIT 2026, lecturer PGS.TS. Trần Đình Quế):
one e-commerce information system followed through requirements, analysis, AI integration, data model, design,
implementation and demonstration. Student: Bế Quốc Khánh (KHANHBQ), B23DCCE049.

Open **[showcase/index.html](showcase/index.html)** for the guided defence tour (Vietnamese): diagrams, model evolution,
traceability to code, database, AI, demo script and answers to the 50 oral-examination questions.

## Where everything is

| Deliverable | Location |
|---|---|
| Essay (official report) | [Tieuluan_V5_04_10_KhanhBQ_049.pdf](Tieuluan_V5_04_10_KhanhBQ_049.pdf): 1 Introduction and requirements, 2 Analysis, 3 AI, 4 Data model, 5 Design, 6 Implementation |
| Diagrams | [TieuLuan_KHANHBQ.vpp](TieuLuan_KHANHBQ.vpp), 47 diagrams in Visual Paradigm in five sub-projects (models), one per phase: 1 Requirements, 2 Analysis, 3 AI Search, 4 Data Model, 5 Design; PNG export (Community Edition) in [diagrams/](diagrams) |
| Analysis classes | CL01, one diagram: attribute names only; Footwear, Apparel, Bag and Watch are subclasses of Product |
| Data model | DM01 = CL01 + identifiers, types, `<<ORM Persistable>>`; ERD01 generated from it by `syncClassesToErd`; tool calls in [design/v5_tool_log.txt](design/v5_tool_log.txt) |
| SQL | [design/create_tables.sql](design/create_tables.sql), generated from ERD01 by `generateSql` (SQLite); application schema [abc_shop/dao/schema.sql](abc_shop/dao/schema.sql) |
| Database check | [design/build_db.py](design/build_db.py), output [design/build_db_output.txt](design/build_db_output.txt) |
| Design and generated code | DCL01-DCL05 (one per package; DCL01 = DM01 + methods), PKG01, LAY01-LAY05, SD05-SD09; [design/generated/](design/generated) written by `generateCode`, checked by [design/check_code.py](design/check_code.py) |
| Source code | [abc_shop/](abc_shop) (Python, SQLite; model, dao, service, ai, controller, view) |
| Test and demo evidence | [demo_results/](demo_results): pytest, demo and AI evaluation output, web screenshots |
| Defence showcase and Q&A | [showcase/index.html](showcase/index.html) (built by [showcase/build.py](showcase/build.py) from [showcase/content.py](showcase/content.py)) |
| Tools | [tools/vp/](tools/vp): scripts that drew the diagrams through the Visual Paradigm MCP plugin (v5_*.py); [tools/vpgen/](tools/vpgen): headless plugin (tidy, five phase models, polish, export); [tools/report/](tools/report): builds the PDF |

## Run the shop

```powershell
cd abc_shop
python -m pip install -r requirements.txt
python main.py serve          # http://localhost:8000 (seeds abc_shop/data/abc_shop.db on first run)
python -m pytest -q           # 45 tests
python main.py demo           # end-to-end scenario in the terminal
python evaluate.py            # AI evaluation
```

Demo accounts: `khanh@example.com / khanh2026` (customer), `sales@abc.vn / sales2026`, `warehouse@abc.vn / stock2026`,
`admin@abc.vn / admin2026`, `manager@abc.vn / report2026`. Delete `abc_shop/data/abc_shop.db` to start from fresh data.

## From the models to the database and the code

The chain runs through the tools of the Visual Paradigm MCP plugin 1.33 (github.com/thanhtrnnn/vp-mcp) with Visual
Paradigm Enterprise open on `TieuLuan_KHANHBQ.vpp`:

```powershell
python tools/vp/v5_build.py analysis        # analysis classes (attribute names only)
python tools/vp/v5_build.py datamodel       # data model classes with identifiers, types, <<ORM Persistable>>
python tools/vp/v5_design_build.py classes  # design classes per package, from the code of abc_shop
python tools/vp/v5_merge.py                 # one class diagram per phase: CL01, DM01, DCL01 (wide grid)
python tools/vp/v5_erd.py                   # syncClassesToErd DM01 -> ERD01, key decisions, generateSql
python tools/vp/v5_design_more.py sequences # SD07-SD09; then essay.gen mode v5org (tools/vpgen) relinks the
                                            # lifelines and files the diagrams under the five phase models
python tools/vp/v5_lay.py                   # LAY01, LAY02; v5_design_more.py layers: LAY03-LAY05
python tools/vp/v5_design_build.py code     # generateCode, one package per folder in design/generated
python tools/vp/v5_geometry.py              # geometry for the red callouts of the report
python design/build_db.py                   # run the generated SQL, compare with schema.sql, seed, check rules
python design/check_code.py                 # compare the generated classes with abc_shop
python tools/report/build_report.py         # the PDF
python showcase/build.py                    # the showcase
```

`generateSql` uses Visual Paradigm's own generator when the project has a database configuration
(Tools > DB > Database Configuration); this project has none, so the plugin wrote the SQL with its SQLite generator
and says so in the first line of the script. To show Visual Paradigm's menu live: open ERD01, configure SQLite in
Tools > DB > Database Configuration, then Tools > DB > Generate Database with "Export to DDL".

## Limits

Payment and carrier are simulated behind fixed interfaces; voice search records in the browser and is recognised
offline by Whisper tiny.en (English, downloaded once into abc_shop/data/stt_model); the shop runs as one process on
SQLite and the performance requirements were not measured; category and customer management have services and tests
but no pages; the product pictures are drawings. NOT NULL, CHECK, UNIQUE, DEFAULT, the BR-CAT-01 triggers and the
technical tables are added by hand in `schema.sql`, because an ERD does not carry them.

Repository: https://github.com/qkhanhbe/ABC-Online-Shop-Information-System
