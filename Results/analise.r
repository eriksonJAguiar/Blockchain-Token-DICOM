
hw1 <- read.csv2("Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/table_hw.csv", sep=";")

hw2 <- read.csv2("Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/table_hw2.csv", sep=";")

hw <- rbind(hw1,hw2)


t  <- (0:309)*10

lt1 <- read.csv2("Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/table_latency.csv", sep=";")
lt2 <- read.csv2("Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/table_latency2.csv", sep=";")

lt <- rbind(lt1,lt2)

png(file = "/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/cpu_usage.png", width = 4, height = 4, units = 'in', res = 300)
plot(t,hw$cpu, type= "l",col = "red", xlab = "Time (s)", ylab = "CPU used (%)", main = "CPU Usage")
dev.off()

png(file = "/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/memory_usage.png", width = 4, height = 4, units = 'in', res = 300)
plot(t,hw$memory, type= "l",col = "red", xlab = "Time (s)", ylab = "Memory used (%)", main = "Memory Usage")
dev.off()

tm<-c()
tm <- c(tm,0)
ltvet <- c(lt$time)

i<-2
aux <- ltvet[1]
while(i <= length(lt$time)){
  val <- aux + ltvet[i+1]
  tm <- c(tm,val)
  aux <- val
  i = i +1
  
}





png(file = "/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/latency.png", width = 4, height = 4, units = 'in', res = 300)
boxplot(c(lt$latftp),c(lt$latapibc),c(lt$latoderer),c(lt$latpeers),c(lt$latcouch),
        main = "Network Latency",
        ylab = "Latency/s",
        names = c("Storage", "API BC", "Orderer", "Peers", "Couchdb"),
        col = "red",
        border = "black",
        notch = TRUE
)

dev.off()

###### statistical metrics ###########

#### CPU #####

mean(c(hw$cpu))
median(c(hw$cpu))
sd(c(hw$cpu))
var(c(hw$cpu))
max(c(hw$cpu))
min(c(hw$cpu))

#### Memory #####

mean(c(hw$memory))
median(c(hw$memory))
sd(c(hw$memory))
var(c(hw$memory))
max(c(hw$memory))
min(c(hw$memory))

#### Latency FTP #####

mean(c(lt$latftp))
median(c(lt$latftp))
sd(c(lt$latftp))
var(c(lt$latftp))
max(c(lt$latftp))
min(c(lt$latftp))

#### Latency API BC #####

mean(c(lt$latapibc))
median(c(lt$latapibc))
sd(c(lt$latapibc))
var(c(lt$latapibc))
max(c(lt$latapibc))
min(c(lt$latapibc))

#### Latency Odererer #####

mean(c(lt$latoderer))
median(c(lt$latoderer))
sd(c(lt$latoderer))
var(c(lt$latoderer))
max(c(lt$latoderer))
min(c(lt$latoderer))

#### Latency Peers #####

mean(c(lt$latpeers))
median(c(lt$latpeers))
sd(c(lt$latpeers))
var(c(lt$latpeers))
max(c(lt$latpeers))
min(c(lt$latpeers))

#### Latency Couchdb #####

mean(c(lt$latcouch))
median(c(lt$latcouch))
sd(c(lt$latcouch))
var(c(lt$latcouch))
max(c(lt$latcouch))
min(c(lt$latcouch))
