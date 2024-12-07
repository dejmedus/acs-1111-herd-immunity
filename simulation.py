import random
import sys
# random.seed(42)
from datetime import datetime
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        self.logger = Logger(datetime.now())

        # TODO: Store the virus in an attribute
        self.virus = virus

        # TODO: Store pop_size in an attribute
        self.pop_size = pop_size

        # TODO: Store the vacc_percentage in a variable
        self.vacc_percentage = vacc_percentage

        # TODO: Store initial_infected in a variable
        self.initial_infected = initial_infected

        self.newly_infected = []

        # You need to store a list of people (Person instances)
        # Some of these people will be infected some will not.
        # Use the _create_population() method to create the list and
        # return it storing it in an attribute here.
        # TODO: Call self._create_population() and pass in the correct parameters.
        self.people = self._create_population()

    def _create_population(self):
        # TODO: Create a list of people (Person instances). This list
        # should have a total number of people equal to the pop_size.
        # Some of these people will be uninfected and some will be infected.
        # The number of infected people should be equal to the the initial_infected
        people = []
        amount_vacc = self.vacc_percentage * self.pop_size

        for i in range(self.pop_size):
            if i < self.initial_infected:
                people.append(Person(i, False, virus))
            elif i < amount_vacc + self.initial_infected:
                people.append(Person(i, True))
            else:
                people.append(Person(i, False))

        # TODO: Return the list of people
        return people

    def _simulation_should_continue(self):
        # This method will return a boolean indicating if the simulation
        # should continue.
        # The simulation should not continue if all of the people are dead,
        # or if all of the living people have been vaccinated.
        # TODO: Loop over the list of people in the population. Return True
        # if the simulation should continue or False if not.
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
        # TODO: Write meta data to the logger. This should be starting
        # statistics for the simulation. It should include the initial
        # population size and the virus.
        self.logger.write_metadata(
            self.pop_size, self.vacc_percentage, self.virus)

        # This method starts the simulation. It should track the number of
        # steps the simulation has run and check if the simulation should
        # continue at the end of each step.
        time_step_counter = 0
        should_continue = True

        while should_continue:
            # TODO: Increment the time_step_counter
            # TODO: for every iteration of this loop, call self.time_step()
            # Call the _simulation_should_continue method to determine if
            # the simulation should continue
            time_step_counter += 1
            self.time_step(time_step_counter)
            should_continue = self._simulation_should_continue()

        # TODO: When the simulation completes you should conclude this with
        # the logger. Send the final data to the logger.
        self.logger.log_infection_survival()

    def time_step(self, step_num):
        # This method will simulate interactions between people, calculate
        # new infections, and determine if vaccinations and fatalities from infections
        # The goal here is have each infected person interact with a number of other
        # people in the population
        # TODO: Loop over your population
        # For each person if that person is infected
        # have that person interact with 100 other living people
        # Run interactions by calling the interaction method below. That method
        # takes the infected person and a random person
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
        # TODO: Finish this method.
        # The possible cases you'll need to cover are listed below:
        # random_person is vaccinated:
        #     nothing happens to random person.
        # random_person is already infected:
        #     nothing happens to random person.
        # random_person is healthy, but unvaccinated:
        # generate a random number between 0.0 and 1.0.  If that number is smaller
        #  than repro_rate, add that person to the newly infected array
        #     Simulation object's newly_infected array, so that their infected
        #     attribute can be changed to True at the end of the time step.
        if random_person.is_vaccinated == False and random_person.infection == None:
            has_been_infected = False
            chance = random.uniform(0.0, 1.0)
            if chance < infected_person.infection.repro_rate:
                self.newly_infected.append(random_person)
                has_been_infected = True

            # TODO: Call logger method during this method.
            self.logger.log_interaction(
                infected_person, random_person, has_been_infected)

    def _infect_newly_infected(self):
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        for person in self.newly_infected:
            person.infection = self.virus

        self.newly_infected = []


if __name__ == "__main__":
    # Test your simulation here
    virus_name = "Sniffles"
    repro_num = 0.5
    mortality_rate = 0.12
    virus = Virus(virus_name, repro_num, mortality_rate)

    # Set some values used by the simulation
    pop_size = 100
    vacc_percentage = 0.1
    initial_infected = 10

    # Make a new instance of the simulation
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)
    sim._create_population()

    vaccinated = sum(1 for person in sim.people if person.is_vaccinated)
    not_infected = sum(1 for person in sim.people if person.infection ==
                       None)
    infected = sum(1 for person in sim.people if person.infection != None)

    assert vaccinated == 10
    assert not_infected == 90
    assert infected == 10

    sim.run()
