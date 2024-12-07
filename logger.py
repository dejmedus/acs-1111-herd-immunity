class Logger(object):
    def __init__(self, file_name):
        # TODO:  Finish this initialization method. The file_name passed should be the
        # full file name of the file that the logs will be written to.
        self.file_name = f'logs/{file_name}.txt'

    # The methods below are just suggestions. You can rearrange these or
    # rewrite them to better suit your code style.
    # What is important is that you log the following information from the simulation:

    # Meta data: This shows the starting situtation including:
    #   population, initial infected, the virus, and the initial vaccinated.

    # Log interactions. At each step there will be a number of interaction
    # You should log:
    #   The number of interactions, the number of new infections that occured
    # You should log the results of each step. This should inlcude:
    #   The population size, the number of living, the number of dead, and the number
    #   of vaccinated people at that step.

    # When the simulation concludes you should log the results of the simulation.
    # This should include:
    #   The population size, the number of living, the number of dead, the number
    #   of vaccinated, and the number of steps to reach the end of the simulation.

    def write_metadata(self, pop_size, vacc_percentage, virus):
        # TODO: Finish this method. This data of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every data with a '/n' character to ensure that each
        # event logged ends up on a separate data!
        data = f'population size: {pop_size} | vaccination percentage {vacc_percentage * 100}% | virus {virus.name} | mortality rate {virus.mortality_rate * 100}% | reproduction {virus.repro_rate}]\n'

        self.write_to_file(data, 'w')

    def log_interactions(self, step_number, number_of_interactions, number_of_new_infections):
        data = f'step {step_number} | interactions {number_of_interactions} | new infections {number_of_new_infections}'

        self.write_to_file(data)

    def log_interaction(self, person, random_person, has_been_infected):
        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.

        transmitted = 'WAS' if has_been_infected else 'WAS NOT'

        data = f'[INTERACTION] person {person._id} <> person {random_person._id}. Virus was {transmitted} transmitted.'

        self.write_to_file(data)

    def log_infection_survival(self, step_number, population_count, number_of_new_fatalities):
        # When the simulation concludes you should log the results of the simulation.
        # This should include:
        #   The population size, the number of living, the number of dead, the number
        #   of vaccinated, and the number of steps to reach the end of the simulation.
        data = f'step {step_number} | fatalities {number_of_new_fatalities} | new population {population_count}'

        self.write_to_file(data)

    def write_to_file(self, data, mode='a'):
        with open(self.file_name, mode) as file:
            file.write(data + '\n')
