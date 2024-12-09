class Logger(object):
    def __init__(self, file_name):
        self.file_name = f'logs/{file_name}.txt'
        self.timestamp = file_name
        self.vacc_safeguard = 0
        self.total_infected = 0
        self.total_interactions = 0

    def write_metadata(self, pop_size, vacc_percentage, virus, initial_infected):
        data = f'population size: {pop_size} | initial infected {initial_infected} | vaccination percentage {vacc_percentage * 100}% | virus {virus.name} | mortality rate {virus.mortality_rate} | reproduction {virus.repro_rate} | timestamp: {self.timestamp}\n'

        self.write_to_file(data, 'w')

    def log_interaction(self, person, random_person, has_been_infected):
        transmitted = 'VIRUS TRANSMISSION' if has_been_infected else ''

        data = f'P{person._id} <> P{random_person._id} {transmitted}'

        self.write_to_file(data)

    def log_infection_survival(self, step_number, population_count, new_infections, number_of_new_fatalities, total_vacc):
        data = f'step {step_number} | new infections {new_infections} | fatalities {number_of_new_fatalities} | new population {population_count} | total_vacc {total_vacc}'

        self.write_to_file(data)

    def log_infection_effects(self, person):
        survived = 'SURVIVED' if person.is_alive else 'DID NOT SURVIVE'
        data = f'P{person._id} {survived}'

        self.write_to_file(data)

    def log_conclusion_metadata(self, total_steps, org_pop, curr_pop, total_vacc):
        data = f'\n\ntotal steps: {total_steps} | total interactions: {self.total_interactions} | original population: {org_pop} | current population: {curr_pop} | total infected: {self.total_infected} | total fatalities: {org_pop - curr_pop} | total vaccinations: {total_vacc} | vaccines prevented transmission: {self.vacc_safeguard} times'

        self.write_to_file(data)

    def write_to_file(self, data, mode='a'):
        with open(self.file_name, mode) as file:
            file.write(data + '\n')
