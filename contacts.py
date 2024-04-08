import psycopg2
from psycopg2 import Error

# Function to connect to the PostgreSQL database
def connect_to_database():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="---",
            host="localhost",
            port="5432",
            database="postgres"
        )
        print("Connected to PostgreSQL database!")
        return connection
    except Error as e:
        print(f"Error while connecting to PostgreSQL: {e}")
        return None

# Function to add a contact to the database
def add_contact_to_database(connection, name, phone):
    try:
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO contacts (name, phone) VALUES (%s,%s)"""
        record_to_insert = (name, phone)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print(f"{count} record(s) inserted successfully into contacts table")
        cursor.close()
    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to insert record into contacts table", error)

# Function to find a contact in the database
def find_contact_in_database(connection, name):
    try:
        cursor = connection.cursor()
        postgres_select_query = """ SELECT * FROM contacts WHERE name = %s """
        cursor.execute(postgres_select_query, (name,))
        record = cursor.fetchone()
        if record:
            print(f"Phone number of {record[1]}: {record[2]}")
        else:
            print(f"Contact {name} not found in the contact book.")
        cursor.close()
    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Error while fetching data from PostgreSQL", error)

def main():
    connection = connect_to_database()
    if not connection:
        return

    while True:
        print("Select action:")
        print("1. Add contact")
        print("2. Find contact")
        print("3. Exit")
        choice = input("Enter action number: ")

        if choice == '1':
            name = input("Enter contact name: ")
            phone = input("Enter phone number: ")
            add_contact_to_database(connection, name, phone)
        elif choice == '2':
            name = input("Enter contact name to find: ")
            find_contact_in_database(connection, name)
        elif choice == '3':
            print("Goodbye!")
            connection.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
