# Multi-Modal Evidence Review — Solution Documentation

An automated, end-to-end multi-modal pipeline designed to evaluate claims by analyzing conversation logs alongside corresponding image evidence. [cite_start]The system utilizes advanced Vision-Language Models (VLMs) to classify issues, determine evidence sufficiency, verify object part visibility, and flag operational risks[cite: 6, 8].

---

## 🛠️ Prerequisites

- **Runtime:** Python 3.10+
- **Environment Variables:** Must have a valid `GOOGLE_API_KEY` configured in your environment.
- **Dependencies:** Install the required packages via pip:
  ```bash
  pip install -r requirements.txt
  ```

---

## 🚀 Usage

### 1. Execute Predictions

To run the inference pipeline on the evaluation dataset, execute the main entry point. This reads the input corpus and generates the required compliance file.

```bash
python3 code/main.py

```

*  **Input:** `dataset/claims.csv` (or the configured test set) 


*  **Output:** `output.csv` (populated with predictions mapping strictly to the target schema) 



### 2. Run the Evaluation Suite

To execute the local evaluation workflow, compute performance metrics, and verify categorical consistency, run the evaluation script:

```bash
python3 code/evaluation/main.py

```

*  **Input:** `dataset/sample_claims.csv` 


*  **Outputs Written To:** `code/evaluation/` 

---

## 📊 Expected Outputs & Deliverables

Upon running the tasks above, the system outputs the following verified submission artifacts:

*  **`output.csv`** Contains the fully predicted test rows, strictly adhering to the 14-column categorical limits and schema layout specified in the problem criteria.


* **`code/evaluation/predictions_sample.csv`**
A localized cache of predicted outputs generated across the evaluation sample subset.

* **`code/evaluation/evaluation_report.md`**
A comprehensive operational review highlighting categorical accuracy, breakdown metrics, and pipeline alignment.

---

## 🏗️ System Architecture

```
                    ┌──────────────────┐
                    │  Claims & Images │
                    └─────────┬────────┘
                              ▼
           ┌──────────────────────────────────────┐
           │ Base64 Image Processing & Validation │
           └──────────────────┬───────────────────┘
                              ▼
         ┌──────────────────────────────────────────┐
         │ Structured VLM Prompt Orchestration (v3) │
         └──────────────────┬───────────────────────┘
                              ▼
           ┌──────────────────────────────────────┐
           │   Gemini Multi-Modal API Inference   │
           └──────────────────┬───────────────────┘
                              ▼
         ┌──────────────────────────────────────────┐
         │  Claim Post-Processor Override System    │
         └──────────────────┬───────────────────────┘
                              ▼
                    ┌──────────────────┐
                    │    output.csv    │
                    └──────────────────┘

```

The system employs a high-throughput, single-pass VLM pipeline built around structured multi-modal prompting. Each claim turn is processed as an isolated context unit:

1.  **Context Packaging:** Text-based conversation records, historical user data, and strict evidence validation boundaries are bundled dynamically.


2.  **Multi-Modal Payload:** Source images are validated, base64-encoded, and appended directly to the context stream.


3.  **Structured Prompting (v3):** Utilizes targeted VLM prompt engineering specifically optimized to identify wrong object parts, flag blurry or low-quality media, and handle tricky edge cases like missing package contents or text instructions overlaid on images.


4.  **Post-Processor Override Engine:** Implements a deterministic parsing layer to rectify structural anomalies, ensuring robust handling of car/package classification mismatches before writing final schemas.



---

## 📁 Repository Blueprint

```text
├── code/
│   ├── main.py                  # Operational entry point for building final test predictions
│   ├── claim_processor.py       # core multi-modal orchestration & override engine
│   ├── prompts_v3.py            # Production VLM prompt layouts and criteria definitions
│   ├── data_loader.py           # Utilities for CSV parsing and input stream handling
│   ├── image_utils.py           # Image validation, formatting, and Base64 compilation
│   └── evaluation/
│       └── main.py              # Performance evaluation framework and validation runner
├── dataset/                     # Local data partitions (excluded from deployment bundle)
├── README.md                    # Core project repository guidance
└── AGENTS.md                    # Multi-agent system tracking configurations

```