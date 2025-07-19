# Stocks
### Project Description
- Lightweight stock fundamentals research app inspired in part by the CANSLIM criteria developed by legendary investor Bill O'Neil. 
- Search for companies by EPS growth and number of institutional holders. Read about companies and visualize data. Create watchlists to track these metrics over time. Includes companies trading on the NYSE and NASDAQ.
- Based on free APIs. Some companies may not appear due to API constraints, including recent IPOs, companies with recent ticker changes, and companies with irregular earnings report dates. There are currently about 1000 companies available in the database.
- Try it out: [https://flask-stocks.onrender.com/](https://flask-stocks.onrender.com/).
  > ⚠️ **Note:** Deployed on Render's free tier. If app has been idle, it can take **half a minute to start**. This delay only occurs on first load.

### User Flow
- `Register/Log In` from the home page. The registration form only validates syntax so using a fake email works great.
- Once logged in, you can toggle between two search forms. `Multiple Conditions Search` lets you add and subtract form fields using the `+` and `-` buttons to tailor a complex search. If you already have a particular company in mind, click `Switch to Ticker Search` button to search by an individual ticker.

  ![Multiple searchfields screenshot](screenshots/search1.PNG)

- A cool feature from within the search results page is a (truncated) company description, and colored icons indicating trends in quarterly and annual EPS growth, including these numbers and number of institutional holders. This saves you time if you're searching for particular kinds of businesses, or particular trends in the data.

  ![Search results screenshot](screenshots/s_results.PNG)

- If you want to save your search results in a watchlist, click the `Save Results in Watchlist` button, at the bottom of the results page.
- Click on company names from the results page to view information about an individual company.

  ![Individual company screenshot](screenshots/company.PNG)

- If you have already created one or more watchlists, they will appear in a drop-down menu at the bottom of the company info page. Use this to add companies to your existing lists.
- From the navigation menu at the top, view and edit your existing watchlists using the `Watchlists` button. You can delete watchlists using the trash buttons on the watchlists page, or by clicking the `Delete Watchlist` button within the page for an individual list.
- Edit your watchlist title and/or description using the `Edit Watchlist` button from within the individual watchlist page. You can also remove companies from the watchlist by clicking the trash buttons.

  ![Watchlist screenshot](screenshots/watchlist.PNG)

- To view and edit your user information, including deleting your account, click your username, which appears in **bold** on the navigation menu.

  ![User account information screenshot](screenshots/user.PNG)

- Click `Log Out`on the top right to exit.

### APIs
- [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs/stable) (for ticker symbols and annual EPS numbers).
- [polygon.io](https://polygon.io/docs/rest/stocks/overview) (for quarterly EPS numbers and company descriptions).

### Technologies Used

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Flask-SQLAlchemy](https://img.shields.io/badge/Flask--SQLAlchemy-FF1717?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://flask-sqlalchemy.readthedocs.io/)
[![Flask-WTF](https://img.shields.io/badge/Flask--WTF-B41717?style=for-the-badge)](https://flask-wtf.readthedocs.io/)
[![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML/)
[![Jinja](https://img.shields.io/badge/Jinja-4B0082?style=for-the-badge&logo=jinja&logoColor=white)](https://jinja.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/)
[![jQuery](https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white)](https://jquery.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![yFinance](https://img.shields.io/badge/yFinance-0080FF?style=for-the-badge)](https://ranaroussi.github.io/yfinance/)

Deployed with [![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://render.com/)
Database hosted on [![Supabase](https://img.shields.io/badge/Supabase-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)

![Database schema diagram](schema/db_schema.PNG)

*App database schema diagram in Supabase*

---

Submitted on 2023-01-28 to fulfill the requirements of Capstone 1 project for Springboard's Software Engineering Career Track.

Enjoy!
