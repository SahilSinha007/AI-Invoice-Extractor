import base64
import json
import os
from typing import Optional
from openai import OpenAI
from pydantic import BaseModel, Field


# ---------- Pydantic schema ----------

class LineItem(BaseModel):
    sr_no: Optional[int] = Field(default=None, description="Serial number of the line item")
    description: str = Field(description="Item name and description")
    hsn_sac: Optional[str] = Field(default=None, description="HSN or SAC code for the item")
    quantity: Optional[float] = Field(default=None, description="Quantity")
    rate: Optional[float] = Field(default=None, description="Rate per unit")
    taxable_amount: Optional[float] = Field(default=None, description="Taxable amount before GST")
    cgst_percent: Optional[float] = Field(default=None, description="CGST percentage")
    cgst_amount: Optional[float] = Field(default=None, description="CGST amount")
    sgst_percent: Optional[float] = Field(default=None, description="SGST percentage")
    sgst_amount: Optional[float] = Field(default=None, description="SGST amount")
    igst_percent: Optional[float] = Field(default=None, description="IGST percentage if applicable")
    igst_amount: Optional[float] = Field(default=None, description="IGST amount if applicable")
    total: Optional[float] = Field(default=None, description="Total amount for this line item including GST")


class InvoiceData(BaseModel):
    # Invoice details
    invoice_number: Optional[str] = Field(default=None, description="Invoice number e.g. SCP/21-22/043")
    invoice_date: Optional[str] = Field(default=None, description="Invoice date as written on bill")
    place_of_supply: Optional[str] = Field(default=None, description="Place of supply state and code")
    bill_period: Optional[str] = Field(default=None, description="Bill period if mentioned")

    # Seller info
    seller_name: Optional[str] = Field(default=None, description="Name of the seller/vendor/company")
    seller_address: Optional[str] = Field(default=None, description="Full address of the seller")
    seller_gst: Optional[str] = Field(default=None, description="GST number of the seller e.g. 23AAWPH7376L2ZX")
    seller_contact: Optional[str] = Field(default=None, description="Phone/contact number of the seller")

    # Purchaser info
    purchaser_name: Optional[str] = Field(default=None, description="Name of the buyer/purchaser")
    purchaser_address: Optional[str] = Field(default=None, description="Full address of the buyer")
    purchaser_gst: Optional[str] = Field(default=None, description="GST number of the buyer if present")
    purchaser_contact: Optional[str] = Field(default=None, description="Contact number of the buyer if present")

    # Line items
    line_items: list[LineItem] = Field(default_factory=list, description="List of all items in the invoice")

    # Totals
    subtotal: Optional[float] = Field(default=None, description="Sub total / taxable amount before GST")
    total_cgst: Optional[float] = Field(default=None, description="Total CGST amount")
    total_sgst: Optional[float] = Field(default=None, description="Total SGST amount")
    total_igst: Optional[float] = Field(default=None, description="Total IGST amount if applicable")
    total_tax: Optional[float] = Field(default=None, description="Total tax amount (CGST+SGST or IGST)")
    total_amount: Optional[float] = Field(default=None, description="Final grand total amount payable")
    total_in_words: Optional[str] = Field(default=None, description="Total amount written in words")
    currency: Optional[str] = Field(default="INR", description="Currency, default INR for Indian invoices")

    # Bank / payment details
    bank_details: Optional[str] = Field(default=None, description="Bank name, account number, IFSC if present")

    # Notes
    notes: Optional[str] = Field(default=None, description="Terms and conditions, remarks, or any other notes")


# Free vision-capable models to try in order
MODELS = [
    "openrouter/free",
    "google/gemma-4-31b-it:free",
]


# ---------- Extraction function ----------

def extract_invoice_data(image_bytes: bytes, media_type: str = "image/jpeg") -> InvoiceData:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )

    b64_image = base64.standard_b64encode(image_bytes).decode("utf-8")
    schema_json = json.dumps(InvoiceData.model_json_schema(), indent=2)

    prompt = f"""You are an expert Indian GST invoice data-entry assistant. Extract every field from this GST bill/invoice image.

Return ONLY a valid JSON object matching this schema — no extra text, no markdown fences:

{schema_json}

Important rules:
- Use null for any field not found on the bill.
- All amounts as plain numbers (e.g. 47000.00 not "₹47,000").
- Preserve dates exactly as written (e.g. "11/12/2021").
- GST numbers are 15-character alphanumeric codes — extract exactly as shown.
- For line items, extract every row including HSN/SAC code, taxable amount, CGST %, CGST amt, SGST %, SGST amt, IGST % and IGST amt.
- If IGST is used instead of CGST+SGST, put values in igst fields and leave cgst/sgst as null.
- Capture full addresses as single strings with line breaks replaced by commas.
- If there are no line items, return an empty list."""

    last_error = None
    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:{media_type};base64,{b64_image}"},
                            },
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
            )

            raw = response.choices[0].message.content.strip()

            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()

            parsed = json.loads(raw)
            return InvoiceData(**parsed)

        except Exception as e:
            last_error = e
            continue

    raise RuntimeError(f"All models failed. Last error: {last_error}")