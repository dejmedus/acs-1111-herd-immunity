import random

from virus import Virus


class Person(object):
    def __init__(self, _id, is_vaccinated, infection=None):
        self._id = _id
        self.is_vaccinated = is_vaccinated
        self.infection = infection
        self.is_alive = True

    def did_survive_infection(self):
        if self.infection != None:
            chance = random.uniform(0.0, 1.0)
            if chance < self.infection.mortality_rate:
                self.is_alive = False
            else:
                self.infection = None
                self.is_vaccinated = True

        return self.is_alive


if __name__ == "__main__":
    vaccinated_person = Person(1, True)
    assert vaccinated_person._id == 1
    assert vaccinated_person.is_alive is True
    assert vaccinated_person.is_vaccinated is True
    assert vaccinated_person.infection is None

    unvaccinated_person = Person(2, False)
    assert unvaccinated_person._id == 2
    assert unvaccinated_person.is_alive is True
    assert unvaccinated_person.is_vaccinated is False
    assert unvaccinated_person.infection is None

    virus = Virus("Sniffles", 0.7, 0.2)
    infected_person = Person(3, False, virus)
    assert infected_person._id == 3
    assert infected_person.is_alive is True
    assert infected_person.is_vaccinated is False
    assert infected_person.infection is virus

    people = []
    for i in range(0, 100):
        people.append(Person(i, False, virus))

    for person in people:
        survived = person.did_survive_infection()

    did_survived = 0
    did_not_survive = 0

    for person in people:
        if person.is_alive:
            did_survived += 1
        else:
            did_not_survive += 1

    print(
        f'survived: {did_survived} did not: {did_not_survive} rate: {virus.mortality_rate}')

    people = []
    for i in range(0, 100):
        people.append(Person(i, False, None))

    for person in people:
        chance = random.uniform(0.0, 1.0)
        was_infected = chance < virus.repro_rate
        if was_infected:
            person.infection = virus

    is_infected = 0
    is_not_infected = 0

    for person in people:
        if person.infection == None:
            is_not_infected += 1
        else:
            is_infected += 1

    print(
        f'infected: {is_infected} is not infected: {is_not_infected} rate: {virus.repro_rate}')
    print("person tests passed!")
