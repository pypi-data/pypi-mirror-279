from .generator import RandomDataGenerator

__all__ = ["RandomDataGenerator"]

generator = RandomDataGenerator()
generate_random_data = generator.generate_random_data
