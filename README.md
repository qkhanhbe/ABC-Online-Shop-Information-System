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

- `tieuluan_V1_04_049_KHANHBQ.pdf` - essay report (5 chapters)
- `TieuLuan_KHANHBQ.vpp` - Visual Paradigm project with all 24 diagrams
- `diagrams/` - PNG export of the diagrams (context, use case, activity, DFD, sequence, class, state, ERD,
  component, package, deployment)
- `abc_shop/` - Python source: model, dao, service, ai, controller, view, tests
- `demo_results/` - demo, evaluation and test output; screenshots of the web application

## Chapters

| Chapter | Content | Diagrams |
|---|---|---|
| 1. Requirement Determination | Business problems, stakeholders, needs, FR/NFR, 32 use cases, traceability | CTX01, UC00 |
| 2. Analysis | Activity, DFD, sequence (BCE), analysis classes, order state machine, data model | AD01-03, DFD0-1, SD01-02, CL01, ST01, ERD01 |
| 3. AI in E-commerce | Multimodal search, review insights, recommender; evaluation, risks, fallbacks | UC_AI, CMP01, SD03-04, AD04 |
| 4. Design | Four steps: methods, use dependencies, DAO, MVC packages; checkout design; deployment | DCL01-03, PKG01, SD05, CMP02, DEP01 |
| 5. Code | Implementation, screenshots, tests, traceability to code | - |
