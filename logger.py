class Logger(object):
    def __init__(self, file_name):
        self.file_name = f'logs/{file_name}.txt'

    def write_metadata(self, pop_size, vacc_percentage, virus):
        data = f'population size: {pop_size} | vaccination percentage {vacc_percentage * 100}% | virus {virus.name} | mortality rate {virus.mortality_rate * 100}% | reproduction {virus.repro_rate}\n'

        self.write_to_file(data, 'w')

    def log_interactions(self, step_number, number_of_interactions, number_of_new_infections):
        data = f'step {step_number} | interactions {number_of_interactions} | new infections {number_of_new_infections}'

        self.write_to_file(data)

    def log_interaction(self, person, random_person, has_been_infected):
        transmitted = 'WAS' if has_been_infected else 'WAS NOT'

        data = f'[INTERACTION] person {person._id} <> person {random_person._id}. Virus was {transmitted} transmitted.'

        self.write_to_file(data)

    def log_infection_survival(self, step_number, population_count, number_of_new_fatalities):
        data = f'step {step_number} | fatalities {number_of_new_fatalities} | new population {population_count}'

        self.write_to_file(data)

    def write_to_file(self, data, mode='a'):
        with open(self.file_name, mode) as file:
            file.write(data + '\n')
