import argparse
from library import (
    add_member, add_book, list_books, search_books, list_members,
    update_book_stock, update_member, delete_member, delete_book,
    borrow_book, return_book
)

def main():
    parser = argparse.ArgumentParser(description="📚 Online Library Management System")
    subparsers = parser.add_subparsers(dest="command")

    # --- Members ---
    add_member_cmd = subparsers.add_parser("add-member", help="Register a new member")
    add_member_cmd.add_argument("name")
    add_member_cmd.add_argument("email")

    subparsers.add_parser("list-members", help="List all members")

    update_member_cmd = subparsers.add_parser("update-member", help="Update member email")
    update_member_cmd.add_argument("member_id", type=int)
    update_member_cmd.add_argument("email")

    delete_member_cmd = subparsers.add_parser("delete-member", help="Delete a member")
    delete_member_cmd.add_argument("member_id", type=int)

    # --- Books ---
    add_book_cmd = subparsers.add_parser("add-book", help="Add a new book")
    add_book_cmd.add_argument("title")
    add_book_cmd.add_argument("author")
    add_book_cmd.add_argument("category")
    add_book_cmd.add_argument("stock", type=int)

    subparsers.add_parser("list-books", help="List all books")

    search_books_cmd = subparsers.add_parser("search-books", help="Search books by filters")
    search_books_cmd.add_argument("-t", "--title")
    search_books_cmd.add_argument("-a", "--author")
    search_books_cmd.add_argument("-c", "--category")

    update_stock_cmd = subparsers.add_parser("update-stock", help="Update stock of a book")
    update_stock_cmd.add_argument("book_id", type=int)
    update_stock_cmd.add_argument("stock", type=int)

    delete_book_cmd = subparsers.add_parser("delete-book", help="Delete a book")
    delete_book_cmd.add_argument("book_id", type=int)

    # --- Transactions ---
    borrow_cmd = subparsers.add_parser("borrow", help="Borrow a book")
    borrow_cmd.add_argument("member_id", type=int)
    borrow_cmd.add_argument("book_id", type=int)

    return_cmd = subparsers.add_parser("return", help="Return a book")
    return_cmd.add_argument("record_id", type=int)

    args = parser.parse_args()

    if args.command == "add-member":
        print(add_member(args.name, args.email))
    elif args.command == "list-members":
        list_members()
    elif args.command == "update-member":
        print(update_member(args.member_id, args.email))
    elif args.command == "delete-member":
        print(delete_member(args.member_id))
    elif args.command == "add-book":
        print(add_book(args.title, args.author, args.category, args.stock))
    elif args.command == "list-books":
        list_books()
    elif args.command == "search-books":
        search_books(args.title, args.author, args.category)
    elif args.command == "update-stock":
        print(update_book_stock(args.book_id, args.stock))
    elif args.command == "delete-book":
        print(delete_book(args.book_id))
    elif args.command == "borrow":
        print(borrow_book(args.member_id, args.book_id))
    elif args.command == "return":
        print(return_book(args.record_id))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
