from django.shortcuts import render, HttpResponse, redirect
from home.models import *
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        books = Books.objects.all()
        borrowedBooks = BorrowedBooks.objects.all()
        overtime = overtimeBorrowed.objects.all()
        members = Members.objects.all()
        staffs = Staffs.objects.all()
        genre =Genre.objects.all()
        if BorrowedBooks.objects.filter(returnDate=datetime.now().strftime('%d-%m-%y')).exists():
            book = BorrowedBooks.objects.filter(returnDate=datetime.now().strftime('%d-%m-%y')).values_list('bookName', 'bookID', 'genre', 'dateOfIssue', 'publisher', 'copies', 'borrowerName', 'bookID', 'writer', 'borrowerID', 'returnDate', 'borrowDate')
            for i in book:
                if overtimeBorrowed.objects.filter(bookName=i[0], bookID=i[1], returnDate=i[10], borrowerID=i[9], borrowerName=i[6]).exists():
                    pass
                else:
                    overtimeBorrowed(bookName = i[0],
                    genre=i[2], dateOfIssue=i[3],
                    publisher=i[4], copies=i[5], borrowerName=i[6], bookID=i[1], writer=i[8],  
                    borrowerID=i[9], returnDate=i[10], borrowDate=i[11 ]).save()
        
        params = {
            'books':books,
            'borrowedBooks':borrowedBooks,
            'overtime':overtime,
            'genre':genre,
            'members':members,
            'staffs':staffs
        }
        return render(request, 'index.html', params)
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')

def books(request):
    if request.user.is_authenticated:
        bookRecords = Books.objects.all()
        genre =Genre.objects.all()
        params = {'books':bookRecords, 'genre':genre}
        if BorrowedBooks.objects.filter(returnDate=datetime.now().strftime('%d-%m-%y')).exists():
            book = BorrowedBooks.objects.filter(returnDate=datetime.now().strftime('%d-%m-%y')).values_list('bookName', 'bookID', 'genre', 'dateOfIssue', 'publisher', 'copies', 'borrowerName', 'bookID', 'writer', 'borrowerID', 'returnDate', 'borrowDate')
            for i in book:
                if overtimeBorrowed.objects.filter(bookName=i[0], bookID=i[1], returnDate=i[10], borrowerID=i[9], borrowerName=i[6]).exists():
                    pass
                else:
                    overtimeBorrowed(bookName = i[0],
                    genre=i[2], dateOfIssue=i[3],
                    publisher=i[4], copies=i[5], borrowerName=i[6], bookID=i[1], writer=i[8],  
                    borrowerID=i[9], returnDate=i[10], borrowDate=i[11]).save()

        if request.method == 'POST':
            name = request.POST['bookName']
            writer = request.POST['writer']
            genre = request.POST['genre']
            publisher = request.POST['publisher']
            copies = request.POST['copies']
            entry = Books(
                bookName=name, writer=writer, genre=genre, 
                dateOfIssue=datetime.now().strftime('%d-%m-%y'),
                publisher=publisher, copies=copies, availableCopies=copies
                )
            entry.save()
        
            messages.success(request, 'Book Added to Database Successfully')
            return redirect('/books')
            
        return render(request, 'books.html', params)
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')

