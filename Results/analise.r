
hw1 <- read.csv2("Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/table_hw.csv", sep=";")

hw2 <- read.csv2("Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/table_hw2.csv", sep=";")


hw <- rbind(hw1,hw2)


t  <- (0:309)*10

lt1 <- read.csv2("Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/table_latency.csv", sep=";")
lt2 <- read.csv2("Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/table_latency2.csv", sep=";")

lt <- rbind(lt1,lt2)

png(file = "/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/cpu_usage_pt.png", width = 4, height = 4, units = 'in', res = 300)
plot(t,hw$cpu, type= "l",col = "red", xlab = "Tempo (s)", ylab = "Uso de CPU (%)", main = "Uso de CPU")
dev.off()

png(file = "/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/memory_usage_pt.png", width = 4, height = 4, units = 'in', res = 300)
plot(t,hw$memory, type= "l",col = "red", xlab = "Tempo (s)", ylab = "Uso de memória (%)", main = "Uso de memória")
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




png(file = "/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/latency_pt.png", width = 3, height = 3, units = 'in', res = 200)
boxplot(c(lt$latftp),c(lt$latapibc),c(lt$latoderer),c(lt$latpeers),c(lt$latcouch),
        main = "Latência da rede",
        ylab = "Latência/s",
        col = "red",
        border = "black",
        notch = TRUE,
        names = c("Armaz.", "API BC", "Ord.", "Nós", "Couchdb")
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


#### Hash similarity #####

mean(simLev)
median(simLev)
sd(simLev)
var(simLev)
max(simLev)
min(simLev)


#### Hash Entropy #####

mean(enpy)
median(enpy)
sd(enpy)
var(enpy)
max(enpy)
min(enpy)

### Hahs analysis ######

sim <- as.integer(readLines('/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/sim.txt'))
simLev <- as.integer(readLines('/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/sim_lev.txt'))
algin <- as.integer(readLines('/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/sim_align.txt'))
enpy <- as.double(readLines('/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/entropy.txt'))

normalize <- function(x) {
  return ((x - min(x)) / (max(x) - min(x)))
}

normEnpy <- normalize(enpy)

denpoison <- dpois(enpy,2)
denormal <- dnorm(enpy,log = TRUE)
dbionmial <- dnbinom(enpy,size = length(enpy),prob = 0.2,log = TRUE)
dchiquad <- dchisq(enpy,1)
densim <- density(enpy, kernel = "gaussian");
plot(enpy, main = "Density Similarity")



distEntropy <- rnorm(enpy, mean=mean(enpy), sd=sd(enpy)) 
d <- pnorm(normEnpy)
g <- rgamma(normEnpy, scale = var(normEnpy), shape = max(normEnpy))
ex <- rexp(normEnpy)
qqr <- pchisq(normEnpy, 1, ncp = 0, lower.tail = TRUE, log.p = FALSE)

png(file = "/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/pdf_entropy.png", width = 4, height = 4, units = 'in', res = 300)
plot(density(d), ylab="Density", xlab="Entropy", main = "PDF of tokens entropy",col="red")
dev.off()

png(file = "/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/cdf_entropy.png", width = 5, height = 4, units = 'in', res = 300)
plot(ecdf(normEnpy), ylab="Density",xlab="Entropy",main="CDF of tokens entropy",verticals = FALSE, col="red", do.points=FALSE)
plot(ecdf(d), verticals=TRUE, do.points=FALSE, add=TRUE, col='blue')  
plot(ecdf(g), verticals=TRUE, do.points=FALSE, add=TRUE, col='orange')
plot(ecdf(qqr), verticals=TRUE, do.points=FALSE, add=TRUE, col='green')
legend("bottomright", 
       legend = c("Entropy", "Normal","Gamma","Chi-Square"), 
       col = c("red","blue","orange","green"), 
       pch = c(6,15,18,8), 
       bty = "n", 
       pt.cex = 1, 
       cex = 1, 
       text.col = "black", 
       horiz = F , 
       inset = c(0, 0.1))
dev.off()

c <- acf(d)

png(file = "/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/acf_entropy.png", width = 4, height = 4, units = 'in', res = 300)
plot(c, type="o", main="Autocorrelation values", xlab = "Time (s)", col="red")
dev.off()


############## Analise var Similairty


normSim <- normalize(simLev)

denpoison <- dpois(simLev,2)
denormal <- dnorm(simLev,log = TRUE)
dbionmial <- dnbinom(simLev,size = length(simLev),prob = 0.2,log = TRUE)
dchiquad <- dchisq(simLev,1)
densim <- density(simLev, kernel = "gaussian");
plot(simLev, main = "Density Similarity")



distEntropy <- rnorm(simLev, mean=mean(simLev), sd=sd(simLev)) 
d <- pnorm(normSim)
g <- rgamma(normSim, scale = var(normSim), shape = max(normSim))
ex <- rexp(normSim)
qqr <- pchisq(normSim, 1, ncp = 0, lower.tail = TRUE, log.p = FALSE)

png(file = "/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/pdf_sim.png", width = 4, height = 4, units = 'in', res = 300)
plot(density(d), ylab="Density", xlab="Similarity", main = "PDF of tokens similarity",col="red")
dev.off()

png(file = "/Users/erjulioaguiar/Documents/healh-blockchain/Blockchain_DICOM_CBMS20/Results/cdf_sim.png", width = 5, height = 4, units = 'in', res = 300)
plot(ecdf(normSim), ylab="Density",xlab="Similarity",main="CDF of tokens similarity",verticals = FALSE, col="red", do.points=FALSE)
plot(ecdf(d), verticals=TRUE, do.points=FALSE, add=TRUE, col='blue')  
plot(ecdf(g), verticals=TRUE, do.points=FALSE, add=TRUE, col='orange')
plot(ecdf(qqr), verticals=TRUE, do.points=FALSE, add=TRUE, col='green')
legend("bottomleft", 
       legend = c("Entropy", "Normal","Gamma","Chi-Square"), 
       col = c("red","blue","orange","green"), 
       pch = c(6,15,18,8), 
       bty = "n", 
       pt.cex = 1, 
       cex = 1, 
       text.col = "black", 
       horiz = F , 
       inset = c(0.15, 0.1))
dev.off()






