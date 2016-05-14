from parser import osmiumParser

builtin_types = ("native::text",)

def process_types(ast):
	compounds = {}
	for top_level in ast:
		if top_level.op is None: # a compound
			name, body = top_level.name, top_level.body
			assert name not in compounds, "duplicate compound declaration: %s" % name
			compounds[name] = {}
			for field in body:
				assert field.name not in compounds[name]
				compounds[name][field.name] = (field.type, field.array is not None)
	for name, fields in compounds.items():
		assert name not in builtin_types
		for fieldname, type in fields.items():
			compounds[name][fieldname] = type if type[0] in builtin_types else (compounds[type[0]], type[1])
	return compounds

def process_components(ast, types):
	components = {}
	for top_level in ast:
		if top_level.op is not None: # a component
			assert top_level.op not in components, "duplicate component declaration: %s" % name
			components[top_level.op] = top_level
	return components

def force_type(obj, type):
	if "type" not in obj:
		obj["type"] = type
	else:
		assert obj["type"] == type, "type mismatch"
	return obj

last_name = -1
def generate_name():
	global last_name
	last_name += 1
	return "gen_%d" % last_name

def get_or_create_var(vars, name):
	if name not in vars:
		vars[name] = {}
	return vars[name]

def apply_component(name, inputs, outputs, types, components):
	if name == "native::generate-name":
		assert len(inputs) == 0 and len(outputs) == 1
		force_type(outputs[0], "native::text").text = generate_name()
		return []
	else:
		parts = name.split("/", 1)
		if len(parts) == 2 and len(name) > 1:
			assert parts[0] in types and parts[1] in types[parts[0]]
			if len(inputs) == 1: # extract
				assert len(outputs) == 1
				force_type(inputs[0], parts[0]) WORKING HERE
			return get_or_create_var(
			return elems
		else:
			comp = components[name]
			assert len(inputs) == len(comp.in_) and len(outputs) == len(comp.out)
			vars = {input_name: input_value for input_name, input_value in zip(comp.in_, inputs)}
			vars.update({output_name: output_value for output_name, output_value in zip(comp.out, outputs)})
			elems = []
			for rule in comp.body:
				if rule.snippets is not None:
					elems.append((rule.snippets, vars))
				else:
					new_inputs = [get_or_create_var(vars, var_name) for var_name in rule.in_]
					new_outputs = [get_or_create_var(vars, var_name) for var_name in rule.out]
					elems += apply_component(components[rule.op], new_inputs, new_outputs, types, components)
			return elems

def process(ast):
	types = process_types(ast)
	components = process_components(ast, types)
	print(types)
	elems = apply_component("main", (), (), types, components)
	print(elems)

def main(filename):
	import json
	with open(filename) as f:
		text = f.read()
	parser = osmiumParser(parseinfo=False)
	ast = parser.parse(text, "program", filename=filename)
	dump(ast)
	print("=====")
	process(ast)

def stringify_snippets(snippets):
	out = []
	for snip in snippets:
		if snip.insert is not None:
			out.append(snip.insert)
		elif snip.constant is not None:
			out.append(snip.constant)
		else:
			out.append("<%s>{ %s }" % (snip.loop, stringify_snippets(snip.body)))
	return " ".join(out)

def dump(ast):
	for top_level in ast:
		if top_level.op is not None:
			# component
			print("component", top_level.op, top_level.in_, "->", top_level.out)
			for rule in top_level.body:
				if rule.snippets is not None:
					# native
					print("\tnative", stringify_snippets(rule.snippets))
				else:
					# rule
					print("\trule", rule.op, rule.in_, "->", rule.out)
		else:
			# compound
			print("compound", top_level.name)
			for field in top_level.body:
				print("\tfield", field.type, field.name, "(array)" if field.array is not None else "")

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description="Parser for osmium.")
	parser.add_argument('file', metavar="FILE", help="the input file to parse")
	args = parser.parse_args()

	main(args.file)
