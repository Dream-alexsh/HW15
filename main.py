import sqlite3


def connect(query):
    with sqlite3.connect('animal.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def main():
    query = """
                CREATE TABLE IF NOT EXISTS colors(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    color VARCHAR(50)
            )
        """

    connect(query)

    query_1 = """
                CREATE TABLE IF NOT EXISTS animals_colors(
                    animals_id INTEGER,
                    colors_id INTEGER,
                    FOREIGN KEY(animals_id) REFERENCES animals_final(id),
                    FOREIGN KEY(colors_id) REFERENCES colors(id)
            )
        """

    connect(query_1)

    query_2 = """
        INSERT INTO colors (color)
    SELECT DISTINCT * FROM (
        SELECT DISTINCT color1 AS color
        FROM animals
        UNION ALL
        SELECT DISTINCT color2 AS color
        FROM animals
        )
        """

    connect(query_2)

    query_3 = """
            INSERT INTO animals_colors (animals_id, colors_id)
                SELECT DISTINCT animals."index", colors.id
                FROM animals
                LEFT JOIN colors ON colors.color = animals.color1
                UNION ALL
                SELECT DISTINCT animals."index", colors.id
                FROM animals
                LEFT JOIN colors ON colors.color = animals.color2
        """

    connect(query_3)

    query_5 = """
                CREATE TABLE IF NOT EXISTS outcome(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subtype VARCHAR(50),
                    "type" VARCHAR(50),
                    "month" INTEGER,
                    "year" INTEGER
        )
        """

    connect(query_5)

    query_6 = """
            INSERT INTO outcome (subtype, "type", "month", "year")
                SELECT DISTINCT animals.outcome_subtype, animals.outcome_type, animals.outcome_month, animals.outcome_year
                FROM animals;
        """

    connect(query_6)

    query_7 = """
            CREATE TABLE IF NOT EXISTS breed_type(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                breed VARCHAR(50)
        )
        """

    connect(query_7)

    query_8 = """
            INSERT INTO breed_type (breed)
                SELECT DISTINCT animals.breed
                FROM animals
        """

    connect(query_8)

    query_9 = """
            CREATE TABLE IF NOT EXISTS animals_final(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age_upon_outcome VARCHAR(50),
                animal_id VARCHAR(50),
                animal_type VARCHAR(50),
                name VARCHAR(50),
                breed_type_id INTEGER,
                date_of_birth VARCHAR(50),
                outcome_id INTEGER,
                FOREIGN KEY(outcome_id) REFERENCES outcome(id),
                FOREIGN KEY(breed_type_id) REFERENCES breed_type(id)
        )
        """

    connect(query_9)

    query_10 = """
            INSERT INTO animals_final (age_upon_outcome, animal_id, animal_type, name, breed_type_id, date_of_birth, outcome_id)
            SELECT DISTINCT animals.age_upon_outcome, animals.animal_id, animals.animal_type, animals.name, breed_type.id, animals.date_of_birth, outcome.id
            FROM animals
            LEFT JOIN outcome
                ON outcome.subtype = animals.outcome_subtype
                AND outcome."type" = animals.outcome_type
                AND outcome."month" = animals.outcome_month
                AND outcome."year" = animals.outcome_year
            JOIN breed_type
                ON breed_type.breed = animals.breed ;
        """

    connect(query_10)

    query_12 = """
            INSERT INTO animals_colors (animals_id, colors_id)
            SELECT DISTINCT animals_final.id, colors.id
            FROM animals
            LEFT JOIN colors ON colors.color = animals.color1
            JOIN animals_final ON animals_final.animal_id = animals.animal_id
            UNION ALL
            SELECT DISTINCT animals_final.id, colors.id
            FROM animals
            LEFT JOIN colors ON colors.color = animals.color2
            JOIN animals_final ON animals_final.animal_id = animals.animal_id;
        """

    connect(query_12)

    query_11 = """
            SELECT animals_final.name, animals_final.breed_type_id, colors.color
                FROM animals_final
                JOIN animals_colors ON animals_colors.animals_id = animals_final.id
                JOIN colors ON colors.id = animals_colors.colors_id
        """

    connect(query_11)


def app_main(animal):
    with sqlite3.connect('animal.db') as connection:
        cursor = connection.cursor()
        query_12 = """
                SELECT name, age_upon_outcome, date_of_birth
                FROM animals_final
                WHERE id LIKE :animal
                ORDER BY name
            """
        cursor.execute(query_12, {'animal': f'{animal}'})
        result = cursor.fetchall()
        for i in result:
            animal_dict = {
                'Name': i[0],
                'age_upon_outcome': i[1],
                'date_of_birth': i[2]
            }
        return animal_dict


if __name__ == "__main__":
    main()

