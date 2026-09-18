from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json

model_name = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


def extract_invoice_data(text:str):
	prompt = f"""Extract invoice information. Return ONLY valid JSON.
		Return ONLY valid JSON.

		Use exactly this schema:

		{{
			"invoice_number": "",
			"date_of_issues": "",
			"client_name": "",
			"client_tax_id": "",
			"total_amount": "",
			"correuncy": ""
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
			max_new_tokens = 500)

	input_length = inputs["input_ids"].shape[1]

	generated_tokens = outputs[0][input_length:]

	answer = tokenizer.decode(
		generated_tokens,
		skip_special_tokens = True)

	try:
		return json.loads(answer)
	except json.JSONDecodeError:
		return{"raw_output": answer}
