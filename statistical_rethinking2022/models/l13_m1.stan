data{
	int<lower=0> N;
	int<lower=0> N_T;
	int<lower=0> N_B;
	int<lower=0> N_A;
    int P[N];
    int A[N];
    int B[N];
    int T[N];
}
parameters{
    matrix[N_T,N_B] b;
    vector[N_A] a;
    real abar;
    real<lower=0> sigma_B;
    real<lower=0> sigma_A;
}
model{
    vector[N] p;
    sigma_A ~ exponential( 1 );
    sigma_B ~ exponential( 1 );
    abar ~ normal( 0 , 1.5 );
    a ~ normal( abar , sigma_A );
    to_vector( b ) ~ normal( 0 , 1 );
    for ( i in 1:N ) {
        p[i] = b[T[i], B[i]]*sigma_B + a[A[i]];
        p[i] = inv_logit(p[i]);
    }
    P ~ bernoulli( p );
}