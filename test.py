from Scripts import RandomTimeGenerator

generator = RandomTimeGenerator(distribution='norm', loc=200, scale=15)
random_values = generator.generate(size=1)  # Generate 100 values
print(random_values)