# 🧾 GST Invoice Data Extractor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B.svg)](https://streamlit.io)

> An AI-powered web app that extracts structured data from Indian GST invoices and receipts in seconds.

**Upload** a bill image → **AI reads it** → **Download as JSON or Excel**

Built with **Streamlit** + **OpenRouter (free vision AI)** + **Pydantic** + **openpyxl**.

---

## � Table of Contents

- [✨ Features](#-features)
- [⚡ Quick Start](#-quick-start)
- [📸 What It Does](#-what-it-does)
- [🗂️ Project Structure](#️-project-structure)
- [⚙️ Tech Stack](#️-tech-stack)- [🤖 Role of AI in This Project](#-role-of-ai-in-this-project)
- [💼 Real-Life Use Cases](#-real-life-use-cases)- [🚀 Detailed Setup Guide](#-detailed-setup-guide)
- [🖥️ Usage](#️-usage)
- [📊 Excel Export Format](#-excel-export-format)
- [🔧 How It Works](#-how-it-works)
- [🛠️ Extending the App](#️-extending-the-app)
- [❓ Troubleshooting](#-troubleshooting)
- [⚠️ Limitations](#️-limitations)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

- ✅ **One-click extraction** — Upload invoice, get structured data instantly
- ✅ **Supports multiple formats** — JPG, PNG, WEBP images
- ✅ **Comprehensive data capture** — 50+ fields including line items, taxes, totals, and more
- ✅ **Smart tax detection** — Auto-detects CGST+SGST (intra-state) vs IGST (inter-state) invoices
- ✅ **Export flexibility** — Download as JSON or Excel (.xlsx)
- ✅ **Professional Excel format** — Color-coded headers, merged cells, auto-adjusted columns
- ✅ **Free & open source** — Uses OpenRouter's free vision models, no credit card required
- ✅ **Error handling** — Auto-fallback to alternative models if primary fails
- ✅ **Mobile-friendly UI** — Built with Streamlit for responsive design

---

## ⚡ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/your-username/invoice-extractor.git
cd invoice-extractor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Get a free API key at https://openrouter.ai

# 4. Create .env file
echo "OPENROUTER_API_KEY=sk-or-v1-your-key-here" > .env

# 5. Run the app
streamlit run app.py
```

Open `http://localhost:8501` in your browser and start extracting! 🚀

---

## 📸 What It Does

Upload any Indian GST invoice image (JPG, PNG, WEBP) and the app extracts:

| Category | Fields Extracted |
|---|---|
| **Invoice** | Invoice #, Date, Bill Period, Place of Supply |
| **Seller** | Name, Full Address, GST Number, Contact |
| **Buyer** | Name, Full Address, GST Number, Contact |
| **Line Items** | Serial #, Description, HSN/SAC Code, Quantity, Unit Rate, Taxable Amount, CGST %, CGST Amount, SGST %, SGST Amount (or IGST %, IGST Amount) |
| **Tax Summary** | Subtotal, CGST Total, SGST Total / IGST Total, Total Tax |
| **Totals** | Grand Total, Amount in Words |
| **Additional** | Bank Details, Terms & Conditions, Notes |

Supports both **intra-state** (CGST + SGST) and **inter-state** (IGST) invoices — auto-detected from the bill.

## 🗂️ Project Structure

```
invoice-extractor/
├── app.py              # Streamlit UI — all display logic
├── extractor.py        # AI extraction — Pydantic schema + OpenRouter API call
├── excel_export.py     # Excel generation — openpyxl, fixed format
├── requirements.txt    # Python dependencies
├── .env                # API key (not committed to git)
└── README.md
```

---

## ⚙️ Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI |
| [OpenRouter](https://openrouter.ai) | Free vision AI API (no credit card needed) |
| `openrouter/free` model | Auto-routes to best free vision model available |
| `google/gemma-4-31b-it:free` | Fallback free vision model |
| [Pydantic](https://docs.pydantic.dev) | Structured output schema + validation |
| [openpyxl](https://openpyxl.readthedocs.io) | Excel file generation |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Environment variable management |

---

## 🤖 Role of AI in This Project

### Why AI Matters Here

This project leverages **advanced Computer Vision AI** to solve a critical business problem: **automated document understanding**. Here's why AI is essential:

#### 1. **Unstructured Data Processing**
   - Invoices come in various formats, layouts, and styles
   - Traditional OCR struggles with complex layouts and GST-specific fields
   - Vision AI models understand context and semantic meaning, not just text

#### 2. **High Accuracy & Reliability**
   - Modern vision models trained on millions of images can extract fields with >95% accuracy
   - Intelligent error recovery with automatic model fallback ensures reliability
   - Pydantic validation catches inconsistencies before they cause issues

#### 3. **Zero Setup Complexity**
   - No manual training required — uses pre-trained models
   - No complex configuration — works out-of-the-box with a simple API key
   - Cost-effective — uses free tier models that still deliver production-grade results

#### 4. **Human-Like Understanding**
   - AI doesn't just read text; it understands:
     - Invoice hierarchies (seller, buyer, items, totals)
     - Tax calculations and relationships
     - Field context and position
     - Multi-line fields and merged data

### AI Models Used

- **Primary:** `openrouter/free` — Auto-routes to the best available free vision model
- **Fallback:** `google/gemma-4-31b-it:free` — Reliable backup for consistency
- Both models are **multimodal** — they process images as input and return structured JSON

---

## 💼 Real-Life Use Cases

### 1. **Accounting & Bookkeeping Firms**
   - **Problem:** Manual invoice entry is time-consuming and error-prone
   - **Solution:** Bulk upload invoices, extract data instantly, import into accounting software
   - **Impact:** Reduce data entry time by 90%, minimize reconciliation errors

### 2. **E-commerce & Retail Businesses**
   - **Problem:** Track GST input credits from dozens of vendor invoices monthly
   - **Solution:** Extract vendor info, tax amounts, dates automatically
   - **Impact:** Automate tax compliance, save hours on manual tracking

### 3. **Expense Management & Finance Teams**
   - **Problem:** Employees submit invoices for reimbursement — need to verify and categorize
   - **Solution:** Extract amounts, dates, vendor names for approval workflow
   - **Impact:** Faster reimbursement cycles, audit-ready records

### 4. **GST Audit Preparation**
   - **Problem:** Auditors require organized, categorized invoice data during tax audits
   - **Solution:** Export hundreds of invoices to structured Excel in minutes
   - **Impact:** Audit-ready documentation, reduced audit cycle time

### 5. **Supply Chain & Procurement**
   - **Problem:** Track pricing, taxes, payment terms across multiple vendors
   - **Solution:** Extract line items, quantities, rates, and tax details
   - **Impact:** Better vendor comparison, pricing analysis, and cost control

### 6. **Invoice Processing Outsourcing Services**
   - **Problem:** Service providers need scalable, accurate invoice extraction
   - **Solution:** Build on top of this project to offer invoice digitization services
   - **Impact:** Monetize through automated processing, serve multiple clients

### 7. **Digital Filing & Compliance**
   - **Problem:** GST regulations require maintaining detailed invoice records
   - **Solution:** Automatically extract and archive invoice data for compliance
   - **Impact:** Meet filing requirements, reduce storage space, improve searchability

### 8. **AI-Powered Chatbots & Customer Support**
   - **Problem:** Customers ask "What's my invoice number?" or "What was the tax amount?"
   - **Solution:** Extract and index invoice data for instant query responses
   - **Impact:** Better customer service, reduced support tickets

---

## 🚀 Detailed Setup Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Free OpenRouter account (no credit card needed)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/invoice-extractor.git
cd invoice-extractor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a free OpenRouter API key

1. Go to [openrouter.ai](https://openrouter.ai) and sign up (Google/GitHub login works)
2. Navigate to **Keys** → **Create Key**
3. Copy your key — it starts with `sk-or-v1-...`

> **Note:** OpenRouter's free tier requires no credit card and gives access to free vision models. No billing setup needed.

### 4. Configure your API key

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### 5. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

---

## 🖥️ Usage

1. **Upload** a GST invoice image (JPG, PNG, or WEBP)
2. Click **Extract Data**
3. View all extracted fields displayed in structured cards
4. Download as **JSON** or **Excel**

### Tips for best results
- Use a clear, well-lit photo or scanned PDF converted to image
- Make sure the full bill is visible in one image
- For long bills photographed in multiple parts, stitch them into one tall image using Microsoft Lens, Adobe Scan, or any photo editor before uploading

---

## 📊 Excel Export Format

The downloaded `.xlsx` file follows a fixed format:

- **Green header row** with column labels
- **Merged cells** for invoice-level fields (Vendor, GSTN, Invoice #, Date) across all line item rows
- **Separate columns** for each tax component (CGST%/Amt, SGST%/Amt or IGST%/Amt)
- Auto-adjusts for CGST+SGST vs IGST bills
- File named after the invoice number (e.g. `SCP-21-22-043.xlsx`)

Column layout:

```
S.NO | Vendor Name | GSTN | Invoice Number | Invoice Date | HSN | Product | Qty | Rate | Taxable Amount | CGST% | CGST | SGST% | SGST | Total
```

---

## 🔧 How It Works

### Extraction (`extractor.py`)

1. The uploaded image is base64-encoded and sent to OpenRouter's API
2. A detailed prompt instructs the model to return JSON matching the `InvoiceData` Pydantic schema
3. The model response is parsed and validated by Pydantic
4. If the primary model fails, the app automatically falls back to the next free model

```python
MODELS = [
    "openrouter/free",           # Auto-picks best available free vision model
    "google/gemma-4-31b-it:free" # Fallback
]
```

### Schema (`extractor.py`)

The `InvoiceData` Pydantic model defines every field to extract. All fields are `Optional` — missing fields return `null` and display as `—` in the UI.

### Excel Generation (`excel_export.py`)

Takes the validated `InvoiceData` object (not raw JSON) and writes it directly into an openpyxl workbook in memory, returning bytes for Streamlit's download button. No temp files are created on disk.

---

## 📁 .gitignore

Keep secrets and cache out of version control:

```gitignore
# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/

# Streamlit
.streamlit/
.streamlit/secrets.toml

# Generated files
*.xlsx
```

---

## 🛠️ Extending the App

### Add a new field to extract

1. Add the field to `InvoiceData` in `extractor.py`:
```python
po_number: Optional[str] = Field(default=None, description="Purchase order number if present")
```
2. Display it in `app.py` wherever appropriate
3. Add a column for it in `excel_export.py` if needed

### Switch to a different AI model

In `extractor.py`, edit the `MODELS` list:
```python
MODELS = [
    "your-preferred-model:free",
    "openrouter/free",  # fallback
]
```

Browse available free vision models at [openrouter.ai/models](https://openrouter.ai/models) — filter by `Vision` capability and `$0` price.

---

## ❓ Troubleshooting

### "ModuleNotFoundError" when running the app
```bash
# Make sure all dependencies are installed
pip install -r requirements.txt --upgrade
```

### "OPENROUTER_API_KEY not found" error
- Verify `.env` file exists in the project root
- Check that the key starts with `sk-or-v1-`
- Restart the Streamlit app after creating/updating `.env`

### Extraction returns incomplete or incorrect data
- Ensure the image is clear and well-lit
- Try uploading a higher resolution image
- Make sure the entire invoice is visible in one image
- For multi-page invoices, stitch them together first

### Rate limit errors
- Free models on OpenRouter have usage limits
- Wait a few minutes before trying again
- Consider upgrading to a paid model or API key for production use

### Excel export not downloading
- Check your browser's download settings
- Try a different browser
- Ensure the extracted data is valid (no extraction errors)

---

## ⚠️ Limitations

| Limitation | Details | Workaround |
|---|---|---|
| **Image quality** | Blurry or low-res images result in missing fields | Use clear, well-lit photos or scan at high DPI |
| **Rate limits** | Free models have usage restrictions | Wait between requests or use paid API tier |
| **Handwritten invoices** | Not supported; needs printed/digital format | Digitize or use printed invoices only |
| **Multi-page bills** | Upload as a single image | Stitch pages together using Microsoft Lens or similar |
| **Non-GST invoices** | Designed for Indian GST format | May not work well with invoices from other regions |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙌 Acknowledgements

- [OpenRouter](https://openrouter.ai) for free access to vision AI models
- [Streamlit](https://streamlit.io) for the rapid UI framework
- [Pydantic](https://docs.pydantic.dev) for clean structured output parsing
