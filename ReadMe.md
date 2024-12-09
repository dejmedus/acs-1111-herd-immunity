## ACS 1111
### Herd Immunity
A simulation of herd immunity by modeling how a virus moves through a population where some of a population is vaccinated against a virus

### How to run
#### Setup
``` bash
git clone https://github.com/dejmedus/acs-1111-herd-immunity.git
cd acs-1111-herd-immunity
```

#### Simulation
``` bash
# Population Size: 100,000
# Vaccination Percentage: 90%
# Virus Name: Sniffles
# Mortality Rate: 70%
# Reproduction Rate: 25%
# People Initially Infected: 10

python3 simulation.py 100000 0.9 Sniffles 0.70 0.25 10
```

#### Tests
``` bash
python3 -m tests.simulation_test
python3 -m tests.logger_test

python3 person.py
python3 virus.py
```

https://github.com/user-attachments/assets/994f8f1e-0f90-4ace-be89-c32740251789

