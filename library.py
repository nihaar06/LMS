import os
from supabase import Client,create_client
from dotenv import load_dotenv
from datetime import datetime,timezone


load_dotenv()

url=os.getenv('SUPABASE_URL')
key=os.getenv('SUPABASE_KEY')

sb:Client=create_client(url,key)

#***CREATE***
def add_member(name,email):
    payload={'name':name,'email':email}
    resp=sb.table("members").insert(payload).execute()
    return resp.data

def add_book(title,author,category,stock):
    payload={"title":title,"author":author,"category":category,"stock":stock}
    resp=sb.table("books").insert(payload).execute()
    return resp.data

#***READ***
def list_books():
    resp=sb.table("books").select("*").execute()
    bk=resp.data
    if bk:
        print("BOOK DETAILS:")
        for i in bk:
            print(f"{i['book_id']}:\nTitle:{i['title']}\nAuthor:{i['author']}\nCategory:{i['category']}\nStock:{i['stock']}")
    else:
        print("No books found")

def search_books(t=None,a=None,c=None):
    query = sb.table("books").select("*")
    if t: query = query.eq("title", t)
    if a: query = query.eq("author", a)
    if c: query = query.eq("category", c)
    resp = query.execute()
    if resp.data:
        for i in resp.data:
            print("Book found")
            print("Details are:")
            print(f"{i['book_id']}:\nTitle:{i['title']}\nAuthor:{i['author']}\nCategory:{i['category']}\nStock:{i['stock']}")
    else:
        print("Not found")
def list_members():
    resp=sb.table("members").select("*").execute()
    if resp.data:
        print("Member details are:")
        for i in resp.data:
            print(f"{i['member_id']}:\nName:{i['name']}\nEmail:{i['email']}\nJoin Date:{i['join_date']}")
            in_resp=sb.table("borrow_records").select("*").eq("member_id",i['member_id']).execute()
            if in_resp.data:
                print("Borrowed books are:")
                for br in in_resp.data:
                    print(f"{br['record_id']}:\nMember id:{br['member_id']}\nBook id:{br['book_id']}\nBorrowed Date:{br['borrow_date']}\nReturn date:{br['return_date']}")
    else:
        print("No members found")

#***UPDATE***
def update_book_stock(id,st):
    resp=sb.table("books").update({"stock":st}).eq("book_id",id).execute()
    return resp.data

def update_member(member_id,email):
    resp=sb.table("members").update({"email":email}).eq("member_id",member_id).execute()
    return resp.data

#***DELETE***
def delete_member(id):
    res=None
    resp=sb.table("members").select("*").eq("member_id",id).execute()
    if resp.data:
        for i in resp.data:
            check=sb.table("borrow_records").select("*").eq("member_id",i['member_id']).execute()
            if check.data:
                print("Member cant be deleted until the book is returned")
            else:
                res=sb.table("members").delete().eq("member_id",id).execute()
    return res

def delete_book(book_id):
    res=None
    resp=sb.table('books').select('*').eq('book_id',book_id).execute()
    if resp.data:
        for i in resp.data:
            check=sb.table('borrow_records').select('*').eq('book_id',i['book_id']).execute()
            if check.data:
                print("Book cannot be deleted until the book is returned")
            else:
                res=sb.table('books').delete().eq('book_id',book_id).execute()
    return res
 
def borrow_book(member_id,book_id):
    ch=sb.table('books').select('stock').eq('book_id',book_id).execute()
    if not ch.data or ch.data[0]['stock']<=0:
        print("Book not available")
        return None
    payload={
        'member_id':member_id,
        'book_id':book_id,
        'borrow_date':datetime.now(timezone.utc).isoformat(),
    }
    resp=sb.table('borrow_records').insert(payload).execute()
    sb.table('books').update({'stock':ch.data[0]['stock']-1}).eq('book_id',book_id).execute()
    return resp.data

def return_book(record_id):
    check = sb.table('borrow_records').select('*').eq('record_id', record_id).execute()
    if check.data:
        record = check.data[0]
        resp = sb.table('borrow_records').update(
            {'return_date': datetime.now(timezone.utc).isoformat()}
        ).eq('record_id', record_id).execute()
        book = sb.table('books').select('stock').eq('book_id', record['book_id']).execute()
        if book.data:
            current_stock = book.data[0]['stock']
            sb.table('books').update({'stock': current_stock + 1}).eq('book_id', record['book_id']).execute()
        return resp.data
