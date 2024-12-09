
from simulation import Simulation
from virus import Virus
from person import Person

virus_name = "Sniffles"
repro_num = 0.5
mortality_rate = 0.12
virus = Virus(virus_name, repro_num, mortality_rate)

pop_size = 1000
vacc_percentage = 0.1
initial_infected = 10

vaccinated_person = Person(1, True)
unvaccinated_person = Person(2, False)
infected_person = Person(3, False, virus)


def create_correct_population():
    pop_size = 100
    vacc_percentage = 0.9
    initial_infected = 10
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)
    sim._create_population()

    vaccinated = sum(1 for person in sim.people if person.is_vaccinated)
    not_infected = sum(1 for person in sim.people if person.infection ==
                       None)
    infected = sum(1 for person in sim.people if person.infection != None)

    assert vaccinated == 90
    assert not_infected == 90
    assert infected == 10


def correct_interaction_results():
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    assert sim.interaction(infected_person, vaccinated_person) == False
    assert sim.interaction(infected_person, infected_person) == False


def run():
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)
    sim._create_population()

    sim.run()

    infected = sum(1 for person in sim.people if person.infection != None)

    assert sim.pop_size != pop_size
    assert infected > initial_infected


create_correct_population()
correct_interaction_results()
run()
print("tests passed!")
