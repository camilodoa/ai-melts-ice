import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, SimpleRNN, GRU
from ai import Learner
from os import listdir
from os.path import isfile, join
import re
from tensorflow.keras.models import load_model
import pickle



class Exelixi():
    '''
    Evolutionary search for finding optimal DL model for ICE raid predictions
    '''
    def __init__(self, size = 10, generations = 50):
        '''
        size: number of individuals
        generations: number of iterations to run
        '''
        # Number of generations that will be produced
        self.generations = generations
        # Current generation
        self.generation = 0
        # Population
        self.population = []
        # Desired population size
        self.capacity = size
        # Tournament size
        self.tournament = 3
        # Mutation probabilities
        self.mutation = self.layer_mutation = 0.3
        self.addition_rate = 0.2
        self.deletion_rate = 0.2
        # Layer possibilities
        self.layer_options = {'Dense': Dense, 'LSTM': LSTM, 'SimpleRNN' : SimpleRNN, 'GRU' : GRU}
        self.activation_functions = ['relu', 'tanh', 'sigmoid', 'softmax']
        # Model parameters
        self.optimizer_options = [
            'Adam', 'SGD', 'RMSprop', 'Adadelta', 'Adagrad', 'Adamax', 'Nadam',
            'Ftrl']
        self.loss_options = [
            'mse', 'mae', 'mape', 'msle', 'cosine_loss', 'huber', 'log_cosh']
        # Lexicase selection
        # Switch between using test loss and train loss in fitness function
        self.fitness_options = ['evaluation']
        self.fitness = random.choice(self.fitness_options)
        # Individual constraints
        self.min_t = 1
        self.max_t = 12
        self.min_split = 0.5
        self.max_split = 0.8
        self.min_epochs = 100
        self.max_epochs = 1000
        self.min_num_layers = 2
        self.max_num_layers = 15
        self.min_neurons = 32
        self.max_neurons = 1000
        # Types of mutations
        self.mutations = {
            't' : self.mutate_t,
            'split' : self.mutate_split,
            'epochs' : self.mutate_epochs,
            'neurons' : self.mutate_neurons,
            'layers' : self.mutate_layers,
            'optimizer' : self.mutate_optimizer,
            'loss' : self.mutate_loss
        }
        # Individual names
        self.names = []
        with open('names.txt','r') as f:
            for line in f:
                for word in line.split():
                   self.names.append(word)


    def individual(self):
        '''
        Makes a new randomized individual
        '''
        # Loop until a viable individual is created
        viable = False
        while viable is False:
            t = random.randint(self.min_t, self.max_t)
            split = random.uniform(self.min_split, self.max_split)
            epochs = random.randint(self.min_epochs, self.max_epochs)
            num_layers = random.randint(self.min_num_layers, self.max_num_layers)
            neurons = random.randint(self.min_neurons, self.max_neurons)
            layers = self.generate_layers(num_layers)
            optimizer = random.choice(self.optimizer_options)
            loss = random.choice(self.loss_options)
            learner = Learner(t = t, split = split, epochs = epochs,
                    neurons = neurons, layers = layers, optimizer = optimizer,
                    loss = loss)
            try:
                learner.fit(type = self.fitness)
                viable = True
            # We're still allowed to cancel the program
            except KeyboardInterrupt:
                raise
            except Exception as e:
                continue
        return learner


    def animate(self, genome):
        '''
        Makes an individual from a genome
        '''
        return Learner(t = genome['t'], split = genome['split'],
                epochs = genome['epochs'], neurons = genome['neurons'],
                layers = genome['layers'], optimizer = genome['optimizer'],
                loss = genome['loss'])

    def name(self, individual):
        '''
        Give a name to an individual
        '''
        return random.choice(self.names) + str(int(individual.error))


    def populate(self, use_previous = False):
        '''
        Create initial population
        '''
        if use_previous:
            individuals = './individuals/'
            models = './models/'
            # Finds file name of the previous individual with lowest error
            previous = min([f for f in listdir(individuals) if isfile(join(individuals, f))], key = lambda x : [[int(s.replace(".", "")) for s in re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", x)]][0])
            # Use the last best model trained
            with open(individuals + previous, 'rb') as input:
                # Load all of genome from individual except for model layers
                ancestor = pickle.load(input)
                # Load model from model folder
                previous_model = load_model(models + previous[:-7] + '.h5')
                # Update ancestor with middle layers (All but input/output)
                ancestor.update({'layers' : previous_model.layers[1:-1]})
                # Add ancestor to population
                self.population.append(self.animate(ancestor))
            # Then generate the rest of the population as normal
            for i in range(self.capacity - 1):
                self.population.append(self.individual())
        else:
            for i in range(self.capacity):
                self.population.append(self.individual())

    def repopulate(self):
        '''
        Make a new generation
        '''
        babies = []
        fittest = self.fittest()
        for i in range(self.capacity - 1):
            babies.append(self.reproduce())
        # Keep best individual from last generation
        babies.append(fittest)
        self.population = babies

    def generate_layers(self, num_layers):
        '''
        Make a list random of DL layers
        '''
        layers = []
        for i in range(num_layers):
            neurons = random.randint(20, 1000)
            layer = random.choice(list(self.layer_options.values()))
            # If the layer is Dense, we get to pick our own activation function
            if layer.__class__.__name__ == 'Dense':
                activation = random.choice(self.activation_functions)
                layers.append(layer(neurons, activation))
            # Otherwise, use the default
            else: layers.append(layer(neurons))
        return layers

    '''
    Mutation functions for parts of the individual's genome
    '''
    def mutate_t(self, t):
        change = random.randint(-2, 2)
        new_t = t + change
        if new_t > self.max_t: return self.max_t
        elif new_t < self.min_t: return self.min_t
        else: return new_t

    def mutate_split(self, split):
        change = random.uniform(-0.2, 0.2)
        new_split = split + change
        if new_split > self.max_split: return self.max_split
        elif new_split < self.min_split: return self.min_split
        else: return new_split

    def mutate_epochs(self, epochs):
        change = random.randint(-200, 200)
        new_epochs = epochs + change
        if new_epochs > self.max_epochs: return self.max_epochs
        elif new_epochs < self.min_epochs: return self.min_epochs
        else: return new_epochs

    def mutate_neurons(self, neurons):
        change = random.randint(-100, 100)
        new_neurons = neurons + change
        if new_neurons > self.max_neurons: return self.max_neurons
        elif new_neurons < self.min_neurons: return self.min_neurons
        else: return new_neurons

    def mutate_layers(self, layers):
        new_layers = []
        # UMAD
        # Addition step
        for layer in layers:
            if random.random() < self.addition_rate:
                new_layer = self.generate_layers(1)[0]
                if random.random() < 0.5:
                    # Add new_layer to genome before original layer
                    new_layers.append(new_layer)
                    new_layers.append(layer)
                else:
                    # Add new_layer to genome after original layer
                    new_layers.append(layer)
                    new_layers.append(new_layer)
            else:
                # Add regular layer
                new_layers.append(layer)

        # Deletion step
        for new_layer in new_layers:
            if random.random() < self.deletion_rate:
                new_layers.remove(new_layer)

        return new_layers

    def mutate_optimizer(self, optimizer):
        return random.choice(self.optimizer_options)

    def mutate_loss(self, loss):
        return random.choice(self.loss_options)

    def mutate(self, genome):
        '''
        Randomly mutate an individual's genome
        '''
        mutated_genome = {}
        for name, chromosome in genome.items():
            # If a mutation occurs in this chromosome
            if random.random() <= self.mutation:
                # Don't mutate layers yet
                if name == 'layers': continue
                # Otherwise, perform appropriate mutation
                else: mutated_chromosome = self.mutations[name](chromosome)
                # Update genome
                mutated_genome.update({name : mutated_chromosome})
            # If no mutation occurs, keep the same chromosome
            else: mutated_genome.update({name : chromosome})
        # Mutate each layer by the same amount
        mutated_genome.update({'layers' : self.mutations['layers'](genome.get('layers'))})
        return mutated_genome

    def crossover(self, i1, i2):
        '''
        Randomly crossover two individuals' genomes
        '''
        new_genome = {}
        i1_genome = i1.genome()
        i2_genome = i2.genome()
        for gene in i1_genome.keys():
            new_genome.update({
                gene : random.choice([i1_genome[gene], i2_genome[gene]])
            })
        return new_genome

    def reproduce(self):
        '''
        Returns a child produced by mutating the result of crossing over two
        parents selected with a tournament.
        The child's fitness is assessed to ensure that it can survive.
        If it can't, another recombination + mutation is attempted.
        A maximum of 5 children are made. If none of them are viable, one of
        the two parents is selected at random.
        '''
        viable = False
        while not viable:
            parent1 = self.select()
            parent2 = self.select()
            # Combine parent genomes and mutate
            offspring_genome = self.mutate(self.crossover(parent1, parent2))
            # Try bringing the baby to life
            try:
                offspring = self.animate(offspring_genome)
                # If the fit fails, that means that the baby is an incorrect
                # configuration
                offspring.fit(type = self.fitness)
                viable = True
                return offspring
            # We're still allowed to cancel the program
            except KeyboardInterrupt:
                raise
            # If the baby isn't viable, try again
            except:
                continue
        # If no offspring were created, return the one with the smallest error
        return min([parent1, parent2], key = lambda parent : parent.fit(type = self.fitness))


    def select(self):
        '''
        Returns best individual selected from population using a tournament
        '''
        return min([random.choice(self.population) for _ in range(self.tournament)], key = lambda indiv : indiv.fit(type = self.fitness))


    def fittest(self):
        '''
        Returns fittest individual in population
        '''
        return min(self.population, key = lambda indiv : indiv.fit(type = self.fitness))


    def report(self):
        '''
        Print generation information
        '''
        fittest = self.fittest()
        print("\nAt generation {0} the best error was {1}.".format(self.generation, fittest.fit(type = self.fitness)))
        fittest.model.summary()
        return fittest

    def save(self):
        '''
        Saves fittest to file
        '''
        fittest = self.fittest()
        name = self.name(fittest)
        fittest.save(name)
        with open('./individuals/{0}.genome'.format(name), 'wb') as output:
            genome = fittest.genome()
            genome.pop('layers') # Remove layers because they can't be serialized
            pickle.dump(genome, output, -1)
        return fittest

    def aetas(self, use_previous = False):
        '''
        Cruxis of the algorithm
        Runs evolution until a target error benchmark is reached
        or until we reach the max number of generations
        '''
        self.populate(use_previous = use_previous)
        fittest = self.report()
        while fittest.fit() > 110 and self.generation <= self.generations:
            self.generation += 1
            self.repopulate()
            fittest = self.report()
            # Random Lexicase selection
            self.fitness = random.choice(self.fitness_options)
        return self.fittest()

if __name__ == '__main__':
    'Usage'
    # Run until we get a good solution or until we reach generation 50s
    world = Exelixi(10, 50)
    fittest = world.aetas(False)
    world.save()

    # test = Exelixi(1, 20)
    # test.populate()
    # test.save()
