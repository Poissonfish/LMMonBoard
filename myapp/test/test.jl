using JWAS, DataFrames, CSV, InvertedIndices, Debugger

phenotypes = CSV.read("myapp/data/customized.csv",
    DataFrame,
    delim=',',
    header=true,
    missingstrings=["NA"])

ped = get_pedigree("myapp/data/customized.ped", header=true, separator=",")

model = build_model("Weight = intercept + Animal + Sire + Animal*CG")
set_covariate(model, "intercept")
set_random(model, "Animal Sire", ped)
set_random(model, "Animal*CG")
sol = solve(model, phenotypes, solver="Gibbs");
