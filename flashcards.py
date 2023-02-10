import argparse
import random
from io import StringIO

deck = []
log = StringIO()
parser = argparse.ArgumentParser(description="This is a flashcard program that quizzes you for answers to "
                                             "those flashcards")
parser.add_argument("--import_from")
parser.add_argument("--export_to")
args = parser.parse_args()

class Card:

    no_cards = 0

    def __init__(self, term, defn, errs=0):
        self.term = term
        self.defn = defn
        self.errs = errs
        Card.no_cards += 1

    def check(self):
        output(f'Print the definition of "{self.term}":')
        ans = _input()
        if ans == self.defn:
            output("Correct!")
        else:
            in_deck = False
            for card in deck:
                if card.defn == ans:
                    output(f'Wrong. The right answer is "{self.defn}", '
                           f'but your definition is correct for "{card.term}".')
                    self.errs += 1
                    in_deck = True
            if not in_deck:
                output(f'Wrong. The right answer is "{self.defn}".')
                self.errs += 1


def _input():
    text = input()
    log.write(text)
    return text


def output(text):
    log.write(text)
    print(text)
    return


def create_card():
    output(f"The card:")
    loop = True
    while loop:
        term = _input()
        loop = False
        for card in deck:
            if card.term == term:
                output(f'The card "{term}" already exists. Try again:')
                loop = True
    output(f"The definition of the card:")
    loop = True
    while loop:
        defn = _input()
        loop = False
        for card in deck:
            if card.defn == defn:
                output(f'The definition "{defn}" already exists. Try again:')
                loop = True
    deck.append(Card(term, defn))
    output(f'The pair ("{term}":"{defn}") has been added.')
    return


def export_cards(fname):
    file = open(fname, 'w', encoding="utf-8")
    for card in deck:
        file.write(card.term + ":" + card.defn + ":" + str(card.errs) + "\n")
    output(f"{Card.no_cards} cards have been saved.")
    file.close()
    return


def hardest_card():
    most = -1
    mult = False
    terms = ""
    for card in deck:
        if card.errs < most:
            continue
        elif card.errs == most:
            terms += f', "{card.term}"'
            mult = True
        else:
            terms = f'"{card.term}"'
            most = card.errs
            mult = False
    if most <= 0:
        output("There are no cards with errors.")
    elif mult:
        output(f'The hardest cards are {terms}. You have {most} errors answering them.')
    else:
        output(f'The hardest card is {terms}. You have {most} errors answering it.')
    return


def import_cards(fname):
    try:
        file = open(fname, 'r', encoding="utf-8")
    except FileNotFoundError:
        output("File not found.")
        return
    loads = 0
    for line in file:
        term, defn, errs = line.strip().split(":")
        errs = int(errs)
        in_deck = False
        for card in deck:
            if card.term == term:
                card.defn = defn
                card.errs = errs
                in_deck = True
        if not in_deck:
            deck.append(Card(term, defn, errs))
        loads += 1
    output(f"{loads} cards have been loaded.")
    return


def rand_ask(num):
    for x in range(num):
        card_num = random.randrange(len(deck))
        deck[card_num].check()


def rem_card(del_term):
    for card in deck:
        if del_term == card.term:
            deck.remove(card)
            Card.no_cards -= 1
            output("The card has been removed")
            return
    output(f'Can\'t remove "{del_term}": there is no such card.')
    return


def reset_stats():
    for card in deck:
        card.errs = 0
    output("Card statistics have been reset.")
    return


def save_log(fname):
    with open(fname, 'w', encoding="utf-8") as file:
        print(log.getvalue(), file=file)
    output("The log has been saved.")
    return


def main():
    running = True
    if args.import_from is not None:
        import_cards(args.import_from)
    while running:
        output("Input the action (add, remove, import, export, ask, exit, log,"
               " hardest card, reset stats):")
        cmd = _input()
        if cmd == "add":
            create_card()
        elif cmd == "remove":
            output("Which card?")
            term = _input()
            rem_card(term)
        elif cmd == "import":
            output("File name:")
            fname = _input()
            import_cards(fname)
        elif cmd == "export":
            output("File name:")
            fname = _input()
            export_cards(fname)
        elif cmd == "ask":
            output("How many times to ask?")
            num = int(_input())
            rand_ask(num)
        elif cmd == "exit":
            output("Bye bye!")
            if args.export_to is not None:
                export_cards(args.export_to)
            running = False
        elif cmd == "log":
            output("File name:")
            fname = _input()
            save_log(fname)
        elif cmd == "hardest card":
            hardest_card()
        elif cmd == "reset stats":
            reset_stats()
        else:
            output("That command isn't recognised, please input "
                   "an action from the list.")
        output("")


main()
