import random
import sys
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
        living_people = [person for person in self.people if person.is_alive]
        vaccinated = sum(1 for person in living_people if person.is_vaccinated)
        infected = sum(
            1 for person in living_people if person.infection != None)
        should_continue = len(
            living_people) > 0 and vaccinated < len(living_people) and infected > 0

        return should_continue

    def run(self):
        self.logger.write_metadata(
            self.pop_size, self.vacc_percentage, self.virus, self.initial_infected)

        time_step_counter = 0
        should_continue = True

        while should_continue:
            time_step_counter += 1
            self.time_step(time_step_counter)
            should_continue = self._simulation_should_continue()

        vaccinated = sum(1 for person in self.people if person.is_vaccinated)

        self.logger.log_conclusion_metadata(
            time_step_counter, len(self.people), self.pop_size, vaccinated)

    def time_step(self, step_num):
        living_people = [person for person in self.people if person.is_alive]
        infected_people = [
            person for person in living_people if person.infection != None]

        for person in infected_people:
            for i in range(100):
                self.logger.total_interactions += 1
                random_person = random.choice(living_people)
                self.interaction(person, random_person)

        new_fatalities = 0

        for person in infected_people:
            alive = person.did_survive_infection()

            self.logger.log_infection_effects(person)

            if not alive:
                new_fatalities += 1
                self.pop_size -= 1

        new_infections = len(set(self.newly_infected))
        self.logger.total_infected += new_infections
        self._infect_newly_infected()

        vaccinated = sum(1 for person in living_people if person.is_vaccinated)

        self.logger.log_infection_survival(
            step_num, len(living_people) - new_fatalities, new_infections, new_fatalities, vaccinated)

    def interaction(self, infected_person, random_person):
        has_been_infected = False
        if random_person.is_vaccinated == False and random_person.infection == None:
            chance = random.uniform(0.0, 1.0)
            if chance < infected_person.infection.repro_rate:
                self.newly_infected.append(random_person)
                has_been_infected = True

            self.logger.log_interaction(
                infected_person, random_person, has_been_infected)
        else:
            self.logger.vacc_safeguard += 1
        return has_been_infected

    def _infect_newly_infected(self):
        for person in self.newly_infected:
            person.infection = self.virus

        self.newly_infected = []


if __name__ == "__main__":

    virus_name = sys.argv[3]
    repro_num = float(sys.argv[5])
    mortality_rate = float(sys.argv[4])
    virus = Virus(virus_name, repro_num, mortality_rate)

    pop_size = int(sys.argv[1])
    vacc_percentage = float(sys.argv[2])
    initial_infected = int(sys.argv[6])

    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    sim.run()
