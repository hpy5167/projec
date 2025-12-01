# user creation done
# user auth done
# question generation
# answer checking
# persistent scoring


from qbreader import Sync as qbr
from qbreader import AnswerJudgement as judge
import os
import re


# MAKING ACCOUTNS PART ############################################################


# list of all user account info (stored as plaintext since its easy)
USER_FILE = "users.txt"


# fetches the list of users into the program memory
def load_users() -> dict:
    users = {}
    if not os.path.exists(USER_FILE):
        return users

    with open(USER_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue

            parts = line.split(":")

            # username:password:score
            username = parts[0]
            password = parts[1]
            score = int(parts[2]) if len(parts) > 2 else 0

            users[username] = {"password": password, "score": score}

    return users


# adds new user info into the USER_FILE
def add_user(username: str, password: str):
    # opens the USER_FILE for writing and writes the new user info
    with open(USER_FILE, "a") as f:
        f.write(f"{username}:{password}:0\n")


# function to register a new user
def register(users: dict):
    username = input("\nenter a username: ").strip()
    if not username:  # if input is blank
        print("\nusername cant be empty")
        return
    if username in users:  # if inputted username is already taken
        print("\nusername already exists")
        return
    password = input("Enter a password: ").strip()
    if not password:  # if password inputted is empty
        print("\npassword cant be empty either")
        return
    users[username] = password
    # calls the add_user function to add new user info the users.txt
    add_user(username, password)
    # finished
    print("\n\nregistered")


def save_users(users: dict):
    with open(USER_FILE, "w") as f:
        for username, info in users.items():
            f.write(f"{username}:{info["password"]}:{info["score"]}\n")


# log in function
def login(users: dict):
    # inputs cleaned for spaces and stuff
    username = input("\nenter your username: ").strip()
    password = input("enter your password: ").strip()

    # im such a genius
    if username in users and users[username]["password"] == password:
        print("\n\nyou in")
        print(f"\ncurrent score: {users[username]["score"]}")
        return username
    else:
        print("\n\ninvalid username or password")


# MAKING ACCOUTNS PART OVER ############################################################

# MAKING QUESTIONS PART ############################################################


# can only be accessed after login
def play(users: dict, username: str):

    def strip_brackets(answer: str) -> str:
        return re.sub(r"\s*\[.*?\]\s*", "", answer).strip()

    client = qbr()  # creates client to interact with the database with
    tossup = client.random_tossup()[0]

    # gets a question (tossup) from the database
    print(tossup.question_sanitized)  # prints the question into the terminal

    user_answer = input("Your answer: ").strip().lower()
    correct_answer = tossup.answer_sanitized.lower()

    judgement = tossup.check_answer_sync(user_answer)

    if judgement.correct():
        print("good")

        # update memory
        users[username]["score"] += 1

        # save to users.txt
        save_users(users)

        print(f"Your score is now {users[username]["score"]}")
    else:
        correct_clean = strip_brackets(tossup.answer_sanitized)
        print(f"no the correct answer was: {correct_clean}")


def main():
    users = load_users()  # Load users once at startup
    logged_in_user = None

    while True:
        # if no ones logged in
        # by default they arent logged in
        if not logged_in_user:  # then they have to log in
            choice = input("\nchoose: [1] register [2] login [3] quit: ").strip()
            if choice == "1":
                register(users)
            elif choice == "2":
                logged_in_user = login(users)
            elif choice == "3":
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nend")
                break
            else:
                print("\n\nno")
        else:  # but if they are logged in
            choice = input(f"[1] play  [2] logout: ").strip()
            if choice == "1":
                play(users, logged_in_user)
            elif choice == "2":
                print("\n\nyou out")
                logged_in_user = None
            else:
                print("\n\nno")


# technically it starts running here but all this part does is tell it to start at main()
if __name__ == "__main__":
    main()
