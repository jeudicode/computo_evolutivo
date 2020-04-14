library(ggplot2)

res_1 <- read.csv(file="~/unam/2020-II/computo_evolutivo/tareas/tarea3/res_pso_1_1.csv")
res_2 <- read.csv(file="~/unam/2020-II/computo_evolutivo/tareas/tarea3/res_pso_1_2.csv")
res_3 <- read.csv(file="~/unam/2020-II/computo_evolutivo/tareas/tarea3/res_pso_1_3.csv")
res_4 <- read.csv(file="~/unam/2020-II/computo_evolutivo/tareas/tarea3/res_pso_1_4.csv")
res_5 <- read.csv(file="~/unam/2020-II/computo_evolutivo/tareas/tarea3/res_pso_1_5.csv")
res_6 <- read.csv(file="~/unam/2020-II/computo_evolutivo/tareas/tarea3/res_pso_1_6.csv")
res_7 <- read.csv(file="~/unam/2020-II/computo_evolutivo/tareas/tarea3/res_pso_1_7.csv")
res_8 <- read.csv(file="~/unam/2020-II/computo_evolutivo/tareas/tarea3/res_pso_1_8.csv")
res_9 <- read.csv(file="~/unam/2020-II/computo_evolutivo/tareas/tarea3/res_pso_1_9.csv")
res_10 <- read.csv(file="~/unam/2020-II/computo_evolutivo/tareas/tarea3/res_pso_1_10.csv")

p <- res_1$eval
q1 = var(p) #sd(p)*(sqrt((length(p)-1)/length(p)))
s1 = sd(p)
q1
s1
t1 = sum(p)
t1
p <- res_2$eval
q2 = var(p) #sd(p)*(sqrt((length(p)-1)/length(p)))
s2 = sd(p)
q2
s2
t2 = sum(p)
t2
p <- res_3$eval
q3 = var(p) #sd(p)*(sqrt((length(p)-1)/length(p)))
q3
s3 = sd(p)
s3
t3 = sum(p)
t3
p <- res_4$eval
q4 = var(p) #sd(p)*(sqrt((length(p)-1)/length(p)))
q4
s4 = sd(p)
s4
t4 = sum(p)
t4
p <- res_5$eval
q5 = var(p) #sd(p)*(sqrt((length(p)-1)/length(p)))
q5
s5 = sd(p)
s5
t5 = sum(p)
t5
p <- res_6$eval
q6 = var(p) #sd(p)*(sqrt((length(p)-1)/length(p)))
q6
s6 = sd(p)
s6
t6 = sum(p)
t6
p <- res_7$eval
q7 = var(p) #sd(p)*(sqrt((length(p)-1)/length(p)))
q7
s7 = sd(p)
s7
t7 = sum(p)
t7
p <- res_8$eval
q8 = var(p) #sd(p)*(sqrt((length(p)-1)/length(p)))
q8
s8 = sd(p)
s8
t8 = sum(p)
t8
p <- res_9$eval
q9 = var(p) #sd(p)*(sqrt((length(p)-1)/length(p)))
q9
s9 = sd(p)
s9
t9 = sum(p)
t9
p <- res_10$eval
q10 = var(p) #sd(p)*(sqrt((length(p)-1)/length(p)))
q10
s10 = sd(p)
s10
t10 = sum(p)
t10

a = sum(t1,t2,t3,t4,t5,t6,t7,t8,t9,t10)
a = a / 10
a
r = sum(q1,q2,q3,q4,q5,q6,q7,q8,q9,q10)
r = r / 10
r
r = sqrt(r)
r

p <- ggplot() + 
  geom_line(data = res_1, aes(x = 1:501, y = res_1$eval), color = "red") +
  geom_line(data = res_2, aes(x = 1:501, y = res_2$eval), color = "blue") +
  geom_line(data = res_3, aes(x = 1:501, y = res_3$eval), color = "orange") +
  geom_line(data = res_4, aes(x = 1:501, y = res_4$eval), color = "#5b8a06") +
  geom_line(data = res_5, aes(x = 1:501, y = res_5$eval), color = "violet") +
  geom_line(data = res_6, aes(x = 1:501, y = res_6$eval), color = "#26a7de") +
  geom_line(data = res_7, aes(x = 1:501, y = res_7$eval), color = "#97a160") +
  geom_line(data = res_8, aes(x = 1:501, y = res_8$eval), color = "#917f50") +
  geom_line(data = res_9, aes(x = 1:501, y = res_9$eval), color = "#db748b") +
  geom_line(data = res_10, aes(x = 1:501, y = res_10$eval), color = "#8c73d9") +
  xlab('times') +
  ylab('eval')

p + theme_bw()