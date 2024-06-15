import copy
import gym
import numpy as np
from gym.spaces import Discrete, Box, Tuple, Dict, MultiDiscrete
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import torch
import torch.nn as nn
import torch.nn.functional as F

# Define the network parameters for the final reward function
input_dim = 5  # number of individual rewards
output_dim = 1  # final reward


stats_file_path_base = 'C:\\Users\\djime\\Documents\\PHD\\THESIS\\CODES\\RL_Routing\\Results_EPyMARL\\stats_over_time'
Eelec = 50e-9  # energy consumption per bit in joules
Eamp = 100e-12  # energy consumption per bit per square meter in joules
info_amount = 3072  # data size in bits
initial_energy = 1  # initial energy of each sensor (in joules)
lower_bound = 0  # lower bound of the sensor positions
upper_bound = 100  # upper bound of the sensor positions
base_station_position = np.array([(upper_bound - lower_bound)/2, (upper_bound - lower_bound)/2]) # position of the base station
initial_number_of_packets = 1  # initial number of packets to transmit


# Define the final reward function using an attention mechanism
class Attention(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(Attention, self).__init__()  # Call the initializer of the parent class (nn.Module)
        self.input_dim = input_dim  # Set the input dimension of the network
        self.output_dim = output_dim  # Set the output dimension of the network
        self.linear1 = nn.Linear(input_dim, 64)  # Define the first linear layer. It takes input of size 'input_dim' and outputs size '64'
        self.linear2 = nn.Linear(64, output_dim)  # Define the second linear layer. It takes input of size '64' and outputs size 'output_dim'

    def forward(self, x):
        x = F.relu(self.linear1(x))  # Pass the input through a linear layer and a ReLU activation function
        attention_weights = F.softmax(x, dim=0)  # Apply the softmax function to get the attention weights
        x = attention_weights * x  # Multiply the input by the attention weights
        x = self.linear2(x)  # Pass the result through another linear layer
        return x

# Calculate the reward
net = Attention(input_dim, output_dim)
net = net.double()  # Convert the weights to Double


class WSNRoutingEnv(gym.Env):
    def __init__(self, n_sensors = 20, coverage_radius=50):

        super(WSNRoutingEnv, self).__init__()

        self.n_sensors = n_sensors
        self.n_agents = n_sensors
        self.coverage_radius = coverage_radius
        self.episode_count = 0
        self.scale_displacement = 0.01 * (upper_bound - lower_bound) # scale of the random displacement of the sensors
        self.epsilon = 1e-10 # small value to avoid division by zero

        # Define observation space
        self.observation_space = Tuple(
            tuple([self._get_observation_space() for _ in range(self.n_sensors)])
        )
        self.action_space = Tuple(tuple([Discrete(self.n_sensors + 1)] * self.n_agents))
                
        self.reset()

    def reset(self):

        # Initialize the position of the sensors randomly
        self.sensor_positions = np.random.rand(self.n_sensors, 2) * (upper_bound - lower_bound) + lower_bound
        self.distance_to_base = np.linalg.norm(self.sensor_positions - base_station_position, axis=1)
        # Initialize remaining energy of each sensor to initial_energy joule
        self.remaining_energy = np.ones(self.n_sensors) * initial_energy
        self.consumption_energy = np.zeros(self.n_sensors)
        self.number_of_packets = np.ones(self.n_sensors, dtype=int) * initial_number_of_packets # number of packets to transmit
        self.episode_count += 1
        return self._get_obs()

    def step(self, actions):
        rewards = [0] * self.n_sensors
        dones = [False] * self.n_sensors
        for i, action in enumerate(actions):
            
            if action not in range(self.n_sensors + 1):
                raise ValueError("Invalid action!")
            
            if i >= self.n_sensors:
                continue  # Skip if the number of actions is greater than the number of sensors

            if self.remaining_energy[i] <= 0 or self.number_of_packets[i] <= 0:
                continue  # Skip if sensor has no energy left or no packets to transmit
            
            if (action == i):
                continue  # Skip if sensor tries to transmit data to itself

            if action == self.n_sensors:
                # Calculate the energy consumption and remaining for transmitting data to the base station
                transmission_energy = self.transmission_energy(self.number_of_packets[i], self.distance_to_base[i])
                self.update_sensor_energies(i, transmission_energy) 
                rewards[i] = self.compute_individual_rewards(i, action)
                dones[i] = True       
            else:
                distance = np.linalg.norm(self.sensor_positions[i] - self.sensor_positions[action])
                transmission_energy = self.transmission_energy(self.number_of_packets[i], distance)
                reception_energy = self.reception_energy(self.number_of_packets[i])
                self.update_sensor_energies(i, transmission_energy)  
                self.update_sensor_energies(action, reception_energy)   
                # Compute individual rewards
                rewards[i] = self.compute_individual_rewards(i, action)
                # Update the number of packets
                self.number_of_packets[action] += self.number_of_packets[i]
            self.number_of_packets[i] = 0 # Reset the number of packets of the sensor i
            # Calculate final reward
            # rewards_individual = torch.tensor(rewards[i], dtype=torch.double)                
            # final_reward = net(rewards_individual)
            final_reward = np.sum(rewards[i]) 
            rewards[i] = final_reward

        rewards = [0.5 * r + 0.5 * (1/self.n_sensors) * (self.network_reward_consumption_energy() + self.network_reward_dispersion_remaining_energy()) for r in rewards]

        for i in range(self.n_sensors):
            if (self.remaining_energy[i] <= 0) or (self.number_of_packets[i] <= 0):
                dones[i] = True

        # Integrate the mobility of the sensors
        self.integrate_mobility() 

        self.distance_to_base = np.linalg.norm(self.sensor_positions - base_station_position, axis=1)

        return self._get_obs(), rewards, dones, {}

    def _get_obs(self):
        return [{'remaining_energy': np.array([e]), 
                 'sensor_positions': p,
                 'consumption_energy': np.array([c]),
                 'number_of_packets': np.array([d])} for e, p, c, d in zip(self.remaining_energy, self.sensor_positions, self.consumption_energy, self.number_of_packets)]

    def _get_observation_space(self):
        return Dict({
            'remaining_energy': Box(low=0, high=initial_energy, shape=(1,), dtype=np.float64),
            'sensor_positions': Box(low=lower_bound, high=upper_bound, shape=(2,), dtype=np.float64),
            'consumption_energy': Box(low=0, high=initial_energy, shape=(1,), dtype=np.float64),
            'number_of_packets': Box(low=0, high=self.n_sensors * initial_number_of_packets + 1, shape=(1,), dtype=int)
        })

    def get_state(self):
        return self._get_obs()
    
    def get_avail_actions(self):
        return [list(range(self.n_sensors + 1)) for _ in range(self.n_sensors)]
    
    def update_sensor_energies(self, i, delta_energy):
        self.consumption_energy[i] += delta_energy
        self.remaining_energy[i] -= delta_energy

    def transmission_energy(self, number_of_packets, distance):
        # energy consumption for transmitting data on a distance        
        return number_of_packets * info_amount * (Eelec + Eamp * distance**2)
    
    def reception_energy(self, number_of_packets):
        # energy consumption for receiving data
        return number_of_packets * info_amount * Eelec
    
    def compute_angle_vectors(self, i, action):
        '''
        Compute the angle in radians between the vectors formed by (i, action) and (i, base station)
        '''
        if action == self.n_sensors:
            return 0
        else:
            vector_to_next_hop = self.sensor_positions[action] - self.sensor_positions[i]
            vector_to_base = base_station_position - self.sensor_positions[i]
            cosine_angle = np.dot(vector_to_next_hop, vector_to_base) / (np.linalg.norm(vector_to_next_hop) * np.linalg.norm(vector_to_base))
            
            return np.arccos(np.clip(cosine_angle, -1, 1))

    def compute_reward_angle(self, i, action):
        '''
        Compute the reward based on the angle between the vectors formed by (i, action) and (i, base station)
        '''
        # Calculate the angle in radians between the vectors formed by (i, action) and (i, base station)
        angle = self.compute_angle_vectors(i, action)
        # Normalize the angle
        normalized_angle = abs(angle) / np.pi

        return np.clip(1 - normalized_angle, 0, 1)
    
    def compute_reward_distance(self, i, action):
        '''
        Compute the reward based on the distance to the next hop
        '''
        if action == self.n_sensors:
            distance = np.linalg.norm(self.sensor_positions[i] - base_station_position)
        else:
            distance = np.linalg.norm(self.sensor_positions[i] - self.sensor_positions[action])
        # Normalize the distance to the next hop
        normalized_distance_to_next_hop = distance / self.coverage_radius

        return np.clip(1 - normalized_distance_to_next_hop, 0, 1)

    def compute_reward_consumption_energy(self, i, action):
        '''
        Compute the reward based on the total energy consumption (transmission, reception)
        '''
        # Calculate the total energy consumption (transmission, reception)
        if action == self.n_sensors:
            total_energy = self.transmission_energy(self.number_of_packets[i], self.distance_to_base[i])
        else:
            distance = np.linalg.norm(self.sensor_positions[i] - self.sensor_positions[action])
            transmission_energy = self.transmission_energy(self.number_of_packets[i], distance)
            reception_energy = self.reception_energy(self.number_of_packets[i])
            total_energy = transmission_energy + reception_energy

        # Normalize the total energy consumption
        max_transmission_energy = self.transmission_energy(self.n_sensors * initial_number_of_packets, self.coverage_radius)
        max_reception_energy = self.reception_energy(self.n_sensors * initial_number_of_packets)
        max_total_energy = max_transmission_energy + max_reception_energy
        normalized_total_energy = total_energy / max_total_energy

        return np.clip(1 - normalized_total_energy, 0, 1)
    
    def compute_reward_dispersion_remaining_energy(self):
        '''
        Compute the reward based on the standard deviation of the remaining energy
        '''
        dispersion_remaining_energy = np.std(self.remaining_energy)
        # Normalize the standard deviation of the remaining energy
        max_dispersion_remaining_energy = initial_energy / 2 # maximum standard deviation of the remaining energy if n_sensors is even
        normalized_dispersion_remaining_energy = dispersion_remaining_energy / max_dispersion_remaining_energy

        return np.clip(1 - normalized_dispersion_remaining_energy, 0, 1)
    
    def compute_reward_number_of_packets(self, action):
        '''
        Compute the reward based on the number of packets of the receiver
        '''
        max_number_of_packets = self.n_sensors * initial_number_of_packets
        if action == self.n_sensors:
            normalized_number_of_packets = 0
        else: 
            normalized_number_of_packets = self.number_of_packets[action] / max_number_of_packets

        return np.clip(1 - normalized_number_of_packets, 0, 1)

    def compute_individual_rewards(self, i, action):
        '''
        Compute the individual rewards
        '''
        reward_angle = self.compute_reward_angle(i, action)
        reward_distance = self.compute_reward_distance(i, action)
        reward_consumption_energy = self.compute_reward_consumption_energy(i, action)
        # reward_dispersion_remaining_energy = self.compute_reward_dispersion_remaining_energy()
        reward_number_of_packets = self.compute_reward_number_of_packets(action)

        # return [reward_angle, reward_distance, reward_consumption_energy, reward_dispersion_remaining_energy, reward_number_of_packets]
        return [reward_angle, reward_distance, reward_consumption_energy, reward_number_of_packets]

    def network_reward_dispersion_remaining_energy(self):
        '''
        Compute the reward based on the standard deviation of the remaining energy at the network level
        '''
        dispersion_remaining_energy = np.std(self.remaining_energy)
        # Normalize the standard deviation of the remaining energy
        max_dispersion_remaining_energy = initial_energy / 2 # maximum standard deviation of the remaining energy if n_sensors is even
        normalized_dispersion_remaining_energy = dispersion_remaining_energy / max_dispersion_remaining_energy

        return np.clip(1 - normalized_dispersion_remaining_energy, 0, 1)
    
    def network_reward_consumption_energy(self):
        '''
        Compute the reward based on the total energy consumption (transmission, reception) at the network level
        '''
        total_energy = np.sum(self.consumption_energy)
        # Normalize the total energy consumption
        max_transmission_energy = self.transmission_energy(self.n_sensors * initial_number_of_packets, self.coverage_radius)
        max_reception_energy = self.reception_energy(self.n_sensors * initial_number_of_packets)
        normalized_total_energy = total_energy / (max_transmission_energy + max_reception_energy)

        return np.clip(1 - normalized_total_energy, 0, 1)

    def integrate_mobility(self):
        '''
        Integrate the mobility of the sensors after each step
        '''
        # Add a small random displacement to each sensor's position
        displacement = np.random.normal(scale=self.scale_displacement, size=(self.n_sensors, 2))
        self.sensor_positions += displacement
        # Cancel the displacement if the sensor goes out of bounds
        for i in range(self.n_sensors):
            if not(np.all(self.sensor_positions[i] >= lower_bound) and np.all(self.sensor_positions[i] <= upper_bound)):
                self.sensor_positions[i] -= displacement[i]