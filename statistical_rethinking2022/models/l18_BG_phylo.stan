functions{
	// From Statistical Rethinking
    matrix cov_GPL1(matrix x, real sq_alpha, real sq_rho, real delta) {
        int N = dims(x)[1];
        matrix[N, N] K;
        for (i in 1:(N-1)) {
          K[i, i] = sq_alpha + delta;
          for (j in (i + 1):N) {
            K[i, j] = sq_alpha * exp(-sq_rho * x[i,j] );
            K[j, i] = K[i, j];
          }
        }
        K[N, N] = sq_alpha + delta;
        return K;
    }

    vector merge_missing( int[] miss_indexes , vector x_obs , vector x_miss ) {
        int N = dims(x_obs)[1];
        int N_miss = dims(x_miss)[1];
        vector[N] merged;
        merged = x_obs;
        for ( i in 1:N_miss )
            merged[ miss_indexes[i] ] = x_miss[i];
        return merged;
    }
}

data{
    int<lower=0> N;
    
    vector[N] M;
    int<lower=0> N_M_miss;
    array[N_M_miss] int M_miss_idx;
    
    vector[N] G;
    int<lower=0> N_G_miss;
    array[N_G_miss] int G_miss_idx;
    
    vector[N] B;
    int<lower=0> N_B_miss;
    array[N_B_miss] int B_miss_idx;
    
    matrix[N,N] Dmat;
}

parameters{
	vector[N_M_miss] M_impute;
	vector[N_G_miss] G_impute;
	vector[N_B_miss] B_impute;

	real alpha_B;

	real betaB_G;
	real betaB_M;
	
	real<lower=0> etasqG;
	real<lower=0> rhoG;
	real<lower=0> etasqB;
	real<lower=0> rhoB;
}

model{
	vector[N] mu;
	
	vector[N] M_merge;
	vector[N] G_merge;
	vector[N] B_merge;
	
	matrix[N,N] K_G;
	matrix[N,N] K_B;
	
	rhoG   ~ normal( 1, 0.25 );
	etasqG ~ normal( 3, 0.25 );
	rhoB   ~ normal( 1, 0.25 );
	etasqB ~ normal( 3, 0.25 );
	
	K_G = cov_GPL1(Dmat, etasqG, rhoG, 0.01);
	K_B = cov_GPL1(Dmat, etasqB, rhoB, 0.01);
    
    betaB_G ~ normal( 0, 0.5 );
    betaB_M ~ normal( 0, 0.5 );
    
    alpha_B ~ normal( 0, 1 );
    
    M_merge = merge_missing(M_miss_idx, to_vector(M), M_impute);
    G_merge = merge_missing(G_miss_idx, to_vector(G), G_impute);
    B_merge = merge_missing(B_miss_idx, to_vector(B), B_impute);
    
    for ( i in 1:N ) {
    	mu[i] = alpha_B + betaB_G*G_merge[i] + betaB_M*M_merge[i];
    }
    
    M_merge ~ normal(0,1);    
    G_merge ~ multi_normal(rep_vector(0,N), K_G);
    B_merge ~ multi_normal(mu             , K_B);
}