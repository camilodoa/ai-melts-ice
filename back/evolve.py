from ai import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, SimpleRNN, GRU
from tensorflow.keras.models import load_model
import re
import pickle
import random
from os import listdir
from os.path import isfile, join
from progress.bar import Bar

class AutomaticModelEvolution():
    '''
    Automatic Model Evolution:
    Evolutionary search for finding optimal DL model
    '''
    # Constructor ##############################################################
    def __init__(self, size = 10, generations = 50, ancestor = False,
        target = 110, verbose = 0):
        '''
        Constructor
        Arguments:
            size: number of individuals
            generations: number of iterations to run
            ancestor: whether to add previous minima to population
            target: target error on testing
        Initializes field variables
        '''
        # Population attributes
        # Whether to print out information to terminal
        self.verbose = verbose
        # Target error
        self.target = target
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
        # How many children every parent has
        self.natality = 2
        # Whether we are incorporating an ancestor into the population
        self.ancestor = ancestor
        # Genome attributes
        # Mutation probabilities
        self.mutation = 0.3
        self.addition_rate = 0.2
        self.deletion_rate = 0.2
        # Layer possibilities
        self.layer_options = {'Dense': Dense, 'LSTM': LSTM,
            'SimpleRNN' : SimpleRNN, 'GRU' : GRU}
        self.activation_functions = ['relu', 'tanh', 'sigmoid', 'softmax']
        # Model parameters
        self.optimizer_options = ['Adam', 'SGD', 'RMSprop', 'Adadelta',
            'Adagrad', 'Adamax', 'Nadam', 'Ftrl']
        self.loss_options = ['mse']
        self.fitness = 'loss'
        # DNA constraints
        self.min_t = 6
        self.max_t = 12
        self.min_split = 0.7
        self.max_split = 0.8
        self.min_epochs = 100
        self.max_epochs = 1500
        self.min_num_layers = 0
        self.max_num_layers = 15
        self.min_neurons = 32
        self.max_neurons = 1000
        # Types of mutations
        self.mutations = { 't' : self.delta_t, 'split' : self.delta_split,
            'epochs' : self.delta_epochs, 'neurons' : self.delta_neurons,
            'layers' : self.delta_layers, 'optimizer' : self.delta_optimizer,
            'loss' : self.delta_loss }
        # Individual names
        self.names = []
        with open('names.txt','r') as f:
            for line in f:
                for word in line.split():
                   self.names.append(word)

    # Individal creation and mutation ##########################################
    def individual(self):
        '''
        Makes a new randomized individual
        '''
        # Loop until a viable individual is created
        viable = False
        while not viable:
            learner = Model(t = random.randint(self.min_t, self.max_t),
                split = random.uniform(self.min_split, self.max_split),
                epochs = random.randint(self.min_epochs, self.max_epochs),
                neurons = random.randint(self.min_neurons, self.max_neurons),
                layers = self.generate_layers(random.randint(self.min_num_layers, self.max_num_layers)),
                optimizer = random.choice(self.optimizer_options),
                loss = random.choice(self.loss_options),
                verbose = self.verbose)
            try:
                learner.fit(type = self.fitness)
                viable = True
            except KeyboardInterrupt:
                raise
            except Exception as e:
                continue
        return learner

    def animate(self, genome):
        '''
        Makes an individual from a genome
        '''
        return Model(t = genome['t'], split = genome['split'],
                epochs = genome['epochs'], neurons = genome['neurons'],
                layers = genome['layers'], optimizer = genome['optimizer'],
                loss = genome['loss'], verbose = self.verbose)

    def name(self, individual):
        '''
        Give a name to an individual
        '''
        return random.choice(self.names) + str(int(individual.error))

    # Mutation #################################################################
    def mutate(self, genome):
        '''
        Randomly mutate an individual's genome
        '''
        mutated_genome = {}
        for name, chromosome in genome.items():
            # If a mutation occurs in this chromosome
            if random.random() < self.mutation:
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
        for gene in i1.get_genome().keys():
            new_genome.update({gene : random.choice([i1.get_genome()[gene], i2.get_genome()[gene]])})
        return new_genome

    def reproduce(self):
        '''
        Returns a child produced by mutating the result of crossing over two
        parents selected with a tournament.
        self.natality children are made, and the best of them survives for
        the next generation
        '''
        children = []
        for _ in range(self.natality):
            viable = False
            while not viable:
                try:
                    parent1 = self.select()
                    parent2 = self.select()
                    # Combine parent genomes and mutate
                    offspring = self.animate(self.mutate(self.crossover(parent1, parent2)))
                    # If the fit fails, that means that the baby is an incorrect
                    # configuration
                    offspring.fit(type = self.fitness)
                    viable = True
                    children.append(offspring)
                # We're still allowed to cancel the program
                except KeyboardInterrupt:
                    raise
                # If the baby isn't viable, try again
                except Exception as e:
                    if self.verbose: print("In reproduce", e)
                    continue
        # Return the offspring with the smallest error
        return min(children, key = lambda child : child.fit(type = self.fitness))

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

    def delta_t(self, t):
        change = random.randint(-2, 2)
        new_t = t + change
        if new_t > self.max_t: return self.max_t
        elif new_t < self.min_t: return self.min_t
        else: return new_t

    def delta_split(self, split):
        change = random.uniform(-0.2, 0.2)
        new_split = split + change
        if new_split > self.max_split: return self.max_split
        elif new_split < self.min_split: return self.min_split
        else: return new_split

    def delta_epochs(self, epochs):
        change = random.randint(-200, 200)
        new_epochs = epochs + change
        if new_epochs > self.max_epochs: return self.max_epochs
        elif new_epochs < self.min_epochs: return self.min_epochs
        else: return new_epochs

    def delta_neurons(self, neurons):
        change = random.randint(-100, 100)
        new_neurons = neurons + change
        if new_neurons > self.max_neurons: return self.max_neurons
        elif new_neurons < self.min_neurons: return self.min_neurons
        else: return new_neurons

    def delta_layers(self, layers):
        # UMAD
        new_layers = []
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

    def delta_optimizer(self, optimizer):
        return random.choice(self.optimizer_options)

    def delta_loss(self, loss):
        return random.choice(self.loss_options)

    # Population ###############################################################
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

    def get_ancestor(self):
        individuals = './individuals/'
        models = './models/'
        # Finds file name of the previous individual with lowest error
        previous = min(
            [f for f in listdir(individuals) if isfile(join(individuals, f))],
            key = lambda x : [int(s.replace(".", "")) for s in re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", x)][0])
        # Use the last best model trained
        with open(individuals + previous, 'rb') as input:
            if self.verbose: print("Loading", individuals + previous)
            # Load all of genome from individual except for model layers
            ancestor = pickle.load(input)
            # Load model from model folder
            previous_model = load_model(models + previous[:-7] + '.h5')
            # Update ancestor with middle layers (All but input/output)
            ancestor.update({'layers' : previous_model.layers[1:-1]})
        return ancestor

    def populate(self):
        '''
        Create initial population
        '''
        bar = Bar('Initializing population',  fill='=', max=self.capacity)
        # Add best previously found individual
        if self.ancestor:
            # Add ancestor to population
            self.population.append(self.animate(self.get_ancestor()))
            bar.next()
            # Rest of the population are working mutations of the ancestor
            for _ in range(self.capacity - 1):
                viable = False
                while not viable:
                    try:
                        # Initialize by mutating ancestor
                        descendant = self.animate(self.mutate(self.get_ancestor()))
                        # If the fit fails, that means that the descendant is an incorrect
                        # configuration
                        descendant.fit(type = self.fitness)
                        viable = True
                        self.population.append(descendant)
                    # We're still allowed to cancel the program
                    except KeyboardInterrupt:
                        raise
                    # If the baby isn't viable, try again
                    except Exception as e:
                        if self.verbose: print("In reproduce", e)
                        continue
                bar.next()
            bar.finish()

        # Initialize as normal
        else:
            for _ in range(self.capacity):
                self.population.append(self.individual())
                bar.next()
            bar.finish()
        return self.population

    def repopulate(self):
        '''
        Make a new generation
        '''
        babies = []
        bar = Bar('Creating generation {0}'.format(self.generation), fill='=', max = self.capacity)
        fittest = self.fittest()
        # Keep best individual from last generation
        babies.append(fittest)
        bar.next()
        for i in range(self.capacity - 1):
            babies.append(self.reproduce())
            bar.next()
        bar.finish()
        self.population = babies

    # I/O ######################################################################
    def report(self):
        '''
        Print generation information
        '''
        fittest = self.fittest()
        print("At generation {0} the best error was {1}".format(self.generation,
            fittest.fit(type = self.fitness)))
        if self.verbose: fittest.model.summary()
        print('\n')
        return fittest

    def save(self):
        '''
        Saves fittest to file
        '''
        fittest = self.fittest()
        fittest.save(self.name(fittest))
        return fittest

    # Main #####################################################################
    def run(self):
        '''
        Cruxis of the algorithm
        Runs evolution until a target error benchmark is reached
        or until we reach the max number of generations
        '''
        print("Starting evolution", "from scratch" if not self.ancestor else "with ancestor")
        self.populate()
        fittest = self.report()
        while fittest.fit() > self.target and self.generation <= self.generations:
            self.generation += 1
            self.repopulate()
            fittest = self.report()
        return self.fittest()

    def predict(self, month, year):
        '''
        Generate time series data up until month/year
        '''
        ancestor = self.animate(self.get_ancestor())
        ancestor.predict(month, year)

if __name__ == '__main__':
    'Usage'
    # Run until we get a good solution or until we reach generation 15
    # Or get an error on testing that is less than 1
    world = AutomaticModelEvolution(size = 5, generations = 15, ancestor = False,
        target = 90, verbose=0)
    world.run()
    world.save()
