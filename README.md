# ABC Online Shop: from requirements to running code

Final essay (version 4) of **Information System Analysis and Design** (PTIT 2026, lecturer PGS.TS. Trần Đình Quế):
one e-commerce information system followed through requirements, analysis, AI integration, design, implementation and
demonstration. Student: Bế Quốc Khánh (KHANHBQ), B23DCCE049.

Open **[showcase/index.html](showcase/index.html)** for the guided defence tour (Vietnamese): diagrams, model evolution,
traceability to code, database, AI, demo script and answers to the 50 oral-examination questions.

## Where everything is

| Deliverable | Location |
|---|---|
| Essay (official report) | [Tieuluan_V4_04_10_KhanhBQ_049.pdf](Tieuluan_V4_04_10_KhanhBQ_049.pdf), 6 chapters |
| Requirement specification | Essay chapters 1-2 (needs, 24 FR, 12 NFR, 32 use cases, specifications, business rules, acceptance criteria) |
| Diagrams per phase | [TieuLuan_KHANHBQ.vpp](TieuLuan_KHANHBQ.vpp), 35 diagrams drawn in Visual Paradigm; PNG export (Community Edition) in [diagrams/](diagrams) |
| Data models and schema | CDM01, LDM01, ERD01-02 in the project; [design/create_tables.sql](design/create_tables.sql) generated from ERD01-02; application schema [abc_shop/dao/schema.sql](abc_shop/dao/schema.sql) |
| Database check | [design/build_db.py](design/build_db.py) and its output [design/build_db_output.txt](design/build_db_output.txt) |
| Code generated from the design | [design/generate_code.py](design/generate_code.py), [design/generated/](design/generated), checked by [design/check_code.py](design/check_code.py) |
| Source code | [abc_shop/](abc_shop) (Python, SQLite; model, dao, service, ai, controller, view) |
| Demo data | [abc_shop/data/seed.json](abc_shop/data/seed.json), played through the real services by [abc_shop/seed.py](abc_shop/seed.py) |
| Test and demo evidence | [demo_results/](demo_results): pytest, demo and AI evaluation output, web screenshots |
| Defence showcase and Q&A | [showcase/index.html](showcase/index.html) (built by [showcase/build.py](showcase/build.py) from [showcase/content.py](showcase/content.py)) |
| Diagram tools | [tools/vp/](tools/vp): drawing scripts for the Visual Paradigm MCP plugin; [tools/screens.py](tools/screens.py) takes the screenshots |

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

## Database and code from the models

```powershell
python design/build_db.py              # create the database from create_tables.sql and check it
python design/generate_code.py         # regenerate the Python skeleton (add --live to read the open VP project)
python design/check_code.py            # compare the generated classes with abc_shop
python showcase/build.py               # rebuild the showcase after a change
```

`create_tables.sql` is written by the `essay.gen` plugin (mode `ddl`, sources in `tools/vpgen`) from the tables, columns
and relationship lines of ERD01-02, with the CHECK and DEFAULT rules stored in the column specifications of the model.

### Generate Database in Visual Paradigm Enterprise (to show live)

Visual Paradigm's own generator needs a database configuration in the project; called through the API without one it
answers "Dialect class not found", so this step has no screenshot yet. To do it in the GUI:

1. Open `TieuLuan_KHANHBQ.vpp` in Visual Paradigm Enterprise and open ERD02 (or ERD01).
2. Tools > DB > Database Configuration: choose SQLite, let VP download the driver, set the database file to
   `design/abc_design_vp.db`, Test Connection.
3. Tools > DB > Generate Database: Action "Create Database", tick "Export to DDL" (folder `design`), Generate.
4. Run `python design/build_db.py` and compare the DDL VP wrote with `design/create_tables.sql`.

## Limits

Payment, carrier and speech recognition are simulated behind fixed interfaces; the shop runs as one process on SQLite
and the performance requirements were not measured; category and customer management have services and tests but no
pages. Two composite UNIQUE keys and four triggers cannot be drawn in an ERD and exist only in `schema.sql`.

Repository: https://github.com/qkhanhbe/ABC-Online-Shop-Information-System
