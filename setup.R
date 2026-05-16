require(mgcv)
require(MSwM)
require(gamair)

dir.create(file.path("./data"))

# Export HMM data
data("energy", package = "MSwM")

write.table(energy,file="./data/energy.csv",sep=",",row.names = F)

# Export mackerel data
data("med",package="gamair")
write.table(med,file="./data/mackerel.csv",sep=",",row.names = F)

# And coast
data("coast",package="gamair")
write.table(coast,file="./data/coast.csv",sep=",",row.names = F)
