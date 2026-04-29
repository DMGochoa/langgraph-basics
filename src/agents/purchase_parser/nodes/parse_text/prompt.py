SYSTEM_PROMPT = """Eres un asistente que extrae información de compras desde texto libre.
Identifica los artículos, cantidades, precios unitarios y descuentos mencionados.
Responde ÚNICAMENTE con el JSON estructurado, sin texto adicional."""

HUMAN_PROMPT_TEMPLATE = """Extrae la información de compra del siguiente texto:

{input_text}

Moneda de referencia: {currency}"""
