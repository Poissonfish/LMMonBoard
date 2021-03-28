#  Package imports
import Pkg
# Pkg.add(["JWAS", "DataFrames", "CSV"])
using JWAS, DataFrames, CSV
# print(versioninfo())
# Weight = intercept + Animal + Dam + CG
# take inputs
# ARG = ["myapp/res/demo_Rosa.csv", "Weight = Animal + Sire", "Animal", "Sire"]
ARG = ["myapp/res/demo.csv", 
    "Weight = intercept + Animal + Dam + CG",
    "CG",
    "Animal Dam"]
arg_file, arg_eq, arg_cov, arg_random = ARG
# arg_file, arg_eq, arg_cov, arg_random = ARGS

# Step 2: Read data
phenotypes = CSV.read(arg_file,
    DataFrame,
    delim=',',
    header=true,
    missingstrings=["NA"])

ped=get_pedigree("myapp/res/ped.csv",header=true)

# Step 3: Build Model Equationcovs
model = build_model(arg_eq); # set residual var

# Step 4: Set Factors or Covariates
set_covariate(model, arg_cov);

# Step 5: Set Random or Fixed Effects
# set_random(model, "Animal Dam", ped); # set random var
ids,Ai,inbred=get_info(ped,Ai=true)
set_random(model, "Animal Dam",Vinv=Ai,names=ids); # set random var
A=[ids abs.(round.(inv(Matrix(Ai)),digits=2))]

# Step 6: Solve Mixed Model Equations
out = solve(model, phenotypes);

# Step 7: Exports
CSV.write("myapp/out/jwas_y.csv", DataFrame(phenotypes[:, 1:2]))
CSV.write("myapp/out/jwas_names.csv", DataFrame(names=out[1]))
CSV.write("myapp/out/jwas_designMat.csv", DataFrame(Matrix(out[2])))
CSV.write("myapp/out/jwas_LHS.csv", DataFrame(Matrix(out[3])))
CSV.write("myapp/out/jwas_RHS.csv", DataFrame(Matrix(out[4])))
