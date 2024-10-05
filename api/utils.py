import json
from api.models import Authors, Books  # Replace 'your_app' with your actual app name

def load_authors_from_json(json_file_path):
    """
    Load authors from a JSON file and insert them into the Author table.
    
    Args:
        json_file_path (str): The path to the JSON file containing author data.
    """
    with open(json_file_path, 'r') as file:
        idx = 0
        
        for line in file:
            idx += 1  # Increment the index
            author_data1 = json.loads(line)

            try:
                author_data = json.loads(line)
                Authors.objects.update_or_create(
                    id=author_data['id'],
                    defaults={
                        'name': author_data['name'],
                        'gender': author_data['gender'],
                        'ratings_count': author_data['ratings_count'],
                        'average_rating': author_data['average_rating'],
                        'text_reviews_count': author_data['text_reviews_count'],
                        'works_count': author_data['works_count'],
                        'book_ids': author_data['book_ids'],
                        'work_ids': author_data['work_ids'],
                        'image_url': author_data['image_url'],
                        'about': author_data['about'],
                        'fans_count': author_data['fans_count'],
                    }
                )
                # print(f"Processed author {idx}: {author_data['name']}")
            except Exception as e:
                print('Nilai author: ', author_data1)
                print(f"Error processing line {idx}: {e}")
    print("Authors imported successfully!")

def load_books_from_json(json_file_path='/Users/rizalilham/Documents/Projects/books_authors_management/books.json'):
    """
    Load books from a JSON file and insert them into the Books table.
    
    Args:
        json_file_path (str): The path to the JSON file containing book data.
    """
    not_inserted_books = []  # List to hold books that were not inserted
    errors = []
    
    with open(json_file_path, 'r') as file:
        idx = 0
        
        for line in file:
            idx += 1  # Increment the index
            book_data = json.loads(line)

            try:
                # Extracting shelves and converting to JSON
                shelves_data = json.dumps(book_data['shelves'])

                # Handling num_pages with a default value
                num_pages = 0 if book_data['num_pages'] == '' else book_data['num_pages']
                
                # Insert or update book data
                Books.objects.update_or_create(
                    id=book_data['id'],
                    defaults={
                        'title': book_data['title'],
                        'work_id': book_data['work_id'],
                        'isbn': book_data['isbn'],
                        'isbn13': book_data['isbn13'],
                        'asin': book_data['asin'],
                        'language': book_data['language'],
                        'average_rating': book_data['average_rating'],
                        'rating_dist': book_data['rating_dist'],
                        'ratings_count': book_data['ratings_count'],
                        'text_reviews_count': book_data['text_reviews_count'],
                        'publication_date': book_data['publication_date'],
                        'original_publication_date': book_data['original_publication_date'],
                        'format': book_data['format'],
                        'edition_information': book_data['edition_information'],
                        'image_url': book_data['image_url'],
                        'publisher': book_data['publisher'],
                        'num_pages': num_pages,
                        'series_id': book_data['series_id'],
                        'series_name': book_data['series_name'],
                        'series_position': book_data['series_position'],
                        'shelves': shelves_data,
                        'description': book_data['description'],
                    }
                )
                print(f"Processed book {idx}: {book_data}")
            
            except Exception as e:
                print(f"Error processing line {idx}: {e}")
                # Store the entire book_data for logging
                print('iddddnya: ', idx)
                not_inserted_books.append(book_data)  # Append the raw book data
                
                # Write non-inserted book data to a JSON file immediately
                filename = '/Users/rizalilham/Documents/Projects/books_authors_management/not_inserted_books.json'
                with open(filename, 'w') as outfile:
                    json.dump(not_inserted_books, outfile, indent=4)

    print("Books imported successfully!")
    

def count_total(json_file_path):
    """
    Load books from a JSON file and insert them into the Books table.
    
    Args:
        json_file_path (str): The path to the JSON file containing book data.
    """
    idx = 0
    with open(json_file_path, 'r') as file:
        
        for line in file:
            idx += 1
            print('idx: ', idx)
            
    print('total data is: ', idx)
    
