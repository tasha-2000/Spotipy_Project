# Spotipy_Project
This project will add 10 recommended tracks to your playlist based on your selected genre and your liked songs on Spotify

## How to run the source code
This project assumes that you already set up your Spotify app and you have your client ID and client secret

1. Clone project and open it in your favourite editor

2. Install the required libraries. In this case, you need Flask and Spotipy. You can install them using pip by running the following commands in your terminal/command prompt:
pip install Flask
pip install spotipy

3. In secrets.py, replace your_client_id and your_client_secret with your Spotify app client ID and client Secret

4.In app.py, replace your_secret_key with a key of your choice

5. Run the app by executing the main file in your terminal/command prompt:
     python main.py

6. Open your web browser and go to http://localhost:5000. This should take you to the login page of Spotify. 

<img width="625" alt="Screenshot 2023-03-12 at 7 39 14 pm" src="https://user-images.githubusercontent.com/103650882/224568859-2d6489be-e723-47a2-a9f9-cc7b8f5cb49b.png">
<img width="690" alt="Screenshot 2023-03-12 at 6 25 42 pm" src="https://user-images.githubusercontent.com/103650882/224568805-12df7dc5-9512-4d48-afb1-795c69b51f43.png">


7.Click on the "Log in with Spotify" button and enter your Spotify credentials. Once you are logged in, the app will redirect you to the page where you can select the genre for your new playlist

8. Follow the prompts and enter the required information to create your new playlist. The app will add 10 recommended tracks to your playlist based on your selected genre and your last 30 liked songs on Spotify.

<img width="402" alt="Screenshot 2023-03-12 at 7 40 29 pm" src="https://user-images.githubusercontent.com/103650882/224568932-41aae1a5-e60c-4063-8d61-48bf77fadcf9.png">

## Outcome

<img width="1496" alt="Screenshot 2023-03-12 at 7 43 16 pm" src="https://user-images.githubusercontent.com/103650882/224569113-e0e78483-9015-46b2-ad11-a3702b4cc8ed.png">



