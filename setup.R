require(mgcv)
require(MSwM)

dir.create(file.path("./data"))

# Export HMM data
data("energy", package = "MSwM")

write.table(energy,file="./data/energy.csv",sep=",",row.names = F)
