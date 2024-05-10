import matplotlib.pyplot as plt
import io
from datetime import datetime
import string

async def plot_starting_letters(collection):
    # Create a set of all uppercase letters and numbers
    all_letters = set(string.ascii_uppercase)
    all_letters.add('#')
    all_letters = sorted(list(all_letters))

    # Count the number of books for each letter
    letter_counts = {letter: 0 for letter in all_letters}

    for letter in all_letters:
        if letter.isalpha():
            count = collection.count_documents({"title": {"$regex": f"^{letter}", "$options": "i"}})
            letter_counts[letter] = count
        elif letter == '#':
            count = collection.count_documents({"title": {"$regex": f"^[0-9]", "$options": "i"}})
            letter_counts['#'] += count

    # Plot the bar graph
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(letter_counts.keys(), letter_counts.values(), color='violet')
    ax.set_xlabel("Starting Character")
    ax.set_ylabel("Number of Books")
    ax.set_title("Distribution of Book Titles by Starting Character", fontsize=16, fontweight='bold', pad=29)
    ax.grid(True)
    ax.tick_params(axis='both', which='major', labelsize=10)

    # Add a label to show the date generated
    date_generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ax.text(0.5, 1.05, f"Date generated: {date_generated}", transform=ax.transAxes, fontsize=8,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray',))

    # Save the plot as a file in memory
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    # Return the image plot as a binary response
    return buf

async def plot_nobel_prize(collection):
    # Query for the number of documents with has_Nobel_Prize set to True and False
    true_count = collection.count_documents({"has_Nobel_Prize": True})
    false_count = collection.count_documents({"has_Nobel_Prize": False})

    # Plot the results
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(['Won Nobel Prize', 'Didn\'t Win Nobel Prize'], [true_count, false_count], color=['gold', 'silver'])
    ax.set_xlabel("Nobel Prize Book Status")
    ax.set_ylabel("Count")
    ax.set_title("Count of Books by Nobel Prize Status", fontsize=16, fontweight='bold', pad=29)
    ax.tick_params(axis='both', which='major', labelsize=12)

    # Add a label to show the date generated
    date_generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ax.text(0.5, 1.05, f"Date generated: {date_generated}", transform=ax.transAxes, fontsize=10,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray', pad=5))

    # Save the plot as a file in memory
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    # Return the image plot as a binary response
    return buf

async def plot_release_years(collection):
   # Query for all year values in the collection
    year_values = collection.distinct("publication_year")

    # Count the number of books for each year
    year_counts = []
    for year in year_values:
        count = collection.count_documents({"publication_year": year})
        year_counts.append(count)

    # Plot the area plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.fill_between(year_values, year_counts, color='skyblue', alpha=0.4)
    ax.plot(year_values, year_counts, color='Slateblue', alpha=0.6, linewidth=2)
    ax.set_xlabel("Year Of Release")
    ax.set_ylabel("Number of Books")
    ax.set_title("Distribution of Books Over the Years", fontsize=16, fontweight='bold', pad=31)
    ax.grid(True)
    ax.tick_params(axis='both', which='major', labelsize=10)
    plt.xticks(rotation=45)

    # Add a label to show the date generated
    date_generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ax.text(0.5, 1.05, f"Date generated: {date_generated}", transform=ax.transAxes, fontsize=10,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray', pad=5))

    # Save the plot as a file in memory
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    # Return the image plot as a binary response
    return buf