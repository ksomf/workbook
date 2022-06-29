
data{
    int<lower=0> N;
    
    vector[N] D_obs;
    vector[N] D_std;
    vector[N] A;
    vector[N] M;
}

parameters{

    vector[N]   D_true;
    real        alpha;
    real        beta_A;
    real        beta_M;
    real        sigma;
}

model{
	vector[N]   mu;
    sigma ~ exponential( 1 );
    
    alpha  ~ normal( 0, 0.2 );
    beta_A ~ normal( 0, 0.5 );
    beta_M ~ normal( 0, 0.5 );
    
    for ( i in 1:N ) {
    	mu[i] = alpha + beta_A*A[i] + beta_M*M[i];
    }
    D_true ~ normal( mu    , sigma );
    D_obs  ~ normal( D_true, D_std );
}

generated quantities{
	vector[N]   mu;
	for ( i in 1:N ) {
    	mu[i] = alpha + beta_A*A[i] + beta_M*M[i];
    }
}