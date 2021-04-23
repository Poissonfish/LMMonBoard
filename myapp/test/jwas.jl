# Imports
# import Pkg
Pkg.add(["JWAS", "DataFrames", "CSV", "InvertedIndices"])
using JWAS, DataFrames, CSV, InvertedIndices

# Step 1: Take inputs
df_param = CSV.read("myapp/out/param.csv", DataFrame, header=false, delim=",")
ARG = Dict()
ARG["data"] = df_param[1, 1]
ARG["pedigree"] = df_param[2, 1]
ARG["eq"] = df_param[3, 1]
ARG["cov"] = df_param[4, 1]
ARG["rdmstr"] = df_param[5, 1]
ARG["rdmiid"] = df_param[6, 1]
ARG["vgstr"] = df_param[7, 1]
ARG["vgiid"] = df_param[8, 1]
ARG["vgres"] = df_param[9, 1]

# Step 2: Read data
phenotypes = CSV.read(ARG["data"],
    DataFrame,
    delim=',',
    header=true,
    missingstrings=["NA"])

# Step 2-2: Build Pedigree
ped = get_pedigree(ARG["pedigree"], header=true, separator=",")

id_int = map(x->parse(Int8, x), ped.IDs)
order_ped = sortperm(id_int)

# compute inversed A
Ai = JWAS.PedModule.AInverse(ped)
# from sparse to dense and get A
AiD = Matrix(Ai)
AD = inv(AiD)
CSV.write("myapp/out/jwas_ped.csv", DataFrame(AD)[order_ped, order_ped], header=false)

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
    dt_vu = CSV.read(ARG["vg"], DataFrame)
    set_random(model, ARG["rdmiid"], Matrix(dt_vu)); # set random var
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
df_fix[:, :terms] = replace.(df_fix.terms, "intercept:intercept"=>"*intercept:0") # make it sorted the first
df_fix[:, :terms] = replace.(df_fix.terms, ":"=>"_")
df_fix[:, :effects] = sol[Not(idx_rdm), 2]
df_fix[:, :isFixed] .= 1

df_rdm = DataFrame()
df_rdm[:, :terms] = replace.(sol[idx_rdm, 1], "$name_y:"=>"")
df_rdm[:, :terms] = replace.(df_rdm.terms, ":"=>"_")
df_rdm[:, :effects] = sol[idx_rdm, 2]
df_rdm[:, :isFixed] .= 0
df_sol = vcat(df_fix, df_rdm)

# Step 8.1.2: Get right order
dt_terms = split.(df_sol.terms, '_')
foreach(enumerate([:Y1, :Y2])) do (i, n)
    df_sol[!, n] = getindex.(dt_terms, i)
end
df_sol[!, :Y2] = map(x->parse(Float64, x), df_sol.Y2)
idx_sort_all = sortperm(df_sol, [:isFixed, :Y1, :Y2], rev=(true, false, false))
idx_sort_X = sortperm(df_sol[[x in 1 for x in df_sol[!, :isFixed]] ,:], [:Y1, :Y2])
idx_sort_Z = sortperm(df_sol[[x in 0 for x in df_sol[!, :isFixed]] ,:], [:Y1, :Y2])


CSV.write("myapp/out/jwas_sol.csv", df_sol[idx_sort_all, :])

# Step 8.2 Make design DF
df_idc_rdm = DataFrame(Matrix(out[2])[:, idx_rdm])
if size(df_idc_rdm) != (0, 0)
    DataFrames.rename!(df_idc_rdm, df_rdm.terms)
    CSV.write("myapp/out/jwas_Z.csv", df_idc_rdm[:, idx_sort_Z])
else
    CSV.write("myapp/out/jwas_Z.csv", DataFrame(Empty_Data = []))
end

df_idc_fix = DataFrame(Matrix(out[2])[:, Not(idx_rdm)])
if size(df_idc_fix) != (0, 0)
    DataFrames.rename!(df_idc_fix, df_fix.terms)
    CSV.write("myapp/out/jwas_X.csv", df_idc_fix[:, idx_sort_X])
else
    CSV.write("myapp/out/jwas_X.csv", DataFrame(Empty_Data = []))
end

# Step 8.3 LHS and RHS
CSV.write("myapp/out/jwas_lhs.csv", DataFrame(Matrix(out[3]))[idx_sort_all, idx_sort_all])
CSV.write("myapp/out/jwas_rhs.csv", DataFrame(Matrix(out[4]))[idx_sort_all, :])

# NOTE
# ids, Ai, inbred = get_info(ped,Ai=true)
# set_random(model, "Animal Dam", Vinv=Ai, names=ids); # set random var
# A=[ids abs.(round.(inv(Matrix(Ai)),digits=2))]
# print(versioninfo())
