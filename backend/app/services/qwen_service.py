from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import re

model_name = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


def extract_invoice_data(text:str):
	prompt = f"""
		You are an invoice data extraction engine.

		Return ONLY valid JSON.
		Do NOT explain.
		Do NOT write code.
		Do NOT write regex.
		Do NOT write Python.
		Do NOT add comments.
		Do NOT add markdown.
		Do NOT add text before JSON.
		Do NOT add text after JSON.

		Extraction rules:

		- Extract values exactly as written in the invoice.
		- If a value is missing return "".
		- Never guess.

		Client rules:

		- Ignore the Seller section completely.
		- Extract information ONLY from the Client section.
		- The Client section contains the buyer information.
		- The Seller section contains supplier information and must be ignored.

		Client name:

		- Return only the client company name.
		- Do not include addresses.
		- Do not include cities.
		- Do not include tax IDs.
		- Do not concatenate seller and client names.
		- If both Seller and Client are present, choose only the Client company.

		Client tax ID:

		- Return only the tax ID from the Client section.
		- Ignore seller tax IDs.
		- If multiple tax IDs exist, choose the one closest to the client company name.

		Total amount:

		- Return the final payable invoice amount.
		- Ignore item amounts.
		- Ignore subtotals.
		- Ignore VAT rows.
		- Use the grand total.

		Return EXACTLY this JSON:

		{{
			"invoice_number": "",
			"date_of_issue": "",
			"client_name": "",
			"client_tax_id": "",
			"total_amount": "",
			"currency": ""
		}}

		Invoice text:

		{text}
		"""


	inputs = tokenizer(
		prompt,
		return_tensors = "pt")
	with torch.no_grad():
		outputs = model.generate(
			**inputs,
			max_new_tokens = 800)

	input_length = inputs["input_ids"].shape[1]

	generated_tokens = outputs[0][input_length:]

	answer = tokenizer.decode(
		generated_tokens,
		skip_special_tokens = True)

	match = re.search(r"\{.*\}", answer, re.DOTALL)
	if match:
		try:
			return json.loads(match.group()) #parsiranje json-a 
		except json.JSONDecodeError:
			return{"raw_output": answer}
	return {"raw_output": answer}
