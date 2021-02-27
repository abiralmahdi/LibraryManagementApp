from django.db import models

# Create your models here.
class Accounts(models.Model):
    username = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    
class Books(models.Model):
    # ID = models.AutoField(db_index=True, primary_key=True, unique=True, default=1)
    bookName = models.CharField(max_length=1000)
    writer = models.CharField(max_length=1000)
    genre = models.CharField(max_length=1000)
    dateOfIssue = models.CharField(max_length=1000)
    publisher = models.CharField(max_length=1000)
    copies = models.CharField(max_length=1000)
    availableCopies = models.CharField(max_length=1000, default='')

class BorrowedBooks(models.Model):
    bookName = models.CharField(max_length=1000)
    bookID = models.CharField(max_length=100, default='')
    genre = models.CharField(max_length=1000)
    writer = models.CharField(max_length=1000, default='')
    dateOfIssue = models.CharField(max_length=1000)
    publisher = models.CharField(max_length=1000)
    copies = models.CharField(max_length=1000)
    borrowerName = models.CharField(max_length=1000)
    borrowerID = models.CharField(max_length=1000)
    borrowDate = models.CharField(max_length=1000)
    returnDate = models.CharField(max_length=1000)
    qtyBorrowed = models.CharField(max_length=1000)

class overtimeBorrowed(models.Model):
    bookName = models.CharField(max_length=1000)
    bookID = models.CharField(max_length=100, default='')
    genre = models.CharField(max_length=1000)
    writer = models.CharField(max_length=1000, default='')
    dateOfIssue = models.CharField(max_length=1000)
    publisher = models.CharField(max_length=1000)
    copies = models.CharField(max_length=1000)
    borrowerName = models.CharField(max_length=1000)
    borrowerID = models.CharField(max_length=1000)
    borrowDate = models.CharField(max_length=1000)
    returnDate = models.CharField(max_length=1000)
    qtyBorrowed = models.CharField(max_length=1000)
    overtimeBy = models.CharField(max_length=1000)

class Members(models.Model):
    name = models.CharField(max_length=1000)
    fname = models.CharField(max_length=1000)
    mname = models.CharField(max_length=1000)
    contact = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    address = models.CharField(max_length=1000)
    dateOfJoin = models.CharField(max_length=1000)
    profession = models.CharField(max_length=1000)
    designation = models.CharField(max_length=1000)
    booksBorrowed = models.CharField(max_length=1000)

class Staffs(models.Model):
    name = models.CharField(max_length=1000)
    fname = models.CharField(max_length=1000)
    mname = models.CharField(max_length=1000)
    contact = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    address = models.CharField(max_length=1000)
    dateOfJoin = models.CharField(max_length=1000)
    pay = models.CharField(max_length=1000)
    designation = models.CharField(max_length=1000)
    leavesAttended = models.CharField(max_length=1000)

class Genre(models.Model):
    name = models.CharField(max_length=1000)