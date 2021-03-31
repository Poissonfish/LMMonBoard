# Imports
import Pkg
Pkg.add(["JWAS", "DataFrames", "CSV", "InvertedIndices"])
using JWAS, DataFrames, CSV, InvertedIndices

# Step 1: Take inputs
df_param = CSV.read("myapp/out/param.csv", DataFrame, header=false, delim=",")
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

# Step 2-2: Build Pedigree
ped = get_pedigree(ARG["ped"], header=true)

# compute inversed A
Ai = JWAS.PedModule.AInverse(ped)
# from sparse to dense and get A
AiD = Matrix(Ai)
AD = inv(AiD)
CSV.write("myapp/out/jwas_ped.csv", DataFrame(AD), header=false)

# Step 3: Build Model Equationcovs
model = build_model(ARG["eq"], ARG["ve"]); # set residual var, 
# n-trait model
# (model1; model2, nxn matrix)


# Step 4: Set Factors or Covariates
if !(ARG["cov"] === missing)
    set_covariate(model, ARG["cov"]);
end

# Step 5: Set Random or Fixed Effects
if !(ARG["rdmstr"] === missing)
    set_random(model, ARG["rdmstr"], ped); # set random var (ped, matrix V)
end
if !(ARG["rdmiid"] === missing)
    set_random(model, ARG["rdmiid"], ARG["vu"]); # set random var
end

# Step 6: Solve Mixed Model Equations
sol = solve(model, phenotypes, solver="Gibbs");
out = solve(model, phenotypes);

# Step 7: Organize outputs
# get response variables
ls_terms = split(ARG["eq"], r"\s*=\s*")
name_y = ls_terms[1]

# get random index 
ls_rdm = String[]
if !(ARG["rdmstr"] === missing)
    ls_rdm = vcat(ls_rdm, split(ARG["rdmstr"], r"\s"))
end
if !(ARG["rdmiid"] === missing)
    ls_rdmiid = vcat(ls_rdm, split(ARG["rdmiid"], r"\s"))
end

idx_rdm = Int8[]
for rdm in ls_rdm
    idx = findall(x -> occursin(rdm, x), sol[:, 1])
    append!(idx_rdm, idx)
end

# Step 8.1 Make solution DF
df_fix = DataFrame()
df_fix[:, :terms] = replace.(sol[Not(idx_rdm), 1], "$name_y:"=>"")
df_fix[:, :terms] = replace.(df_fix.terms, "intercept:"=>"")
df_fix[:, :terms] = replace.(df_fix.terms, ":"=>"_")
df_fix[:, :effects] = sol[Not(idx_rdm), 2]
df_fix[:, :isFixed] .= 1

df_rdm = DataFrame()
df_rdm[:, :terms] = replace.(sol[idx_rdm, 1], "$name_y:"=>"")
df_rdm[:, :terms] = replace.(df_rdm.terms, ":"=>"_")
df_rdm[:, :effects] = sol[idx_rdm, 2]
df_rdm[:, :isFixed] .= 0
df_sol = vcat(df_fix, df_rdm)

CSV.write("myapp/out/jwas_sol.csv", df_sol)

# Step 8.2 Make design DF
df_idc_rdm = DataFrame(Matrix(out[2])[:, idx_rdm])
if size(df_idc_rdm) != (0, 0)
    DataFrames.rename!(df_idc_rdm, df_rdm.terms)
    CSV.write("myapp/out/jwas_Z.csv", df_idc_rdm)
else
    CSV.write("myapp/out/jwas_Z.csv", DataFrame(Empty_Data = 0))
end

df_idc_fix = DataFrame(Matrix(out[2])[:, Not(idx_rdm)])
if size(df_idc_fix) != (0, 0)
    DataFrames.rename!(df_idc_fix, df_fix.terms)
    CSV.write("myapp/out/jwas_X.csv", df_idc_fix)
else
    CSV.write("myapp/out/jwas_X.csv", DataFrame(Empty_Data = []))
end

# Step 8.3 LHS and RHS
CSV.write("myapp/out/jwas_LHS.csv", DataFrame(Matrix(out[3])))
CSV.write("myapp/out/jwas_RHS.csv", DataFrame(Matrix(out[4])))

# NOTE
# ids, Ai, inbred = get_info(ped,Ai=true)
# set_random(model, "Animal Dam", Vinv=Ai, names=ids); # set random var
# A=[ids abs.(round.(inv(Matrix(Ai)),digits=2))]
# print(versioninfo())
