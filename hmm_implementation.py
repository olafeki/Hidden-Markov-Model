import math
import numpy as np

def forward_algorithm (obs, P, E, pi):
    T = len(obs)  # Length of the observation sequence
    S = P.shape[0]  # Number of states
    alpha = np.zeros((T, S))  # Forward probabilities matrix

    # Initialize alpha 
    alpha[0, :] = pi * E[:, obs[0]]
    
    # Recursion
    for t in range(1, T):
        for j in range(S):
            alpha[t, j] = np.sum(alpha[t-1, i] * P[i, j] * E[j, obs[t]] for i in range(S))

    return alpha

def backward_algorithm(obs_seq, start_prob, transition_prob, emission_prob):
    num_states = transition_prob.shape[0]
    T = len(obs_seq)

    # Initialize the backward matrix
    beta = np.zeros((num_states, T))

    # Initialize the last column of the backward matrix
    beta[:, T - 1] = 1.0

    # Backward pass
    for t in range(T - 2, -1, -1):
        for i in range(num_states):
            beta[i, t] = np.sum(
                beta[j, t + 1] * transition_prob[i, j] * emission_prob[j, obs_seq[t + 1]]
                for j in range(num_states)
            )

    return beta.T

def update_parameters(alpha,beta,p,e,pi,o,number_steps,number_states):
    #We can now calculate the temporary variables, according to Bayes' theorem:
    # Specify the number of rows and columns
    num_rows = number_steps
    num_columns = number_states

    # Creating an empty matrix with all elements initialized to 0
    gamma = [[0 for _ in range(num_columns)] for _ in range(num_rows)]
    for t in range(number_steps):
        for i in range(number_states):
                try:
                    gamma[t][i]=(alpha[t][i]*beta[t][i])/sum(alpha[t][j] * beta[t][j] for j in range(number_states))
                except:
                    gamma[t][i] = 0.0
    
    # number of states
    num_states = len(alpha[0])

    # Initialize a 3D matrix for epsilon
    epsilon = [[[0.0 for _ in range(num_states)] for _ in range(num_states)] for _ in range(len(o) - 1)]

    # Calculate epsilon for each time step
    for t in range(len(o) - 1):
        denominator = sum(alpha[t][i] * beta[t][i] for i in range(num_states))

        for i in range(num_states):
            for j in range(num_states):
                numerator = alpha[t][i] * p[i][j] * e[j][o[t + 1]] * beta[t + 1][j]
                epsilon[t][i][j] = numerator / denominator
                
    #update transition matrix 
    for i in range(number_states):
        for j in range(number_states):
            numerator = sum(epsilon[t][i][j] for t in range(len(o) - 1))
            denominator = sum(gamma[t][i] for t in range(len(o) - 1))
            p[i][j] = numerator / denominator
    # update emission matrix 
    # Convert V to a list
    V = list(set(o))


    # Update Emission Probabilities (e)
    for j in range(number_states):
        for k in range(len(V)):
            symbol = V[k]
            numerator = sum(gamma[t][j] for t in range(len(o)) if o[t] == symbol)
            denominator = sum(gamma[t][j] for t in range(len(o)))
            e[j][k] = numerator / denominator
            
    #update initial distribution
    for i in range(num_states):
        pi[i] = gamma[0][i]
        
    return p,e,pi

def baum_welch(p, e, pi, o, number_steps, number_states, max_iterations=70, convergence_threshold=1e-5):
    for iteration in range(max_iterations):
        # Forward step
        alpha = forward_algorithm(obs=o, P = np.array(p), E = np.array(e), pi = np.array([pi]))
        alpha = alpha.tolist()

        # Backward step
        beta = backward_algorithm(obs_seq=o, start_prob=np.array([pi]), transition_prob=np.array(p), emission_prob=np.array(e))
        beta = beta.tolist()

        # Parameter update step
        p, e, pi = update_parameters(alpha, beta, p, e, pi, o, number_steps, number_states)

        # Check for convergence using the log-likelihood of the observed sequence
        log_likelihood = sum(math.log(sum(alpha[t][i] * beta[t][i] for i in range(number_states))) for t in range(number_steps))
        
        # Print the log-likelihood at each iteration (optional)
        print(f"Iteration {iteration + 1}, Log-Likelihood: {log_likelihood}")

        # Check for convergence
        if iteration > 0 and abs(log_likelihood - prev_log_likelihood) < convergence_threshold:
            print("Converged!")
            break

        prev_log_likelihood = log_likelihood

    return p, e, pi


def viterbi(p,e,pi,o,number_steps,number_states):
    viterbi1k_list=[]
    for k in range (number_states):
        viterbi1k=pi[k]*e[k][o[0]]
        viterbi1k_list.append(viterbi1k)
        print(viterbi1k_list)
    # Specify the number of rows and columns
    num_rows = number_steps
    num_columns = number_states

    # Creating an empty matrix with all elements initialized to 0
    viterbi = [[0 for _ in range(num_columns)] for _ in range(num_rows)]
    # Updating the first row of the matrix
    viterbi[0] = viterbi1k_list
    for t in range (1,number_steps):
        for j in range(number_states):
            viterbi[t][j]=max(viterbi[t-1][i]*p[i][j]*e[j][o[t]] for i in range (0,number_states))
    
    return viterbi
