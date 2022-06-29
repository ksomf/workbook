data{
    int<lower=0> N;
    
    vector[N] D_obs;
    vector[N] D_std;
    vector[N] A;
    vector[N] M_obs;
    vector[N] M_std;
}

parameters{
    vector[N]   D_true;
    vector[N]   M_true;
    real        alpha_D;
    real        alpha_M;
    real        betaD_A;
    real        betaD_M;
    real        betaM_A;
    real        sigma;
    real        tau;
}

model{
	vector[N]   mu;
	vector[N]   nu;
	
    sigma ~ exponential( 1 );
    tau   ~ exponential( 1 );
    
    alpha_D ~ normal( 0, 0.2 );
    alpha_M ~ normal( 0, 0.2 );
    betaD_A ~ normal( 0, 0.5 );
    betaD_M ~ normal( 0, 0.5 );
    betaM_A ~ normal( 0, 0.5 );
    
    for ( i in 1:N ) {
    	nu[i] = alpha_M + betaM_A*A[i];
    }
    M_true ~ normal( nu    , tau   );
    M_obs  ~ normal( M_true, M_std );
    
    for ( i in 1:N ) {
    	mu[i] = alpha_D + betaD_A*A[i] + betaD_M*M_true[i];
    }
    D_true ~ normal( mu    , sigma );
    D_obs  ~ normal( D_true, D_std );
}

generated quantities{
	vector[N] mu;
	vector[N] nu;
	for ( i in 1:N ) {
    	mu[i] = alpha_D + betaD_A*A[i] + betaD_M*M_true[i];
    	nu[i] = alpha_M + betaM_A*A[i];
    }
}
