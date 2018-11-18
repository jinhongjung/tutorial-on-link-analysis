import codecs

edges = []
max_u_id = 0

with open('u.data', 'r') as input_file:
    for line in input_file:
        items = line.split()
        #  print(items)
        user = int(items[0]) - 1
        movie = int(items[1]) - 1
        rating = int(items[2])
        edge = [user, movie, rating]
        edges.append(edge)

        max_u_id = max(max_u_id, user)

    max_u_id = max_u_id + 1

with open('edges.tsv', 'w') as output_file:
    for edge in edges:
        user, movie, rating = edge
        movie = movie + max_u_id
        line = "{}\t{}\t{}\n".format(user, movie, rating)
        output_file.write(line)

male_names = []
with open('census-dist-male-first.txt', 'r') as input_file:
    for line in input_file:
        items = line.split()
        name = items[0].lower()
        male_names.append(name)

female_names = []
with open('census-dist-female-first.txt', 'r') as input_file:
    for line in input_file:
        items = line.split()
        name = items[0].lower()
        female_names.append(name)

node_labels = {}
user_node_labels = {}
with open('u.user', 'r') as input_file:
    for line in input_file:
        items = line.split('|')
        user = int(items[0]) - 1
        age = int(items[1])
        gender = items[2]
        job = items[3]
        if gender is 'M':
            name = male_names[user]
        else:
            name = female_names[user]

        label = "{}\t{}\t{}\t{}\t{}".format("user", name, gender, age, job)
        user_node_labels[user] = label
        node_labels[user] = label

genres = {}
with open('u.genre', 'r') as input_file:
    for line in input_file:
        items = line.split('|')
        genre = items[0].lower()
        genre_id = int(items[1])
        genres[genre_id] = genre

movie_node_labels = {}
with codecs.open('u.item', 'r', encoding='utf-8', errors='ignore') as input_file:
    for line in input_file:
        items = line.split('|')
        movie = int(items[0]) - 1
        movie = movie + max_u_id
        movie_name = items[1]
        date = items[2]
        url = items[3]
        genre_array = items[5:]
        movie_genres = []
        for i, genre_flag in zip(range(len(genre_array)), genre_array):
            if int(genre_flag) is 1:
                genre = genres[i]
                movie_genres.append(genre)

        genre_label = movie_genres[0]
        for movie_genre in movie_genres[1:]:
            genre_label = "{};{}".format(genre_label, movie_genre)

        label = "{}\t{}\t{}".format("movie", movie_name, genre_label)
        movie_node_labels[movie] = label
        node_labels[movie] = label

with open("user_node_labels.tsv", "w") as output_file:
    for key in sorted(user_node_labels):
        node_label = user_node_labels[key]
        line = "{}\t{}\n".format(key, node_label)
        output_file.write(line)

with open("movie_node_labels.tsv", "w") as output_file:
    for key in sorted(movie_node_labels):
        node_label = movie_node_labels[key]
        line = "{}\t{}\n".format(key, node_label)
        output_file.write(line)

with open("node_labels.tsv", "w") as output_file:
    for key in sorted(node_labels):
        node_label = node_labels[key]
        line = "{}\t{}\n".format(key, node_label)
        output_file.write(line)
