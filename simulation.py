import random
from datetime import datetime

from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        self.logger = Logger(datetime.now())
        self.virus = virus
        self.pop_size = pop_size
        self.vacc_percentage = vacc_percentage
        self.initial_infected = initial_infected
        self.newly_infected = []
        self.people = self._create_population()

    def _create_population(self):
        people = []
        amount_vacc = self.vacc_percentage * self.pop_size

        for i in range(self.pop_size):
            if i < self.initial_infected:
                people.append(Person(i, False, virus))
            elif i < amount_vacc + self.initial_infected:
                people.append(Person(i, True))
            else:
                people.append(Person(i, False))

        return people

    def _simulation_should_continue(self):
        num_vacc = 0
        num_alive = 0

        for person in self.people:
            if person.is_alive:
                num_alive += 1
                if person.is_vaccinated:
                    num_vacc += 1

        should_continue = num_alive > 0 and num_vacc < num_alive

        self.logger.write_to_file(
            'WILL CONTINUE: ' + str(should_continue) + '\n\n')

        return should_continue

    def run(self):
        self.logger.write_metadata(
            self.pop_size, self.vacc_percentage, self.virus)

        time_step_counter = 0
        should_continue = True

        while should_continue:
            time_step_counter += 1
            self.time_step(time_step_counter)
            should_continue = self._simulation_should_continue()

        self.logger.log_infection_survival()

    def time_step(self, step_num):
        living_people = [person for person in self.people if person.is_alive]
        new_fatalities = 0

        for person in living_people:
            if person.infection != None:
                for i in range(10):
                    random_person = random.choice(living_people)
                    self.interaction(person, random_person)

        self._infect_newly_infected()

        for person in living_people:
            alive = person.did_survive_infection()
            if not alive:
                new_fatalities += 1

        self.logger.log_infection_survival(
            step_num, len(living_people) - new_fatalities, new_fatalities)

    def interaction(self, infected_person, random_person):
        if random_person.is_vaccinated == False and random_person.infection == None:
            has_been_infected = False
            chance = random.uniform(0.0, 1.0)
            if chance < infected_person.infection.repro_rate:
                self.newly_infected.append(random_person)
                has_been_infected = True

            self.logger.log_interaction(
                infected_person, random_person, has_been_infected)

    def _infect_newly_infected(self):
        for person in self.newly_infected:
            person.infection = self.virus

        self.newly_infected = []


if __name__ == "__main__":
    virus_name = "Sniffles"
    repro_num = 0.5
    mortality_rate = 0.12
    virus = Virus(virus_name, repro_num, mortality_rate)

    pop_size = 100
    vacc_percentage = 0.1
    initial_infected = 10

    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)
    # sim._create_population()

    # vaccinated = sum(1 for person in sim.people if person.is_vaccinated)
    # not_infected = sum(1 for person in sim.people if person.infection ==
    #                    None)
    # infected = sum(1 for person in sim.people if person.infection != None)

    # assert vaccinated == 10
    # assert not_infected == 90
    # assert infected == 10

    sim.run()
