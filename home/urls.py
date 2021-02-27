from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('', login, name='login'),
    path('logout', logout, name='logout'),
    path('home', index, name='home'),
    path('books', books, name='books'),
    path('books/searchBooks', searchBooks, name='searchBooks'),
    path('books/borrowedBooks', borrowedBooksList, name='borrowedBooks'),
    path('books/borrowedBooks/search', searchBorrowedBooks, name='searchBorrowedBooks'),
    path('books/borrowBook/<str:bookID>', borrowBook, name='borrowBook'),
    path('books/returnBook/<str:bookID>/<str:borrowerID>/<str:borrowID>', returnBook, name='returnBook'),
    path('books/delayedBooks', delayedBooks, name='delayedBooks'),
    path('books/delayedBooks/searchOverDues', searchOverDues, name='delayedSearchBooks'),
    path('books/deleteBooks/<str:book>', deleteBooks, name='deleteBooks'),
    path('books/editBooks/<str:id>', editBooks, name='editBooks'),
    path('staffs', staffs, name='staffs'),
    path('staffs/searchStaffs', searchStaffs, name='searchStaffs'),
    path('staffs/addStaff', addStaff, name='addStaff'),
    path('staffs/deleteStaff/<str:staff>', deleteStaffs, name='deleteStaff'),
    path('staffs/editStaff/<str:id>', editStaff, name='editStaff'),
    path('members', members, name='members'),
    path('members/searchMembers', searchMembers, name='searchMembers'),
    path('members/addMembers', addMembers, name='addMembers'),
    path('members/deleteMembers/<str:memberr>', deleteMembers, name='deleteMembers'),
    path('members/editMembers/<str:id>', editMembers, name='editMembers'),
    path('genre', genre, name='genre'),
    path('manageAccounts', manageAccounts, name='manageAccounts'),
    path('manageAccounts/edit/<str:usernamee>', editAccounts, name='manageAccountsEdit'),
    path('manageAccounts/search', manageAccountsSearch, name='manageAccountsSearch'),
    path('manageAccounts/deleteAccounts/<str:usernamee>', deleteAccounts, name='deleteAccounts'),
    
]
