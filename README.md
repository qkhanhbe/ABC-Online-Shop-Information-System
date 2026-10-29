# ABC Online Shop - From Requirements to Code

Course essay for **Information System Analysis and Design** (PTIT, class 04): one e-commerce information system
followed through requirement determination, analysis, AI in e-commerce, design and code.

Student: Be Quoc Khanh (KHANHBQ), B23DCCE049

## Run the application

```powershell
cd abc_shop
python -m pip install -r requirements.txt
python main.py serve          # http://localhost:8000
python main.py demo           # end-to-end scenario in the terminal
python -m pytest -q           # 40 tests
python evaluate.py            # AI evaluation
```

See [abc_shop/README.md](abc_shop/README.md) for all commands, demo accounts and the package structure.

## Project files

- `design_04_10_KhanhBQ_049.pdf` - essay report (5 chapters)
- `TieuLuan_KHANHBQ.vpp` - Visual Paradigm project with all 29 diagrams
- `diagrams/` - PNG export of the diagrams from VP Community Edition (CTX01, DFD0, DFD1 are drawn from
  the stored project layout, as Community Edition cannot open data flow diagrams) (context, use case, activity, DFD, sequence, class, state, ERD,
  component, package, deployment)
- `abc_shop/` - Python source: model, dao, service, ai, controller, view, tests
- `design/` - Chapter 4: `create_tables.sql` generated from ERD01-02, `build_db.py` (builds and checks the
  database), `generate_code.py` (Python skeleton from the design classes, `--live` reads the open VP project)
  and `check_code.py` (compares the generated classes with `abc_shop/`)
- `demo_results/` - demo, evaluation and test output; screenshots of the web application

## Chapters

| Chapter | Content | Diagrams |
|---|---|---|
| 1. Requirement Determination | Business problems, stakeholders, needs, FR/NFR, 32 use cases, traceability | CTX01, UCD1-UCD4 |
| 2. Analysis | Activity, DFD, sequence (BCE), analysis classes, order state machine, data model | AD01-03, DFD0-1, SD01-02, CL01, ST01 |
| 3. AI in E-commerce | Multimodal search, review insights, recommender; evaluation, risks, fallbacks | UC_AI, CMP01, SD03-04, AD04 |
| 4. Design | Updated analysis classes, data model and generated database, design classes, layers and one slice, code generated from the model | CL01, ERD01-02, DCL01-04, PKG01, SD05 |
| 5. Code | Implementation, screenshots, tests, traceability to code | - |
