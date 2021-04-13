using JWAS, DataFrames, CSV, InvertedIndices

# data 1
phenotypes = CSV.read("myapp/data/demo_1.csv",
    DataFrame,
    delim=',',
    header=true,
    missingstrings=["NA"])
CSV.write("myapp/data/customized.ped", phenotypes[!, 1:3])
ped = get_pedigree("myapp/data/customized.ped", header=true, separator=",")

# mode 1
model = build_model("Observation = intercept + Weight")
set_covariate(model, "intercept Weight")
# set_random(model, "Weight")
sol = solve(model, phenotypes, solver="Gibbs");


# mode 2
phenotypes
model = build_model("Observation = intercept + Weight + Weight*Weight")
set_covariate(model, "Weight")
sol = solve(model, phenotypes, solver="Gibbs");


# cat con exclude interaction terms
