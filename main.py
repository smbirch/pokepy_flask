import interface
import database


def main():
    # print(
    #     "\nStrong Pokémon, weak Pokémon, that is only the foolish perception of people. Truly skilled trainers should try to win with their favorites.\n"
    # )
    database.create_db()
    interface.setup_user()


if __name__ == "__main__":
    main()
