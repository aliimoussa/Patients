import pandas as pd
import random

# List of possible first names
first_names = ['Emma', 'Liam', 'Ava', 'Noah', 'Olivia', 'Ethan', 'Isabella', 'Mia', 'Sophia', 'Jacob', 'William', 'Charlotte', 'James',
               'Amelia', 'Benjamin', 'Evelyn', 'Lucas', 'Harper', 'Michael', 'Abigail', 'Alexander', 'Emily', 'Daniel', 'Madison', 'Henry',
               'Avery', 'Matthew', 'Elizabeth', 'Sebastian', 'Scarlett', 'David', 'Chloe', 'Jackson', 'Victoria', 'Owen', 'Penelope',
               'Ella', 'Levi', 'Grace', 'Gabriel', 'Aria', 'Nathan', 'Hannah', 'Dylan', 'Lily', 'Caleb', 'Addison', 'Eli', 'Natalie',
               'Connor', 'Sofia', 'Julia', 'Luke', 'Avery', 'Caroline', 'Isaac', 'Aaliyah', 'Eleanor', 'Wyatt', 'Audrey', 'Oscar',
               'Aurora', 'Nicholas', 'Genesis', 'Josiah', 'Luna', 'Mason', 'Brooklyn', 'Adam', 'Aubrey', 'Leo', 'Alyssa', 'Ian', 'Ellie',
               'Eva', 'Isabelle', 'Landon', 'Nora', 'Ethan', 'Stella', 'Josie', 'Samantha', 'Leonardo', 'Maya', 'Lincoln', 'Piper', 'Xavier',
               'Hazel', 'Miles', 'Avery', 'Genesis', 'Zoe', 'Zachary', 'Aria', 'Bella', 'Mateo', 'Nova', 'Makayla', 'Emilia', 'Emery', 'Serenity',
               'Adalyn', 'Riley', 'Willow', 'Liliana', 'Madelyn', 'Arianna', 'Aubree', 'Aaliyah', 'Jaxon', 'Kaylee', 'Elena', 'Makenzie', 'Claire',
               'Leah', 'Alessandra', 'Delilah', 'Lila', 'Camila', 'Avery', 'Natalia', 'Genesis', 'Evangeline', 'Adeline', 'Aria', 'Ayla', 'Brooklynn',
               'Naomi', 'Katherine', 'Jocelyn', 'Brielle', 'Elise', 'Aliyah', 'Jayla', 'Sienna', 'Alexandra', 'Maggie', 'Makenna', 'Callie', 'Annabelle',
               'Cora', 'Elliana', 'Paige', 'Haley', 'Daisy', 'Amaya', 'Journey', 'Kinsley', 'Eloise', 'Hayden', 'Maddison', 'Eliza', 'Malia', 'Adelaide']

# Generate 150 random first names
patient_first_names = random.choices(first_names, k=150)

# Create a dataframe with the patient first names column
df = pd.DataFrame({'first_name': patient_first_names})

# Print the first 10 rows of the dataframe
print(df.head(10))