import numpy as np

class ParticleFilter:
    """Bootstrap particle filter based on sequential importance resampling."""

    def __init__(self, state_func, state_noise_var, meas_func, meas_noise_var, num_particles=200, shape=(2,)):
        self.particles = np.zeros((num_particles, *shape))
        self.weights = np.ones(num_particles) / num_particles
        self.num_particles = num_particles
        self.state_tran_func = state_func
        self.state_noise_var = state_noise_var
        self.meas_func = meas_func
        self.meas_noise_var = meas_noise_var

    def init_prior_particles(self, *ranges):
        for i,limits in enumerate(ranges):
            self.particles[:,i] = np.random.random(self.num_particles)*(limits[1]-limits[0]) + limits[0]

    def expected_value(self):
        return np.mean(self.particles * self.weights[:,np.newaxis], axis=0)

    def update(self, meas):
        # do state update
        # sampling from importance distribution that is the transition function
        next_particles = self.state_tran_func(self.particles) + np.random.randn(*self.particles.shape)*np.sqrt(self.state_noise_var)

        # calculate the new weights based on measurements
        expected = self.meas_func(next_particles)
        expected[np.where(expected == np.inf)] = 0.0
        meas[np.where(meas == np.inf)] = 0.0
        for i,p in enumerate(next_particles):
            self.weights[i] = np.sum(1 / np.sqrt(2*self.meas_noise_var*np.pi) * \
                np.exp(-(expected[i] - meas)**2/(2*self.meas_noise_var))) * self.weights[i]
            
        # normalize the weights
        self.weights = self.weights / np.sum(self.weights)

        # resample
        resampled = np.zeros(next_particles.shape)
        for i in range(self.weights.shape[0]):
            eps = np.random.random()
            cumulative = 0.0
            for j in range(self.weights.shape[0]):
                cumulative += self.weights[j]
                if eps < cumulative:
                    resampled[i] = next_particles[j]
                    break
                
        self.weights = np.ones(self.weights.shape) / self.weights.shape[0]
        self.particles = resampled