def searchBooks(request):
    if request.user.is_authenticated:   
        genre =Genre.objects.all()
        if request.method == 'GET':
            search = request.GET['search']
            results = Books.objects.filter(bookName__icontains=search)
            results2 = Books.objects.filter(publisher__icontains=search)
            results3 = Books.objects.filter(writer__icontains=search)
            results4 = Books.objects.filter(genre__icontains=search)
            results5 = Books.objects.filter(id__icontains=search)
            resultsFinal = results.values('bookName', 'id', 'genre', 'writer', 'dateOfIssue', 'publisher', 'copies', 'availableCopies')
            results2Final = results2.values('bookName', 'id', 'genre', 'writer', 'dateOfIssue', 'publisher', 'copies', 'availableCopies')
            results3Final = results3.values('bookName', 'id', 'genre', 'writer', 'dateOfIssue', 'publisher', 'copies', 'availableCopies')
            results4Final = results4.values('bookName', 'id', 'genre', 'writer', 'dateOfIssue', 'publisher', 'copies', 'availableCopies')
            results5Final = results5.values('bookName', 'id', 'genre', 'writer', 'dateOfIssue', 'publisher', 'copies', 'availableCopies')

            if results.exists():
                params = {'books': resultsFinal, 'genre':genre}
                return render(request, 'searchBooks.html', params)
            if results2.exists():
                params = {'books': results2Final, 'genre':genre}
                return render(request, 'searchBooks.html', params)
            if results3.exists():
                params = {'books': results3Final, 'genre':genre}
                return render(request, 'searchBooks.html', params)
            if results4.exists():
                params = {'books': results4Final, 'genre':genre}
                return render(request, 'searchBooks.html', params)
            if results5.exists():
                params = {'books': results5Final, 'genre':genre}
                return render(request, 'searchBooks.html', params)
            else:
                messages.error(request,'No search results found :-(')
                return redirect('/books')
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')

    
def borrowBook(request, bookID):
    if request.user.is_authenticated:
        
        book = Books.objects.get(id=bookID)
        if request.method == 'POST':
            borrowerID = request.POST['Borrower ID']
            borrower = Members.objects.get(id=borrowerID)
            returnDate = datetime.now() + timedelta(days = 7)
            entry = BorrowedBooks(bookName = book.bookName,
            genre=book.genre, dateOfIssue=book.dateOfIssue,
            publisher=book.publisher, copies=book.copies, borrowerName=borrower.name, bookID=book.id, writer=book.writer,  
            borrowerID=borrowerID, returnDate=returnDate.strftime("%d-%m-%y"), borrowDate=datetime.now().strftime('%d-%m-%y'))
            book.availableCopies = int(book.availableCopies)-1
            borrower.booksBorrowed = int(borrower.booksBorrowed)+1
            borrower.save()
            entry.save()
            book.save()
            messages.success(request, 'Book added to Borrow List.')
            return redirect('/books/borrowedBooks')
        return redirect('/books/borrowedBooks')
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')

def returnBook(request, bookID, borrowerID, borrowID):
    if request.user.is_authenticated:
        borrowed = BorrowedBooks.objects.get(bookID=bookID, borrowerID=borrowerID, id=borrowID)
        book = Books.objects.get(id=bookID)
        book.availableCopies = int(book.availableCopies)+1
        book.save()
        borrowed.delete()
        messages.success(request, 'Book returned by Borrower.')
        return redirect('/books/borrowedBooks')
        # return HttpResponse(overtimebook.returnDate)
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')


def deleteBooks(request, book):
    if request.user.is_authenticated and request.user.is_superuser:
        bookSpecified = Books.objects.get(id=book)
        bookSpecified.delete()
        if BorrowedBooks.objects.filter(bookID=book).exists():
            BorrowedBooks.objects.get(bookID=book).delete()
        messages.error(request, 'Deleted Book from Records')
        return redirect('/books')
    else:
        messages.error(request, 'Please Log In as an Admin')
        return redirect('/')

def editBooks(request, id):
    if request.user.is_authenticated and request.user.is_superuser:    
        bookSpecified = Books.objects.get(id=id)
        if request.method== 'POST':
            name = request.POST['bookName1']
            writer = request.POST['writer1']
            genre = request.POST['genre1']
            publisher = request.POST['publisher1']
            copies = request.POST['copies1']
            copyDiff = int(bookSpecified.copies) - int(bookSpecified.availableCopies)

            bookSpecified.bookName = name
            bookSpecified.writer = writer
            bookSpecified.genre = genre
            bookSpecified.publisher = publisher
            bookSpecified.copies = copies
            bookSpecified.save()
            bookSpecified.availableCopies = int(bookSpecified.copies) - int(copyDiff)
            bookSpecified.save()

            messages.success(request, 'Edited Book Records')
            return redirect('/books')
    else:
        messages.error(request, 'Please Log In as an Admin first')
        return redirect('/')


