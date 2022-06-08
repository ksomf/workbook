data{
    int<lower=0> N;
    int<lower=0> N_T;
    int<lower=0> N_B;
    int<lower=0> N_A;
    array[N] int P;
    array[N] int A;
    array[N] int B;
    array[N] int T;
}
parameters{
    array[N_A] vector[N_T] a;
    array[N_B] vector[N_T] b;
    vector[N_A] abar;
    vector[N_B] bbar;
    real<lower=0> tau_A;
    real<lower=0> tau_B;
    vector<lower=0>[N_T] sigma_A;
    vector<lower=0>[N_T] sigma_B;
    corr_matrix[N_T] Rho_A;
    corr_matrix[N_T] Rho_B;
}
model{
    vector[N] p;
    
    Rho_A ~ lkj_corr(N_T);
    Rho_B ~ lkj_corr(N_T);
    sigma_A ~ exponential(1);
    sigma_B ~ exponential(1);
    tau_A ~ exponential(1);
    tau_B ~ exponential(1);
    
    abar ~ normal(0 , tau_A);
    bbar ~ normal(0 , tau_B);
    
    a ~ multi_normal( rep_vector(0,N_T), quad_form_diag(Rho_A, sigma_A));
    b ~ multi_normal( rep_vector(0,N_T), quad_form_diag(Rho_B, sigma_B));

    for ( i in 1:N ) {
        p[i] = abar[A[i]] + a[A[i], T[i]] + bbar[B[i]] + b[B[i], T[i]];
        p[i] = inv_logit(p[i]);
    }
    P ~ bernoulli( p );
}