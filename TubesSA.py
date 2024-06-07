import tkinter as tk
from tkinter import messagebox
import heapq
import timeit

class Film:
    def __init__(self, title, duration, genre, rating, popularity):
        self.title = title
        self.duration = duration
        self.genre = genre
        self.rating = rating
        self.popularity = popularity

def filter_films(films, genre=None, min_rating=None):
    filtered = films
    if genre:
        filtered = [film for film in filtered if film.genre.lower() == genre.lower()]
    if min_rating:
        filtered = [film for film in filtered if film.rating >= min_rating]
    return filtered

def dp_maximize_films(films, max_duration):
    n = len(films)
    dp = [[0 for _ in range(max_duration + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(max_duration + 1):
            if films[i - 1].duration <= w:
                dp[i][w] = max(dp[i - 1][w],
                               dp[i - 1][w - films[i - 1].duration] + films[i - 1].popularity)
            else:
                dp[i][w] = dp[i - 1][w]
    
    res = []
    w = max_duration
    i = n
    while i > 0 and w > 0:
        if dp[i][w] != dp[i - 1][w]:
            res.append(films[i - 1])
            w -= films[i - 1].duration
        i -= 1
    
    return res

def bound(node, films, max_duration):
    if node.duration >= max_duration:
        return 0
    else:
        j = node.level + 1
        tot_duration = node.duration
        bound = node.popularity

        while j < len(films) and tot_duration + films[j].duration <= max_duration:
            tot_duration += films[j].duration
            bound += films[j].popularity
            j += 1

        if j < len(films):
            bound += (max_duration - tot_duration) * (films[j].popularity / films[j].duration)

        return bound

class Node:
    def __init__(self, level, popularity, duration, films_taken):
        self.level = level
        self.popularity = popularity
        self.duration = duration
        self.films_taken = films_taken
        self.bound = 0

    def __lt__(self, other):
        return self.bound > other.bound

def branch_and_bound(films, max_duration):
    films = sorted(films, key=lambda film: film.popularity/film.duration, reverse=True)
    pq = []
    u = Node(-1, 0, 0, [])
    u.bound = bound(u, films, max_duration)
    heapq.heappush(pq, u)

    max_popularity = 0
    best_film_list = []

    while pq:
        u = heapq.heappop(pq)

        if u.bound > max_popularity and u.level < len(films) - 1:
            v = Node(u.level + 1, u.popularity + films[u.level + 1].popularity,
                     u.duration + films[u.level + 1].duration, u.films_taken + [films[u.level + 1]])
            if v.duration <= max_duration and v.popularity > max_popularity:
                max_popularity = v.popularity
                best_film_list = v.films_taken
            v.bound = bound(v, films, max_duration)
            if v.bound > max_popularity:
                heapq.heappush(pq, v)

            v = Node(u.level + 1, u.popularity, u.duration, u.films_taken)
            v.bound = bound(v, films, max_duration)
            if v.bound > max_popularity:
                heapq.heappush(pq, v)

    return best_film_list

def create_film_list(algorithm):
    max_duration = int(entry_max_duration.get())

    genre = entry_genre.get().strip()
    min_rating_input = entry_min_rating.get().strip()
    if min_rating_input == "":
        min_rating = None
    else:
        min_rating = float(min_rating_input)

    filtered_films = filter_films(films, genre, min_rating)
    
    if algorithm == "DP":
        start_time = timeit.default_timer()
        selected_films = dp_maximize_films(filtered_films, max_duration)
        elapsed_time = timeit.default_timer() - start_time
    elif algorithm == "BB":
        start_time = timeit.default_timer()
        selected_films = branch_and_bound(filtered_films, max_duration)
        elapsed_time = timeit.default_timer() - start_time

    total_duration = sum(film.duration for film in selected_films)
    result_text = "Selected Films:\n"
    for film in selected_films:
        result_text += f"{film.title} - Duration: {film.duration}, Rating: {film.rating}\n"
    result_text += f"Total Duration: {total_duration}\n"
    result_text += f"Time to generate list: {elapsed_time:.6f} seconds"

    messagebox.showinfo("Film List", result_text)

# Example usage
films = [
    Film("Film A", 90, "Action", 8.2, 150),
    Film("Film B", 120, "Drama", 7.5, 100),
    Film("Film C", 60, "Action", 8.8, 200),
    Film("Film D", 110, "Action", 9.0, 300),
    Film("Film E", 85, "Comedy", 7.0, 120),
    Film("Film F", 95, "Comedy", 6.8, 110),
    Film("Film G", 130, "Drama", 8.1, 250),
    Film("Film H", 75, "Horror", 6.5, 90),
    Film("Film I", 100, "Horror", 7.2, 130),
    Film("Film J", 105, "Action", 8.5, 220),
    Film("Film K", 90, "Action", 7.9, 140),
    Film("Film L", 140, "Drama", 9.1, 280),
    Film("Film M", 55, "Comedy", 7.4, 100),
    Film("Film N", 115, "Thriller", 8.0, 200),
    Film("Film O", 65, "Thriller", 7.3, 150),
    Film("Film P", 125, "Action", 8.7, 270),
    Film("Film Q", 80, "Romance", 7.6, 110),
    Film("Film R", 95, "Romance", 7.8, 130),
    Film("Film S", 85, "Animation", 8.0, 140),
    Film("Film T", 90, "Animation", 8.3, 160),
]

# Create main window
root = tk.Tk()
root.title("Film List Generator")

# Create labels and entry fields
label_max_duration = tk.Label(root, text="Max Duration (minutes):")
label_max_duration.grid(row=0, column=0, padx=5, pady=5)
entry_max_duration = tk.Entry(root)
entry_max_duration.grid(row=0, column=1, padx=5, pady=5)

label_genre = tk.Label(root, text="Genre (optional):")
label_genre.grid(row=1, column=0, padx=5, pady=5)
entry_genre = tk.Entry(root)
entry_genre.grid(row=1, column=1, padx=5, pady=5)

label_min_rating = tk.Label(root, text="Min Rating (optional):")
label_min_rating.grid(row=2, column=0, padx=5, pady=5)
entry_min_rating = tk.Entry(root)
entry_min_rating.grid(row=2, column=1, padx=5, pady=5)

# Create buttons
button_dp = tk.Button(root, text="Generate Film List (DP)", command=lambda: create_film_list("DP"))
button_dp.grid(row=3, column=0, padx=5, pady=5)

button_bb = tk.Button(root, text="Generate Film List (B&B)", command=lambda: create_film_list("BB"))
button_bb.grid(row=3, column=1, padx=5, pady=5)

root.mainloop()
