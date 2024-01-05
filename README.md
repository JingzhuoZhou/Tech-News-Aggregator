# Tech News Aggregator

Overview
--------

The Tech News Aggregator is a web application that scrapes technology news articles from [sina news](https://news.sina.com.cn/roll/) and presents it in a user-friendly manner. The project is implemented using Python for web scraping, Django for the backend, and Bootstrap for the frontend. The main features include search, sorting, acategorization  and commenting of news articles.

Features
--------

* **Search:** Users can search for specific news articles based on keywords. Searching is powered by the inverted index algorithm. Search results can be filtered with their categories and sorted by post time or likes.
* **Sorting:** The website allows sorting of news articles based on different criteria (post time or likes).
* **Categorization:** News articles are categorized based on posting dates.
* **Commenting:** Comments can be posted to or deleted from any articles in the website.

Technology Stack
----------------

* **Python:** Web scraping is implemented using Python.
* **Django:** The backend is built using the Django web framework.
* **Bootstrap:** The frontend is designed using the Bootstrap framework.

Setup
-----

1. Clone the repository:
   
   ```bash
   git clone https://github.com/JingzhuoZhou/tech-news-aggregator.git
   ```

2. Install dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

3. Scrape the news:
   
   ```bash
   cd crawler
   python crawler_url.py
   python crawler_info.py
   python crawler_data.py
   ```

4. Create inverted index:
   
   ```bash
   cd ../inverted-index
   python inverted-index.py
   ```

5. Run migrations:
   
   ```bash
   cd ../web
   python manage.py migrate
   ```

6. Start the Django development server:
   
   ```bash
   python manage.py runserver
   ```

7. Access the admin page at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) and import article data (crawler/data.json) and the inverted index data (inverted-index/dic.json) to django's database.

8. Access the admin page at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and enjoy your daily tech news! 


