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

		Return the actual company name, not labels such as "Client", "Seller", "Buyer" or similar.

		Expected format:

		{{
			"invoice_number": "",
			"date_of_issue": "",
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
			max_new_tokens = 800)

	input_length = inputs["input_ids"].shape[1]

	generated_tokens = outputs[0][input_length:]

	answer = tokenizer.decode(
		generated_tokens,
		skip_special_tokens = True)

	match = re.search(r"\{.*\}", answer, re.DOTALL)
	if match:
		try:
			return json.loads(match.group())
		except json.JSONDecodeError:
			return{"raw_output": answer}
	return {"raw_output": answer}
