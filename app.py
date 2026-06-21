import json
import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from extractor import extract_invoice_data
from excel_export import generate_excel

load_dotenv()

st.set_page_config(page_title="GST Invoice Extractor", page_icon="🧾", layout="centered")

st.markdown("""
<style>
    .main { background-color: #0f1117; }
    h1 { font-size: 2rem; font-weight: 700; color: #f0f0f0; }
    .subtitle { color: #888; margin-top: -0.5rem; margin-bottom: 1.5rem; font-size: 0.95rem; }

    .card {
        background: #1c1e26;
        border: 1px solid #2a2d3a;
        border-radius: 12px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #4ade80;
        margin-bottom: 0.8rem;
    }
    .field-label {
        font-size: 0.68rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.55rem;
    }
    .field-value {
        font-size: 0.95rem;
        color: #f0f0f0;
        font-weight: 500;
        margin-top: 0.1rem;
    }
    .field-value-small {
        font-size: 0.85rem;
        color: #ccc;
        margin-top: 0.1rem;
        line-height: 1.45;
    }
    .total-value {
        font-size: 1.6rem;
        color: #4ade80;
        font-weight: 700;
    }
    .words-value {
        font-size: 0.82rem;
        color: #aaa;
        font-style: italic;
        margin-top: 0.2rem;
    }
    .thumb-filename { font-size: 0.95rem; font-weight: 600; color: #f0f0f0; margin-bottom: 0.2rem; word-break: break-all; }
    .thumb-meta { font-size: 0.78rem; color: #888; }

    /* Two-col grid used for seller/purchaser */
    .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem; }
    /* Three-col grid for invoice summary */
    .three-col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-bottom: 1rem; }
    /* Four-col grid for totals row */
    .four-col { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 1rem; margin-bottom: 1rem; }

    /* Line items table */
    .items-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
    .items-table th {
        font-size: 0.68rem; color: #888; text-align: left;
        padding: 0.4rem 0.5rem; border-bottom: 1px solid #2a2d3a;
        white-space: nowrap;
    }
    .items-table td {
        color: #d0d0d0; padding: 0.45rem 0.5rem;
        border-bottom: 1px solid #1a1c24; vertical-align: top;
    }
    .items-table tr:last-child td { border-bottom: none; }
    .num { text-align: right; }
    .tag {
        display: inline-block;
        background: #2a2d3a;
        color: #aaa;
        font-size: 0.68rem;
        padding: 0.1rem 0.4rem;
        border-radius: 4px;
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🧾 GST Invoice Extractor")
st.markdown('<p class="subtitle">Upload a GST bill — AI extracts all fields instantly.</p>', unsafe_allow_html=True)

if not os.getenv("OPENROUTER_API_KEY"):
    st.error("⚠️  `OPENROUTER_API_KEY` not found. Add it to your `.env` file and restart.")
    st.stop()

uploaded = st.file_uploader(
    "Drop a GST invoice image here",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed",
)

if not uploaded:
    st.info("Supported formats: JPG, PNG, WEBP")
    st.stop()

# ── Thumbnail preview ─────────────────────────────────────────────────────────
image = Image.open(uploaded)
file_size_kb = round(len(uploaded.getvalue()) / 1024, 1)
thumb_col, info_col = st.columns([1, 3])
with thumb_col:
    st.image(image, width=110, clamp=True)
with info_col:
    st.markdown(f"""
    <div style="padding:0.4rem 0;">
        <div class="thumb-filename">{uploaded.name}</div>
        <div class="thumb-meta">{file_size_kb} KB &nbsp;·&nbsp; {image.width} × {image.height} px</div>
    </div>
    """, unsafe_allow_html=True)

# ── Extract button ────────────────────────────────────────────────────────────
if st.button("Extract Data", type="primary", use_container_width=True):
    with st.spinner("Reading invoice…"):
        ext = uploaded.name.rsplit(".", 1)[-1].lower()
        media_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
        media_type = media_map.get(ext, "image/jpeg")
        try:
            data = extract_invoice_data(uploaded.getvalue(), media_type)
        except Exception as e:
            st.error(f"Extraction failed: {e}")
            st.stop()

    st.success("Extraction complete!")
    st.divider()

    curr = data.currency or "INR"

    # ── 1. Invoice details ────────────────────────────────────────────────────
    st.markdown(f"""
<div class="three-col">
  <div class="card">
    <div class="section-title">🧾 Invoice</div>
    <div class="field-label">Invoice #</div>
    <div class="field-value">{data.invoice_number or '—'}</div>
    <div class="field-label">Date</div>
    <div class="field-value">{data.invoice_date or '—'}</div>
    <div class="field-label">Bill Period</div>
    <div class="field-value">{data.bill_period or '—'}</div>
  </div>
  <div class="card">
    <div class="section-title">📍 Supply</div>
    <div class="field-label">Place of Supply</div>
    <div class="field-value">{data.place_of_supply or '—'}</div>
    <div class="field-label">Currency</div>
    <div class="field-value">{curr}</div>
  </div>
  <div class="card">
    <div class="section-title">💰 Grand Total</div>
    <div class="field-label">Total Amount</div>
    <div class="total-value">{"₹{:,.2f}".format(data.total_amount) if data.total_amount is not None else "—"}</div>
    <div class="words-value">{data.total_in_words or ''}</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── 2. Seller & Purchaser ─────────────────────────────────────────────────
    st.markdown(f"""
<div class="two-col">
  <div class="card">
    <div class="section-title">🏪 Seller</div>
    <div class="field-label">Name</div>
    <div class="field-value">{data.seller_name or '—'}</div>
    <div class="field-label">Address</div>
    <div class="field-value-small">{data.seller_address or '—'}</div>
    <div class="field-label">GST Number</div>
    <div class="field-value">{data.seller_gst or '—'}</div>
    <div class="field-label">Contact</div>
    <div class="field-value">{data.seller_contact or '—'}</div>
  </div>
  <div class="card">
    <div class="section-title">🧑 Purchaser</div>
    <div class="field-label">Name</div>
    <div class="field-value">{data.purchaser_name or '—'}</div>
    <div class="field-label">Address</div>
    <div class="field-value-small">{data.purchaser_address or '—'}</div>
    <div class="field-label">GST Number</div>
    <div class="field-value">{data.purchaser_gst or '—'}</div>
    <div class="field-label">Contact</div>
    <div class="field-value">{data.purchaser_contact or '—'}</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── 3. Line items table ───────────────────────────────────────────────────
    if data.line_items:
        # Detect if IGST bill or CGST+SGST bill
        has_igst = any(i.igst_amount is not None for i in data.line_items)

        rows = ""
        for item in data.line_items:
            sr = item.sr_no if item.sr_no is not None else "—"
            qty = item.quantity if item.quantity is not None else "—"
            rate = f"₹{item.rate:,.2f}" if item.rate is not None else "—"
            taxable = f"₹{item.taxable_amount:,.2f}" if item.taxable_amount is not None else "—"
            hsn = item.hsn_sac if item.hsn_sac else '—'

            if has_igst:
                igst_pct = f"{item.igst_percent}%" if item.igst_percent is not None else "—"
                igst_amt = f"₹{item.igst_amount:,.2f}" if item.igst_amount is not None else "—"
                tax_cols = f"<td class='num'>{igst_pct}</td><td class='num'>{igst_amt}</td>"
            else:
                cgst_pct = f"{item.cgst_percent}%" if item.cgst_percent is not None else "—"
                cgst_amt = f"₹{item.cgst_amount:,.2f}" if item.cgst_amount is not None else "—"
                sgst_pct = f"{item.sgst_percent}%" if item.sgst_percent is not None else "—"
                sgst_amt = f"₹{item.sgst_amount:,.2f}" if item.sgst_amount is not None else "—"
                tax_cols = f"<td class='num'>{cgst_pct}</td><td class='num'>{cgst_amt}</td><td class='num'>{sgst_pct}</td><td class='num'>{sgst_amt}</td>"

            total = f"₹{item.total:,.2f}" if item.total is not None else "—"

            rows += f"""<tr>
              <td>{sr}</td>
              <td>{item.description}</td>
              <td class='num'>{hsn}</td>
              <td class='num'>{qty}</td>
              <td class='num'>{rate}</td>
              <td class='num'>{taxable}</td>
              {tax_cols}
              <td class='num'>{total}</td>
            </tr>"""

        if has_igst:
            tax_headers = "<th class='num'>IGST %</th><th class='num'>IGST Amt</th>"
        else:
            tax_headers = "<th class='num'>CGST %</th><th class='num'>CGST Amt</th><th class='num'>SGST %</th><th class='num'>SGST Amt</th>"

        st.markdown(f"""
<div class="card" style="overflow-x:auto;">
  <div class="section-title">📦 Line Items</div>
  <table class="items-table">
    <thead>
      <tr>
        <th>#</th><th>Item & Description</th><th class='num'>HSN/SAC</th><th class='num'>Qty</th><th class='num'>Rate</th>
        <th class='num'>Taxable Amt</th>{tax_headers}<th class='num'>Total</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</div>""", unsafe_allow_html=True)

    # ── 4. Tax summary ────────────────────────────────────────────────────────
    has_igst_total = data.total_igst is not None
    st.markdown(f"""
<div class="four-col">
  <div class="card">
    <div class="field-label">Subtotal (Taxable)</div>
    <div class="field-value">{'₹{:,.2f}'.format(data.subtotal) if data.subtotal is not None else '—'}</div>
  </div>
  <div class="card">
    <div class="field-label">{'IGST' if has_igst_total else 'CGST'}</div>
    <div class="field-value">{'₹{:,.2f}'.format(data.total_igst if has_igst_total else data.total_cgst) if (data.total_igst or data.total_cgst) is not None else '—'}</div>
  </div>
  <div class="card">
    <div class="field-label">{'—' if has_igst_total else 'SGST'}</div>
    <div class="field-value">{'—' if has_igst_total else ('₹{:,.2f}'.format(data.total_sgst) if data.total_sgst is not None else '—')}</div>
  </div>
  <div class="card">
    <div class="field-label">Total Tax</div>
    <div class="field-value">{'₹{:,.2f}'.format(data.total_tax) if data.total_tax is not None else '—'}</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── 5. Bank details & Notes ───────────────────────────────────────────────
    if data.bank_details or data.notes:
        st.markdown(f"""
<div class="two-col">
  {'<div class="card"><div class="section-title">🏦 Bank Details</div><div class="field-value-small">' + data.bank_details + '</div></div>' if data.bank_details else '<div></div>'}
  {'<div class="card"><div class="section-title">📋 Notes / Terms</div><div class="field-value-small">' + data.notes + '</div></div>' if data.notes else '<div></div>'}
</div>""", unsafe_allow_html=True)

    # ── 6. Raw JSON & Downloads ──────────────────────────────────────────────
    with st.expander("View raw JSON"):
        st.code(data.model_dump_json(indent=2), language="json")

    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        st.download_button(
            label="⬇️  Download JSON",
            data=data.model_dump_json(indent=2),
            file_name="invoice_data.json",
            mime="application/json",
            use_container_width=True,
        )
    with dl_col2:
        try:
            excel_bytes = generate_excel(data)
            invoice_id = data.invoice_number or "invoice"
            safe_name = invoice_id.replace("/", "-").replace(" ", "_")
            st.download_button(
                label="⬇️  Download Excel",
                data=excel_bytes,
                file_name=f"{safe_name}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Excel generation failed: {e}")