def borrowedBooksList(request):
    if request.user.is_authenticated:    
        genre =Genre.objects.all()
        borrowedBks = BorrowedBooks.objects.all()
        date = datetime.now().strftime('%d-%m-%y') 
        if BorrowedBooks.objects.filter(returnDate=datetime.now().strftime('%d-%m-%y')).exists():
            book = BorrowedBooks.objects.filter(returnDate=datetime.now().strftime('%d-%m-%y')).values_list('bookName', 'bookID', 'genre', 'dateOfIssue', 'publisher', 'copies', 'borrowerName', 'bookID', 'writer', 'borrowerID', 'returnDate', 'borrowDate')
            for i in book:
                if overtimeBorrowed.objects.filter(bookName=i[0], bookID=i[1], returnDate=i[10], borrowerID=i[9], borrowerName=i[6]).exists():
                    pass
                else:
                    overtimeBorrowed(bookName = i[0],
                    genre=i[2], dateOfIssue=i[3],
                    publisher=i[4], copies=i[5], borrowerName=i[6], bookID=i[1], writer=i[8],  
                    borrowerID=i[9], returnDate=i[10], borrowDate=i[11]).save()

        params = {'borrowedBooks': borrowedBks, 'date':date, 'genre':genre}
        return render(request, 'borrowedBooks.html', params)
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')

def searchBorrowedBooks(request):
    if request.user.is_authenticated:
        genre =Genre.objects.all()
        if request.method == 'GET':
            search = request.GET['search']
            results = BorrowedBooks.objects.filter(bookName__icontains=search)
            results2 = BorrowedBooks.objects.filter(publisher__icontains=search)
            results3 = BorrowedBooks.objects.filter(writer__icontains=search)
            results4 = BorrowedBooks.objects.filter(genre__icontains=search)
            results5 = BorrowedBooks.objects.filter(borrowerName__icontains=search)
            results6 = BorrowedBooks.objects.filter(borrowerID__icontains=search)
            resultsFinal = results.values('bookName', 'id', 'genre', 'writer', 'dateOfIssue', 'publisher', 'copies', 'bookID', 'borrowerName', 'borrowerID', 'borrowDate', 'returnDate')
            results2Final = results2.values('bookName', 'id', 'genre', 'writer', 'dateOfIssue', 'publisher', 'copies', 'bookID', 'borrowerName', 'borrowerID', 'borrowDate', 'returnDate')
            results3Final = results3.values('bookName', 'id', 'genre', 'writer', 'dateOfIssue', 'publisher', 'copies', 'bookID', 'borrowerName', 'borrowerID', 'borrowDate', 'returnDate')
            results4Final = results4.values('bookName', 'id', 'genre', 'writer', 'dateOfIssue', 'publisher', 'copies', 'bookID', 'borrowerName', 'borrowerID', 'borrowDate', 'returnDate')
            results5Final = results5.values('bookName', 'id', 'genre', 'writer', 'dateOfIssue', 'publisher', 'copies', 'bookID', 'borrowerName', 'borrowerID', 'borrowDate', 'returnDate')
            results6Final = results6.values('bookName', 'id', 'genre', 'writer', 'dateOfIssue', 'publisher', 'copies', 'bookID', 'borrowerName', 'borrowerID', 'borrowDate', 'returnDate')

            if results.exists():
                params = {'books': resultsFinal, 'genre':genre}
                return render(request, 'searchBorrowedBooks.html', params)
            if results2.exists():
                params = {'books': results2Final, 'genre':genre}
                return render(request, 'searchBorrowedBooks.html', params)
            if results3.exists():
                params = {'books': results3Final, 'genre':genre}
                return render(request, 'searchBorrowedBooks.html', params)
            if results4.exists():
                params = {'books': results4Final, 'genre':genre}
                return render(request, 'searchBorrowedBooks.html', params)
            if results5.exists():
                params = {'books': results5Final, 'genre':genre}
                return render(request, 'searchBorrowedBooks.html', params)
            if results6.exists():
                params = {'books': results6Final, 'genre':genre}
                return render(request, 'searchBorrowedBooks.html', params)
            else:
                messages.error(request,'No search results found :-(')
                return redirect('/books/borrowedBooks')
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')


