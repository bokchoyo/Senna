import json

# Load cars.json
with open(r"C:\Users\bokch\PyCharm\W1\data\cars.json", "r") as infile:
    cars_data = json.load(infile)

# Transform data
result = {}
result["make_list"] = list(cars_data.keys())

for make, models in cars_data.items():
    make_data = {"model_list": list(models.keys())}
    for model, trims in models.items():
        model_data = {"trim_list": list(trims.keys())}
        for trim, years in trims.items():
            trim_years = list(years.keys())
            model_data[trim] = trim_years
        make_data[model] = model_data
    result[make] = make_data

# Write the transformed data to a new JSON file
with open(r"/data/cars_list.json", "w") as outfile:
    json.dump(result, outfile, indent=4)

print("Transformed JSON with trims has been saved to 'output_with_trims.json'")
