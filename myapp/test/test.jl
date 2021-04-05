using JWAS, DataFrames, CSV, InvertedIndices, Debugger

df_param = CSV.read("myapp/out/param.csv", 
    DataFrame, 
    header=false, 
    delim=",")
phenotypes = CSV.read("myapp/data/customized.ped",
    DataFrame,
    delim=',',
    header=true,
    missingstrings=["NA"])
print(phenotypes)
