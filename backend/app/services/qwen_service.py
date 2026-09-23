from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import re

model_name = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


def extract_invoice_data(text:str):
	prompt = f"""Extract invoice information. Return ONLY valid JSON.
		Return ONLY valid JSON.

		Do NOT explain your answer.
		Do NOT add comments.
		Do NOT markdown.
		Do NOT add code examples.
		Do NOT add Python code.
		Do NOT add any text before or after JSON.

		CRITICAL RULES:
		- Extract values exactly as they appear in the invoice.
		- Do not invent or guess missing values.
		- If a field cannot be found, return an empty string.
		- Return ONLY the final extracted value for each field.
  
		CLIENT NAME RULES:
 
		- The client name is located on the top right side of the invoice.
		- It is usually below the issue date.
		- Return ONLY the actual company or person name.
		- NEVER return labels such as:
			"Client"
			"Client:"
			"Buyer"
			"Buyer:"
			"Customer"
			"Customer:"
			"Seller"
			"Seller:"
			"Bill To"
			"Bill To:"
		- Remove any label prefixes and return only the name itself.
		- If the extracted value is exactly "Client", "Buyer", "Customer", "Seller" or similar label, treat it as invalid and continue searching for the actual name.
		- The client name must contain the company/person name, not a field label.
  
		CLIENT TAX ID RULES:
  
		- Return the tax ID belonging to the client.
		- It is usually directly below the client name.
  
		TOTAL AMOUNT RULES:

		- Return the FINAL invoice total.
		- The total amount is usually located in the last row and last column of the invoice table.
		- Prefer the grand total amount.
		- Ignore line item amounts, subtotals, VAT percentages and unit prices.
		- If multiple totals exist, choose the largest final payable amount.
  
		Expected format:

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
