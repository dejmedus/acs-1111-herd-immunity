from pathlib import Path
from simulation import Simulation
from virus import Virus
from logger import Logger

virus_name = "Sniffles"
repro_num = 0.5
mortality_rate = 0.12
virus = Virus(virus_name, repro_num, mortality_rate)

pop_size = 1000
vacc_percentage = 0.1
initial_infected = 10


def check_file_exists():
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)
    sim._create_population()

    sim.logger = Logger("test")
    sim.run()

    test_file = Path("logs/test.txt")
    assert test_file.is_file()


def check_file_not_empty():
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)
    sim._create_population()

    sim.logger = Logger("test")
    sim.run()

    test_file = open("logs/test.txt", "r")
    assert test_file.read() != ""


check_file_exists()
check_file_not_empty()
print("logger tests passed!")
