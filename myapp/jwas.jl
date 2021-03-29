# Imports
import Pkg
# Pkg.add(["JWAS", "DataFrames", "CSV", "InvertedIndices])
using JWAS, DataFrames, CSV, InvertedIndices

# Step 1: Take inputs
df_param = CSV.read("myapp/out/param.csv", DataFrame, header=false)
ARG = Dict()
ARG["data"] = df_param[1, 1]
ARG["ped"] = df_param[2, 1]
ARG["eq"] = df_param[3, 1]
ARG["cov"] = df_param[4, 1]
ARG["rdmstr"] = df_param[5, 1]
ARG["rdmiid"] = df_param[6, 1]
ARG["ve"] = parse(Int64, df_param[7, 1])
ARG["vu"] = parse(Int64, df_param[8, 1])

# Step 2: Read data
phenotypes = CSV.read(ARG["data"],
    DataFrame,
    delim=',',
    header=true,
    missingstrings=["NA"])
ped = get_pedigree(ARG["ped"], header=true)

# Step 3: Build Model Equationcovs
model = build_model(ARG["eq"], ARG["ve"]); # set residual var

# Step 4: Set Factors or Covariates
set_covariate(model, ARG["cov"]);

# Step 5: Set Random or Fixed Effects
set_random(model, ARG["rdmstr"], ped); # set random var
set_random(model, ARG["rdmiid"], ARG["vu"]); # set random var

# Step 6: Solve Mixed Model Equations
sol = solve(model, phenotypes, solver="Gibbs");
out = solve(model, phenotypes);

# Step 7: Organize outputs
# get response variables
ls_terms = split(ARG["eq"], r"\s*=\s*")
name_y = ls_terms[1]

# get random index 
ls_rdmstr = split(ARG["rdmstr"], r"\s")
ls_rdmiid = split(ARG["rdmiid"], r"\s")
ls_rdm = vcat(ls_rdmstr, ls_rdmiid)

idx_rdm = Int8[]
for rdm in ls_rdm
    idx = findall(x -> occursin(rdm, x), sol[:, 1])
    append!(idx_rdm, idx)
end

# Step 8.1 Make solution DF
df_fix = DataFrame()
df_fix[:, :terms] = replace.(sol[Not(idx_rdm), 1], "$name_y:"=>"")
df_fix[:, :terms] = replace.(df_fix.terms, "intercept:"=>"")
df_fix[:, :effects] = sol[Not(idx_rdm), 2]
df_fix[:, :isFixed] .= 1

df_rdm = DataFrame()
df_rdm[:, :terms] = replace.(sol[idx_rdm, 1], "$name_y:"=>"")
df_rdm[:, :effects] = sol[idx_rdm, 2]
df_rdm[:, :isFixed] .= 0
df_sol = vcat(df_fix, df_rdm)

CSV.write("myapp/out/jwas_sol.csv", df_sol)

# Step 8.2 Make design DF
df_idc_rdm = DataFrame(Matrix(out[2])[:, idx_rdm])
DataFrames.rename!(df_idc_rdm, df_rdm.terms)
df_idc_fix = DataFrame(Matrix(out[2])[:, Not(idx_rdm)])
DataFrames.rename!(df_idc_fix, df_fix.terms)

CSV.write("myapp/out/jwas_Z.csv", df_idc_rdm)
CSV.write("myapp/out/jwas_X.csv", df_idc_fix)

# Step 8.3 LHS and RHS
CSV.write("myapp/out/jwas_LHS.csv", DataFrame(Matrix(out[3])))
CSV.write("myapp/out/jwas_RHS.csv", DataFrame(Matrix(out[4])))

# NOTE
# ids, Ai, inbred = get_info(ped,Ai=true)
# set_random(model, "Animal Dam", Vinv=Ai, names=ids); # set random var
# A=[ids abs.(round.(inv(Matrix(Ai)),digits=2))]
# print(versioninfo())