"""
{
  "id": "2",
  "title": "Harry Potter and the Order of the Phoenix (Harry Potter, #5)",
  "authors": [
    {
      "id": "1077326",
      "name": "J.K. Rowling",
      "role": ""
    },
    {
      "id": "2927",
      "name": "Mary GrandPré",
      "role": "Illustrator"
    }
  ],
  "author_name": "J.K. Rowling",
  "author_id": "1077326",
  "work_id": "2809203",
  "isbn": "0439358078",
  "isbn13": "9780439358071",
  "asin": "",
  "language": "eng",
  "average_rating": 4.5,
  "rating_dist": "5:1674064|4:664833|3:231195|2:41699|1:16215|total:2628006",
  "ratings_count": 2628006,
  "text_reviews_count": 44716,
  "publication_date": "2004-09",
  "original_publication_date": "2003-06-21",
  "format": "Paperback",
  "edition_information": "US Edition",
  "image_url": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1546910265l/2._SX98_.jpg",
  "publisher": "Scholastic Inc.",
  "num_pages": 870,
  "series_id": "45175",
  "series_name": "Harry Potter",
  "series_position": "5",
  "shelves": [
    {
      "name": "to-read",
      "count": 324191
    },
    {
      "name": "currently-reading",
      "count": 52675
    },
    {
      "name": "fantasy",
      "count": 48251
    },
    {
      "name": "favorites",
      "count": 38332
    },
    {
      "name": "young-adult",
      "count": 15837
    },
    {
      "name": "fiction",
      "count": 13971
    },
    {
      "name": "harry-potter",
      "count": 9798
    },
    {
      "name": "books-i-own",
      "count": 8230
    },
    {
      "name": "owned",
      "count": 7664
    },
    {
      "name": "ya",
      "count": 5790
    },
    {
      "name": "series",
      "count": 4859
    },
    {
      "name": "favourites",
      "count": 4359
    },
    {
      "name": "magic",
      "count": 3985
    },
    {
      "name": "childrens",
      "count": 2955
    },
    {
      "name": "re-read",
      "count": 2396
    },
    {
      "name": "owned-books",
      "count": 2277
    },
    {
      "name": "adventure",
      "count": 2097
    },
    {
      "name": "audiobook",
      "count": 1910
    },
    {
      "name": "children",
      "count": 1901
    },
    {
      "name": "audiobooks",
      "count": 1792
    },
    {
      "name": "middle-grade",
      "count": 1760
    },
    {
      "name": "childhood",
      "count": 1578
    },
    {
      "name": "j-k-rowling",
      "count": 1540
    },
    {
      "name": "my-books",
      "count": 1405
    },
    {
      "name": "classics",
      "count": 1372
    },
    {
      "name": "reread",
      "count": 1341
    },
    {
      "name": "children-s",
      "count": 1340
    },
    {
      "name": "sci-fi-fantasy",
      "count": 1298
    },
    {
      "name": "all-time-favorites",
      "count": 1288
    },
    {
      "name": "5-stars",
      "count": 1213
    },
    {
      "name": "default",
      "count": 1195
    },
    {
      "name": "fantasy",
      "count": 1156
    },
    {
      "name": "my-library",
      "count": 1084
    },
    {
      "name": "novels",
      "count": 1030
    },
    {
      "name": "ya-fantasy",
      "count": 982
    },
    {
      "name": "children-s-books",
      "count": 964
    },
    {
      "name": "favorite-books",
      "count": 936
    },
    {
      "name": "kids",
      "count": 932
    },
    {
      "name": "i-own",
      "count": 926
    },
    {
      "name": "fantasy-sci-fi",
      "count": 908
    },
    {
      "name": "favorite",
      "count": 859
    },
    {
      "name": "audio",
      "count": 850
    },
    {
      "name": "library",
      "count": 774
    },
    {
      "name": "english",
      "count": 771
    },
    {
      "name": "read-more-than-once",
      "count": 740
    },
    {
      "name": "urban-fantasy",
      "count": 739
    },
    {
      "name": "paranormal",
      "count": 738
    },
    {
      "name": "books",
      "count": 728
    },
    {
      "name": "re-reads",
      "count": 695
    },
    {
      "name": "witches",
      "count": 685
    },
    {
      "name": "teen",
      "count": 672
    },
    {
      "name": "british",
      "count": 632
    },
    {
      "name": "jk-rowling",
      "count": 631
    },
    {
      "name": "bookshelf",
      "count": 588
    },
    {
      "name": "ya-fiction",
      "count": 587
    },
    {
      "name": "novel",
      "count": 578
    },
    {
      "name": "mystery",
      "count": 562
    },
    {
      "name": "my-bookshelf",
      "count": 557
    },
    {
      "name": "kindle",
      "count": 556
    },
    {
      "name": "childrens-books",
      "count": 550
    },
    {
      "name": "read-in-2017",
      "count": 541
    },
    {
      "name": "harry-potter-series",
      "count": 538
    },
    {
      "name": "read-in-2020",
      "count": 536
    },
    {
      "name": "on-my-shelf",
      "count": 534
    },
    {
      "name": "read-in-2016",
      "count": 520
    },
    {
      "name": "own-it",
      "count": 517
    },
    {
      "name": "faves",
      "count": 515
    },
    {
      "name": "rereads",
      "count": 509
    },
    {
      "name": "my-favorites",
      "count": 502
    },
    {
      "name": "supernatural",
      "count": 501
    },
    {
      "name": "read-in-2019",
      "count": 493
    },
    {
      "name": "read-in-2018",
      "count": 488
    },
    {
      "name": "audible",
      "count": 475
    },
    {
      "name": "childhood-favorites",
      "count": 474
    },
    {
      "name": "audio-books",
      "count": 466
    },
    {
      "name": "young-adult-fiction",
      "count": 464
    },
    {
      "name": "scifi-fantasy",
      "count": 455
    },
    {
      "name": "ebook",
      "count": 446
    },
    {
      "name": "fantasia",
      "count": 444
    },
    {
      "name": "youth",
      "count": 438
    },
    {
      "name": "coming-of-age",
      "count": 428
    },
    {
      "name": "5-star",
      "count": 422
    },
    {
      "name": "favorite-series",
      "count": 419
    },
    {
      "name": "favourite",
      "count": 418
    },
    {
      "name": "all-time-favourites",
      "count": 413
    },
    {
      "name": "hp",
      "count": 412
    },
    {
      "name": "wizards",
      "count": 406
    },
    {
      "name": "favs",
      "count": 404
    },
    {
      "name": "childhood-books",
      "count": 404
    },
    {
      "name": "kids-books",
      "count": 401
    },
    {
      "name": "made-me-cry",
      "count": 390
    },
    {
      "name": "tbr",
      "count": 387
    },
    {
      "name": "kindle-unlimited",
      "count": 387
    },
    {
      "name": "juvenile",
      "count": 382
    },
    {
      "name": "read-in-2015",
      "count": 379
    },
    {
      "name": "have",
      "count": 375
    },
    {
      "name": "read-in-english",
      "count": 370
    },
    {
      "name": "fantasy-scifi",
      "count": 363
    },
    {
      "name": "read-2020",
      "count": 361
    },
    {
      "name": "favoritos",
      "count": 360
    }
  ],
  "description": "There is a door at the end of a silent corridor. And it’s haunting Harry Pottter’s dreams. Why else would he be waking in the middle of the night, screaming in terror?<br /><br />Harry has a lot on his mind for this, his fifth year at Hogwarts: a Defense Against the Dark Arts teacher with a personality like poisoned honey; a big surprise on the Gryffindor Quidditch team; and the looming terror of the Ordinary Wizarding Level exams. But all these things pale next to the growing threat of He-Who-Must-Not-Be-Named - a threat that neither the magical government nor the authorities at Hogwarts can stop.<br /><br />As the grasp of darkness tightens, Harry must discover the true depth and strength of his friends, the importance of boundless loyalty, and the shocking price of unbearable sacrifice.<br /><br />His fate depends on them all."
}
"""