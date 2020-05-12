import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from ai import Learner

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
        # Number of babies parents try to have
        self.natality = 5
        # Tournament size
        self.tournament = 3
        # Mutation probabilities
        self.mutation = 0.1
        self.layer_mutation = 0.2
        # Layer possibilities
        self.layer_options = {'Dense': Dense, 'LSTM': LSTM}
        self.activation_functions = [
            'relu', 'tanh', 'sigmoid', 'softmax']
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
        self.max_num_layers = 10
        self.min_neurons = 32
        self.max_neurons = 700
        # Types of mutations
        self.mutations = {
            't' : self.mutate_t,
            'split' : self.mutate_split,
            'epochs' : self.mutate_epochs,
            'num_layers' : self.mutate_num_layers,
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
                    num_layers = num_layers, neurons = neurons,
                    layers = layers, optimizer = optimizer, loss = loss)
            try:
                learner.fit(type = self.fitness)
                viable = True
            except Exception as e:
                continue
        return learner


    def animate(self, genome):
        '''
        Makes an individual from a genome
        '''
        return Learner(t = genome['t'], split = genome['split'],
                epochs = genome['epochs'], num_layers = genome['num_layers'],
                neurons = genome['neurons'], layers = genome['layers'],
                optimizer = genome['optimizer'], loss = genome['loss'])

    def name(self, individual):
        '''
        Give a name to an individual
        '''
        return random.choice(self.names) + str(individual.fitness)


    def populate(self):
        '''
        Create initial population
        '''
        for i in range(self.capacity):
            self.population.append(self.individual())

    def repopulate(self):
        '''
        Make a new generation
        '''
        babies = []
        for i in range(self.capacity - 1):
            babies.append(self.reproduce())
        # Keep best individual
        babies.append(self.fittest())
        self.population = babies

    def generate_layers(self, num_layers):
        '''
        Make a list of DL layers
        '''
        layers = []
        for i in range(num_layers):
            neurons = random.randint(20, 700)
            layer = random.choice(list(self.layer_options.values()))
            activation = random.choice(self.activation_functions)
            layers.append(layer(neurons, activation))
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

    def mutate_num_layers(self, num_layers):
        change = random.randint(-1, 1)
        new_num_layers = num_layers + change
        if new_num_layers > self.max_num_layers: return self.max_num_layers
        elif new_num_layers < self.min_num_layers: return self.min_num_layers
        else: return new_num_layers

    def mutate_neurons(self, neurons):
        change = random.randint(-100, 100)
        new_neurons = neurons + change
        if new_neurons > self.max_neurons: return self.max_neurons
        elif new_neurons < self.min_neurons: return self.min_neurons
        else: return new_neurons

    def mutate_layers(self, layers, num_layers = None):
        if num_layers is None: num_layers = len(layers)
        new_layers = []
        # For every layer we have, we have a probability of mutation
        for i in range(num_layers):
            # If we are mutating this layer
            if random.random() < self.layer_mutation:
                # Mutate number of neurons
                neurons = self.mutate_neurons(layers[i].units)
                # Randomly pick a layer
                new_layer = random.choice(list(self.layer_options.values()))
                # Randomly pick an activation function
                activation = random.choice(self.activation_functions)

                new_layers.append(new_layer(neurons, activation))
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
                # If we are mutating the layers, we must take our new num_layers into account
                if name == 'layers': mutated_chromosome = self.mutations[name](chromosome, mutated_genome.get('num_layers'))
                # Otherwise, perform appropriate mutation
                else: mutated_chromosome = self.mutations[name](chromosome)
                # Update genome
                mutated_genome.update({name : mutated_chromosome})
            # If no mutation occurs, keep the same chromosome
            else: mutated_genome.update({name : chromosome})
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
        parent1 = self.select()
        parent2 = self.select()
        for i in range(self.natality):
            # Combine parent genomes and mutate
            offspring_genome = self.mutate(self.crossover(parent1, parent2))
            # Try bringing the baby to life
            try:
                offspring = self.animate(offspring_genome)
                # If the fit fails, that means that the baby is an incorrect
                # configuration
                offspring.fit(type = self.fitness)
                return offspring
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
        fittest.model.summary()
        print({'generation' : self.generation,
            'best-fitness' : fittest.fit(type = self.fitness),
            'best-genome' : fittest.genome()}, '\n\n')


    def aetas(self):
        '''
        Cruxis of the algorithm
        Runs evolution
        '''
        self.populate()
        for g in range(self.generations):
            self.report()
            self.repopulate()
            self.generation += 1
            # Random Lexicase selection
            self.fitness = random.choice(self.fitness_options)
        return self.fittest()

if __name__ == '__main__':
    'Usage'
    world = Exelixi(4, 20)
    fittest = world.aetas()
    fittest.save()
