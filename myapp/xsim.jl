using XSim

chrLength = 1.0
numChr    = 1
numLoci   = 2000
mutRate   = 0.0
locusInt  = chrLength/numLoci
mapPos   = collect(0:locusInt:(chrLength-0.0001))
geneFreq = fill(0.5,numLoci)
build_genome(numChr,chrLength,numLoci,geneFreq,mapPos,mutRate)

popSizeFounder = 2
sires = sampleFounders(popSizeFounder);
dams  = sampleFounders(popSizeFounder);

ngen,popSize = 5,10
sires1,dams1,gen1 = sampleRan(popSize, ngen, sires, dams);

sires1.animalCohort[1].genomePat

nSires,nDams = 2,2
popSize,ngen = 10,5
varRes = 1.0
sire2,dam2,gen2=sampleSel(popSize, nSires, nDams, ngen,sires, dams, varRes);
