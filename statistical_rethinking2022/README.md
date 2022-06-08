# Statistical Rethinking 2022 Workbook

## Installation

```R
install.packages("rstan", repos = "https://cloud.r-project.org/", dependencies = TRUE)
install.packages("cmdstanr", repos = c("https://mc-stan.org/r-packages/", getOption("repos")))
cmdstanr::install_cmdstan()
install.packages(c("coda","mvtnorm","devtools","loo","dagitty","shape"))
devtools::install_github("rmcelreath/rethinking")
```
