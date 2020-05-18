from evolve import AutomaticModelEvolution
from ai import Model
from tensorflow.keras.models import load_model

if __name__ == '__main__':
    'Usage'
    # Run until we get a good solution or until we reach generation 15
    # Or get an error on testing that is less than 1
    # world = AutomaticModelEvolution(size = 10, generations = 15, ancestor = False,
    #     target = 1, verbose=1)
    # ancient_genome = world.get_ancestor()
    # print(ancient_genome)
    # ancient_genome['split'] = 1
    # ancestor = world.animate(ancient_genome)
    # ancestor.predict(12, 2022)

    # world.run()
    # world.save()

    primis = Model(t = 12, split = 1, verbose=1, epochs = 1000)

    primis.fit()

    # primis.model = load_model('model.h5')
    # primis.model.summary()

    primis.predict(12, 2020)