def staffs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        staff = Staffs.objects.all()
        params = {'staffs':staff}
        if BorrowedBooks.objects.filter(returnDate=datetime.now().strftime('%d-%m-%y')).exists():
            book = BorrowedBooks.objects.filter(returnDate=datetime.now().strftime('%d-%m-%y')).values_list('bookName', 'bookID', 'genre', 'dateOfIssue', 'publisher', 'copies', 'borrowerName', 'bookID', 'writer', 'borrowerID', 'returnDate', 'borrowDate')
            for i in book:
                if overtimeBorrowed.objects.filter(bookName=i[0], bookID=i[1], returnDate=i[10], borrowerID=i[9], borrowerName=i[6]).exists():
                    pass
                else:
                    overtimeBorrowed(bookName = i[0],
                    genre=i[2], dateOfIssue=i[3],
                    publisher=i[4], copies=i[5], borrowerName=i[6], bookID=i[1], writer=i[8],  
                    borrowerID=i[9], returnDate=i[10], borrowDate=i[11]).save()

        return render(request, 'staffs.html', params)
    else:
        messages.error(request, 'Please Log In as an Admin first')
        return redirect('/')

def addStaff(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST['fname'] + ' ' + request.POST['lname']
            ftname = request.POST['ftname']
            mtname = request.POST['mtname']
            email = request.POST['email']
            contact = request.POST['contact']
            address = request.POST['address']
            pay = request.POST['pay']
            designation = request.POST['designation']
            entry = Staffs(name=name, fname=ftname, mname=mtname, contact=contact, email=email, address=address,
            dateOfJoin=datetime.now().strftime('%d-%m-%y'), pay=pay, designation=designation, leavesAttended=0)
            entry.save()
            messages.success(request, 'Staff Added to Database Successfully')
            return redirect('/staffs')
    else:
        messages.error(request, 'Please Log In as an Admin first')
        return redirect('/')

def deleteStaffs(request, staff):
    if request.user.is_authenticated and request.user.is_superuser:
        stf = Staffs.objects.get(id=staff)
        stf.delete()
        messages.success(request, 'Deleted Staff from Records')
        return redirect('/staffs')
    else:
        messages.error(request, 'Please Log In as an Admin first')
        return redirect('/')

def editStaff(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        staff = Staffs.objects.get(id=id)
        if request.method== 'POST':
            name = request.POST['name']
            ftname = request.POST['ftname1']
            mtname = request.POST['mtname1']
            email = request.POST['email1']
            contact = request.POST['contact1']
            address = request.POST['address1']
            pay = request.POST['pay1']
            designation = request.POST['designation1']
            leave = request.POST['leave1']

            staff.name = name
            staff.fname = ftname
            staff.mname = mtname
            staff.email = email
            staff.contact = contact
            staff.pay = pay
            staff.address = address
            staff.designation = designation
            staff.leavesAttended = leave

            staff.save()

            messages.success(request, 'Edited Staff Records')
            return redirect('/staffs')
    else:
        messages.error(request, 'Please Log In as an Admin first')
        return redirect('/')


def searchStaffs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        
        if request.method == 'GET':
            search = request.GET['searchInput']
            results = Staffs.objects.filter(id__icontains=search)
            results2 = Staffs.objects.filter(name__icontains=search)
            results3 = Staffs.objects.filter(email__icontains=search)
            results4 = Staffs.objects.filter(contact__icontains=search)
            results5 = Staffs.objects.filter(designation__icontains=search)
            resultsFinal = results.values('name', 'id', 'fname', 'mname', 'dateOfJoin', 'email', 'contact', 'address', 'pay', 'designation', 'leavesAttended')
            results2Final = results2.values('name', 'id', 'fname', 'mname', 'dateOfJoin', 'email', 'contact', 'address', 'pay', 'designation', 'leavesAttended')
            results3Final = results3.values('name', 'id', 'fname', 'mname', 'dateOfJoin', 'email', 'contact', 'address', 'pay', 'designation', 'leavesAttended')
            results4Final = results4.values('name', 'id', 'fname', 'mname', 'dateOfJoin', 'email', 'contact', 'address', 'pay', 'designation', 'leavesAttended')
            results5Final = results5.values('name', 'id', 'fname', 'mname', 'dateOfJoin', 'email', 'contact', 'address', 'pay', 'designation', 'leavesAttended')

            if results.exists():
                params = {'staffs': resultsFinal}
                return render(request, 'searchStaffs.html', params)
            if results2.exists():
                params = {'staffs': results2Final}
                return render(request, 'searchStaffs.html', params)
            if results3.exists():
                params = {'staffs': results3Final}
                return render(request, 'searchStaffs.html', params)
            if results4.exists():
                params = {'staffs': results4Final}
                return render(request, 'searchStaffs.html', params)
            if results5.exists():
                params = {'staffs': results5Final}
                return render(request, 'searchStaffs.html', params)
            else:
                messages.error(request,'No search results found :-(')
                return redirect('/staffs')
    else:
        messages.error(request, 'Please Log In as an Admin first')
        return redirect('/')



def members(request):
    if request.user.is_authenticated:
    
        members = Members.objects.all()
        params = {'members':members}
        if BorrowedBooks.objects.filter(returnDate=datetime.now().strftime('%d-%m-%y')).exists():
            book = BorrowedBooks.objects.filter(returnDate=datetime.now().strftime('%d-%m-%y')).values_list('bookName', 'bookID', 'genre', 'dateOfIssue', 'publisher', 'copies', 'borrowerName', 'bookID', 'writer', 'borrowerID', 'returnDate', 'borrowDate')
            for i in book:
                if overtimeBorrowed.objects.filter(bookName=i[0], bookID=i[1], returnDate=i[10], borrowerID=i[9], borrowerName=i[6]).exists():
                    pass
                else:
                    overtimeBorrowed(bookName = i[0],
                    genre=i[2], dateOfIssue=i[3],
                    publisher=i[4], copies=i[5], borrowerName=i[6], bookID=i[1], writer=i[8],  
                    borrowerID=i[9], returnDate=i[10], borrowDate=i[11]).save()

        return render(request, 'members.html', params)
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')


def searchMembers(request):
    if request.user.is_authenticated:
    
        if request.method == 'GET':
            search = request.GET['search']
            results = Members.objects.filter(id__icontains=search)
            results2 = Members.objects.filter(name__icontains=search)
            results3 = Members.objects.filter(email__icontains=search)
            results4 = Members.objects.filter(contact__icontains=search)
            resultsFinal = results.values('name', 'id', 'fname', 'mname', 'dateOfJoin', 'email', 'contact', 'address', 'profession', 'designation', 'booksBorrowed')
            results2Final = results2.values('name', 'id', 'fname', 'mname', 'dateOfJoin', 'email', 'contact', 'address', 'profession', 'designation', 'booksBorrowed')
            results3Final = results3.values('name', 'id', 'fname', 'mname', 'dateOfJoin', 'email', 'contact', 'address', 'profession', 'designation', 'booksBorrowed')
            results4Final = results4.values('name', 'id', 'fname', 'mname', 'dateOfJoin', 'email', 'contact', 'address', 'profession', 'designation', 'booksBorrowed')

            if results.exists():
                params = {'members': resultsFinal}
                return render(request, 'searchMembers.html', params)
            if results2.exists():
                params = {'members': results2Final}
                return render(request, 'searchMembers.html', params)
            if results3.exists():
                params = {'members': results3Final}
                return render(request, 'searchMembers.html', params)
            if results4.exists():
                params = {'members': results4Final}
                return render(request, 'searchMembers.html', params)
            else:
                messages.error(request,'No search results found :-(')
                return redirect('/members')
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')




def addMembers(request):
    if request.user.is_authenticated:
    
        memberRecords = Members.objects.all()
        params = {'books':memberRecords}
        if request.method == 'POST':
            name = request.POST['fname'] + ' ' + request.POST['lname']
            ftname = request.POST['ftname']
            mtname = request.POST['mtname']
            email = request.POST['email']
            contact = request.POST['contact']
            address = request.POST['address']
            profession = request.POST['profession']
            designation = request.POST['designation']
            entry = Members(name=name, fname=ftname, mname=mtname, contact=contact, email=email, address=address,
            dateOfJoin=datetime.now().strftime('%d-%m-%y'), profession=profession, designation=designation, booksBorrowed=0)
            entry.save()
            messages.success(request, 'Member Added to Database Successfully')
            return redirect('/members')
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')

            
def deleteMembers(request, memberr):
    if request.user.is_authenticated:
        
        member = Members.objects.get(id=memberr)
        member.delete()
        messages.success(request, 'Deleted Member from Records')
        return redirect('/members')
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')


def editMembers(request, id):
    if request.user.is_authenticated:
        member = Members.objects.get(id=id)
        if request.method== 'POST':
            name = request.POST['name']
            ftname = request.POST['ftname']
            mtname = request.POST['mtname']
            email = request.POST['email']
            contact = request.POST['contact']
            address = request.POST['address']
            profession = request.POST['profession']
            designation = request.POST['designation']

            member.name = name
            member.fname = ftname
            member.mname = mtname
            member.email = email
            member.contact = contact
            member.profession = profession
            member.address = address
            member.designation = designation

            member.save()

            messages.success(request, 'Edited Book Records')
            return redirect('/members')
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')


def enlistOverDue():
    if request.user.is_authenticated:
        if BorrowedBooks.objects.filter(returnDate=datetime.now().strftime('%d-%m-%y')).exists():
            book = BorrowedBooks.objects.filter(returnDate=datetime.now().strftime('%d-%m-%y')).values_list('bookName', 'bookID', 'genre', 'dateOfIssue', 'publisher', 'copies', 'borrowerName', 'bookID', 'writer', 'borrowerID', 'returnDate', 'borrowDate')
            for i in book:
                if overtimeBorrowed.objects.filter(bookName=i[0], bookID=i[1], returnDate=i[10], borrowerID=i[9], borrowerName=i[6]).exists():
                    pass
                else:
                    overtimeBorrowed(bookName = i[0],
                    genre=i[2], dateOfIssue=i[3],
                    publisher=i[4], copies=i[5], borrowerName=i[6], bookID=i[1], writer=i[8],  
                    borrowerID=i[9], returnDate=i[10], borrowDate=i[11]).save()
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')




def delayedBooks(request):
    if request.user.is_authenticated:
    
        overDue= overtimeBorrowed.objects.all()
        if BorrowedBooks.objects.filter(returnDate=datetime.now().strftime('%d-%m-%y')).exists():
            book = BorrowedBooks.objects.filter(returnDate=datetime.now().strftime('%d-%m-%y')).values_list('bookName', 'bookID', 'genre', 'dateOfIssue', 'publisher', 'copies', 'borrowerName', 'bookID', 'writer', 'borrowerID', 'returnDate', 'borrowDate')
            for i in book:
                if overtimeBorrowed.objects.filter(bookName=i[0], bookID=i[1], returnDate=i[10], borrowerID=i[9], borrowerName=i[6]).exists():
                    pass
                else:
                    overtimeBorrowed(bookName = i[0],
                    genre=i[2], dateOfIssue=i[3],
                    publisher=i[4], copies=i[5], borrowerName=i[6], bookID=i[1], writer=i[8],  
                    borrowerID=i[9], returnDate=i[10], borrowDate=i[11]).save()

        return render(request, 'overtime.html', {"overDue":overDue})
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')


def searchOverDues(request):
    if request.user.is_authenticated:
    
        if request.method == 'GET':
            search = request.GET['search']
            results = overtimeBorrowed.objects.filter(bookName__icontains=search)
            results2 = overtimeBorrowed.objects.filter(publisher__icontains=search)
            results3 = overtimeBorrowed.objects.filter(writer__icontains=search)
            results4 = overtimeBorrowed.objects.filter(genre__icontains=search)
            results5 = overtimeBorrowed.objects.filter(borrowerName__icontains=search)
            results6 = overtimeBorrowed.objects.filter(borrowerID__icontains=search)
            results7 = overtimeBorrowed.objects.filter(bookID__icontains=search)
            resultsFinal = results.values('bookName', 'bookID', 'genre', 'dateOfIssue', 'publisher', 'copies', 'borrowerName', 'bookID', 'writer', 'borrowerID', 'returnDate', 'borrowDate')
            results2Final = results2.values('bookName', 'bookID', 'genre', 'dateOfIssue', 'publisher', 'copies', 'borrowerName', 'bookID', 'writer', 'borrowerID', 'returnDate', 'borrowDate')
            results3Final = results3.values('bookName', 'bookID', 'genre', 'dateOfIssue', 'publisher', 'copies', 'borrowerName', 'bookID', 'writer', 'borrowerID', 'returnDate', 'borrowDate')
            results4Final = results4.values('bookName', 'bookID', 'genre', 'dateOfIssue', 'publisher', 'copies', 'borrowerName', 'bookID', 'writer', 'borrowerID', 'returnDate', 'borrowDate')
            results5Final = results5.values('bookName', 'bookID', 'genre', 'dateOfIssue', 'publisher', 'copies', 'borrowerName', 'bookID', 'writer', 'borrowerID', 'returnDate', 'borrowDate')
            results6Final = results6.values('bookName', 'bookID', 'genre', 'dateOfIssue', 'publisher', 'copies', 'borrowerName', 'bookID', 'writer', 'borrowerID', 'returnDate', 'borrowDate')
            results7Final = results7.values('bookName', 'bookID', 'genre', 'dateOfIssue', 'publisher', 'copies', 'borrowerName', 'bookID', 'writer', 'borrowerID', 'returnDate', 'borrowDate')

            if results.exists():
                params = {'books': resultsFinal}
                return render(request, 'searchOverDues.html', params)
            if results2.exists():
                params = {'books': results2Final}
                return render(request, 'searchOverDues.html', params)
            if results3.exists():
                params = {'books': results3Final}
                return render(request, 'searchOverDues.html', params)
            if results4.exists():
                params = {'books': results4Final}
                return render(request, 'searchOverDues.html', params)
            if results5.exists():
                params = {'books': results5Final}
                return render(request, 'searchOverDues.html', params)
            if results6.exists():
                params = {'books': results6Final}
                return render(request, 'searchOverDues.html', params)
            if results7.exists():
                params = {'books': results7Final}
                return render(request, 'searchOverDues.html', params)
            else:
                messages.error(request,'No search results found :-(')
                return redirect('/books/borrowedBooks')
    else:
        messages.error(request, 'Please Log In first')
        return redirect('/')



def genre(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST['name']
            entry = Genre(name=name)
            entry.save()
            messages.success(request, 'Genre added successfully')
            return redirect('/')
        return render(request, 'genre.html')
    else:
        messages.error(request, 'Please Log In as an Admin first')
        return redirect('/')


def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Successfully logged in, ' + str(user.first_name) + ' ' + str(user.last_name) + '!')
            return redirect('/home')
        else:
            messages.error(request, 'Incorrect credentials')
            return redirect('/')
    else:
        return render(request, 'login.html')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')

def manageAccounts(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            username = request.POST['username1']
            password = request.POST['password1']
            email = username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'User with same username exists')
                return redirect('/manageAccounts')
            else:
                user = User.objects.create_user(username, email, password)
                Accounts(username=username, password=password).save()
                user.save()
            return redirect('/manageAccounts')
        accounts = Accounts.objects.all()
        return render(request, 'manageAccounts.html', {'accounts':accounts})
    else:
        messages.error(request, 'Please Log in as an Admin first')
        return redirect('/')

def manageAccountsSearch(request):
    if request.method == 'GET':
        search = request.GET['searchInput']
        results = Accounts.objects.filter(username__icontains=search)
        resultsFinal = results.values('username', 'password')
    if results.exists():
        return render(request, 'accountsSearch.html', {'accounts':resultsFinal})
    else:
        messages.error(request, 'No search results found :-(')
        return redirect('/manageAccounts')

def editAccounts(request, usernamee):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            email = username
            user = User.objects.get(username=usernamee)
            user.username = username
            user.email = email
            user.set_password(password)
            user2 = Accounts.objects.get(username=usernamee)
            user2.username = username
            user2.password = password
            user.save()
            user2.save()
            messages.success(request, 'Updated Account data')
            return redirect('/manageAccounts')

def deleteAccounts(request, usernamee):
    if request.user.is_authenticated and request.user.is_superuser:
        user = User.objects.get(username=usernamee)
        user2 = Accounts.objects.get(username=usernamee)
        user.delete()
        user2.delete()
        messages.success(request, 'Deleted Account')
        return redirect('/manageAccounts')
        