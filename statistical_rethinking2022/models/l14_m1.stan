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
    matrix[N_T,N_A] zA;
    matrix[N_T,N_B] zB;
    vector[N_A]     zAbar;
    vector[N_B]     zBbar;

    real<lower=0> tau_A;
    real<lower=0> tau_B;
    vector<lower=0>[N_T] sigma_A;
    vector<lower=0>[N_T] sigma_B;
    
    cholesky_factor_corr[N_T] L_Rho_A;
    cholesky_factor_corr[N_T] L_Rho_B;
}
transformed parameters{
    matrix[N_A,N_T] a;
    matrix[N_B,N_T] b;
    vector[N_A] abar;
    vector[N_B] bbar;
    
    a = (diag_pre_multiply(sigma_A, L_Rho_A) * zA)';
    b = (diag_pre_multiply(sigma_B, L_Rho_B) * zB)';

    abar = zAbar * tau_A;
    bbar = zBbar * tau_B;
}
model{
    vector[N] p;
    
    L_Rho_A ~ lkj_corr_cholesky(N_T);
    L_Rho_B ~ lkj_corr_cholesky(N_T);
    sigma_A ~ exponential(1);
    sigma_B ~ exponential(1);
    tau_A ~ exponential(1);
    tau_B ~ exponential(1);
    
    zAbar ~ normal(0, 1);
    zBbar ~ normal(0, 1);
    to_vector(zA) ~ normal(0, 1);
    to_vector(zB) ~ normal(0, 1);
    
    for ( i in 1:N ) {
        p[i] = abar[A[i]] + a[A[i], T[i]] + bbar[B[i]] + b[B[i], T[i]];
        p[i] = inv_logit(p[i]);
    }
    P ~ bernoulli( p );
}

generated quantities{
    vector[N] log_lik;
    vector[N] p;
    matrix[N_T,N_T] Rho_A;
    matrix[N_T,N_T] Rho_B;
    Rho_A = multiply_lower_tri_self_transpose(L_Rho_A);
    Rho_B = multiply_lower_tri_self_transpose(L_Rho_B);
    for ( i in 1:N ) {
        p[i] = abar[A[i]] + a[A[i], T[i]] + bbar[B[i]] + b[B[i], T[i]];
        p[i] = inv_logit(p[i]);
        log_lik[i] = bernoulli_lpmf( P[i] | p[i] );
    }
}