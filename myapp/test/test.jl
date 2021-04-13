using JWAS, DataFrames, CSV, InvertedIndices, Debugger

# data 1
phenotypes = CSV.read("myapp/data/demo_1.csv",
    DataFrame,
    delim=',',
    header=true,
    missingstrings=["NA"])
CSV.write("myapp/data/customized.ped", phenotypes[!, 1:3])
ped = get_pedigree("myapp/data/customized.ped", header=true, separator=",")

# mode 1
phenotypes
model = build_model("Observation = intercept + Animal")
set_covariate(model, "intercept")
set_random(model, "Animal", ped)
sol = solve(model, phenotypes, solver="Gibbs");

# mode 2

